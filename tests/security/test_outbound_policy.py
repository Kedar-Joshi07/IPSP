"""Backend outbound-policy allow and deny behavior."""

import pytest
from ipsp.errors.exceptions import IPSPError
from ipsp.security.outbound import (
    DatasetClassification,
    OutboundAction,
    OutboundPolicy,
    OutboundRequest,
    PolicyDenialReason,
    RemoteTransmissionLevel,
)


def _policy(**overrides: object) -> OutboundPolicy:
    values: dict[str, object] = {
        "internet_enabled": True,
        "remote_llm_enabled": True,
        "remote_llm_feature_enabled": True,
        "allowed_remote_providers": ("provider-a",),
        "model_download_enabled": True,
        "update_check_enabled": True,
        "default_transmission_level": RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
    }
    values.update(overrides)
    return OutboundPolicy(**values)  # type: ignore[arg-type]


def _remote_request(
    level: RemoteTransmissionLevel = RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
    **overrides: object,
) -> OutboundRequest:
    values: dict[str, object] = {
        "action": OutboundAction.REMOTE_LLM,
        "provider": "provider-a",
        "transmission_level": level,
    }
    values.update(overrides)
    return OutboundRequest(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "action",
    [OutboundAction.REMOTE_LLM, OutboundAction.MODEL_DOWNLOAD, OutboundAction.UPDATE_CHECK],
)
def test_global_internet_off_denies_every_internet_action(action: OutboundAction) -> None:
    request = (
        _remote_request() if action is OutboundAction.REMOTE_LLM else OutboundRequest(action=action)
    )
    decision = _policy(internet_enabled=False).evaluate(request)

    assert decision.allowed is False
    assert decision.reason is PolicyDenialReason.INTERNET_DISABLED


def test_remote_llm_outbound_off_denies_enabled_feature() -> None:
    decision = _policy(remote_llm_enabled=False).evaluate(_remote_request())

    assert decision.reason is PolicyDenialReason.REMOTE_LLM_DISABLED


def test_remote_feature_off_is_an_additional_denial_layer() -> None:
    decision = _policy(remote_llm_feature_enabled=False).evaluate(_remote_request())

    assert decision.reason is PolicyDenialReason.FEATURE_DISABLED


def test_model_download_permission_off_denies_download() -> None:
    decision = _policy(model_download_enabled=False).evaluate(
        OutboundRequest(action=OutboundAction.MODEL_DOWNLOAD)
    )

    assert decision.reason is PolicyDenialReason.MODEL_DOWNLOAD_DISABLED


def test_update_check_permission_off_denies_check() -> None:
    decision = _policy(update_check_enabled=False).evaluate(
        OutboundRequest(action=OutboundAction.UPDATE_CHECK)
    )

    assert decision.reason is PolicyDenialReason.UPDATE_CHECK_DISABLED


def test_missing_or_unapproved_remote_provider_is_denied() -> None:
    missing = _policy().evaluate(_remote_request(provider=None))
    unapproved = _policy().evaluate(_remote_request(provider="provider-b"))

    assert missing.reason is PolicyDenialReason.PROVIDER_REQUIRED
    assert unapproved.reason is PolicyDenialReason.PROVIDER_NOT_ALLOWED


def test_approved_provider_passes_when_every_layer_allows() -> None:
    decision = _policy().evaluate(_remote_request())

    assert decision.allowed is True
    assert decision.reason is None


@pytest.mark.parametrize(
    ("maximum", "requested", "allowed"),
    [
        (
            RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
            RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
            True,
        ),
        (
            RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
            RemoteTransmissionLevel.ORIGINAL_COLUMN_NAMES_NO_VALUES,
            False,
        ),
        (
            RemoteTransmissionLevel.ORIGINAL_COLUMN_NAMES_NO_VALUES,
            RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
            True,
        ),
        (
            RemoteTransmissionLevel.SANITIZED_AGGREGATES_ANONYMIZED_EXAMPLES,
            RemoteTransmissionLevel.SANITIZED_AGGREGATES_ANONYMIZED_EXAMPLES,
            True,
        ),
    ],
)
def test_transmission_levels_obey_ordering(
    maximum: RemoteTransmissionLevel,
    requested: RemoteTransmissionLevel,
    allowed: bool,
) -> None:
    classifications = frozenset({DatasetClassification.ORDINARY_BUSINESS_DATA})
    decision = _policy(default_transmission_level=maximum).evaluate(
        _remote_request(requested, dataset_classifications=classifications)
    )

    assert decision.allowed is allowed
    if not allowed:
        assert decision.reason is PolicyDenialReason.TRANSMISSION_EXCEEDS_POLICY


def test_remote_disabled_level_never_authorizes_remote_llm() -> None:
    decision = _policy(
        default_transmission_level=RemoteTransmissionLevel.EXPLICITLY_APPROVED_SAMPLE_ROWS
    ).evaluate(_remote_request(RemoteTransmissionLevel.REMOTE_DISABLED))

    assert decision.reason is PolicyDenialReason.REMOTE_TRANSMISSION_DISABLED


def test_restricted_dataset_defaults_to_local_only() -> None:
    decision = _policy().evaluate(
        _remote_request(
            dataset_classifications=frozenset({DatasetClassification.CONFIDENTIAL_RESTRICTED})
        )
    )

    assert decision.reason is PolicyDenialReason.RESTRICTED_DATASET_REQUIRES_POLICY


def test_explicit_sample_rows_cannot_use_default_policy() -> None:
    decision = _policy(
        default_transmission_level=RemoteTransmissionLevel.EXPLICITLY_APPROVED_SAMPLE_ROWS
    ).evaluate(
        _remote_request(
            RemoteTransmissionLevel.EXPLICITLY_APPROVED_SAMPLE_ROWS,
            dataset_classifications=frozenset({DatasetClassification.ORDINARY_BUSINESS_DATA}),
        )
    )

    assert decision.reason is PolicyDenialReason.EXPLICIT_ROW_APPROVAL_REQUIRED


def test_explicit_dataset_policy_can_allow_approved_rows() -> None:
    decision = _policy().evaluate(
        _remote_request(
            RemoteTransmissionLevel.EXPLICITLY_APPROVED_SAMPLE_ROWS,
            dataset_classifications=frozenset({DatasetClassification.ORDINARY_BUSINESS_DATA}),
            dataset_policy_level=RemoteTransmissionLevel.EXPLICITLY_APPROVED_SAMPLE_ROWS,
        )
    )

    assert decision.allowed is True


def test_sensitive_transmission_without_classification_context_fails_closed() -> None:
    decision = _policy(
        default_transmission_level=(
            RemoteTransmissionLevel.SANITIZED_AGGREGATES_ANONYMIZED_EXAMPLES
        )
    ).evaluate(_remote_request(RemoteTransmissionLevel.SANITIZED_AGGREGATES_ANONYMIZED_EXAMPLES))

    assert decision.reason is PolicyDenialReason.SENSITIVE_CONTEXT_REQUIRED


def test_require_allowed_raises_safe_domain_error_without_secret_marker() -> None:
    marker = "DO_NOT_LEAK_PHASE1B_SECRET"

    with pytest.raises(IPSPError) as caught:
        _policy(internet_enabled=False).require_allowed(_remote_request())

    assert caught.value.error_code == "SYS-OUTBOUND_DENIED"
    assert marker not in str(caught.value)
    assert marker not in repr(caught.value.details)


def test_policy_request_rejects_secret_bearing_extra_input() -> None:
    marker = "DO_NOT_LEAK_PHASE1B_SECRET"

    with pytest.raises(TypeError) as caught:
        OutboundRequest(  # type: ignore[call-arg]
            action=OutboundAction.UPDATE_CHECK,
            secret=marker,
        )

    assert marker not in str(caught.value)
