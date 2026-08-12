"""Side-effect-free outbound and remote-transmission policy enforcement."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum

from ipsp.errors.exceptions import IPSPError
from ipsp.security.secrets import validate_provider_identifier


class OutboundAction(StrEnum):
    """Internet-dependent purposes evaluated by the backend policy."""

    REMOTE_LLM = "remote_llm"
    MODEL_DOWNLOAD = "model_download"
    UPDATE_CHECK = "update_check"
    OTHER_INTERNET = "other_internet"


class RemoteTransmissionLevel(StrEnum):
    """The five ordered remote-data policies frozen by the privacy specification."""

    REMOTE_DISABLED = "remote_disabled"
    SANITIZED_SCHEMA_ONLY = "sanitized_schema_only"
    ORIGINAL_COLUMN_NAMES_NO_VALUES = "original_column_names_no_values"
    SANITIZED_AGGREGATES_ANONYMIZED_EXAMPLES = "sanitized_aggregates_anonymized_examples"
    EXPLICITLY_APPROVED_SAMPLE_ROWS = "explicitly_approved_sample_rows"

    @property
    def rank(self) -> int:
        return tuple(type(self)).index(self)


class DatasetClassification(StrEnum):
    """Policy vocabulary supplied by future classification and Admin workflows."""

    ORDINARY_BUSINESS_DATA = "ordinary_business_data"
    DIRECT_IDENTIFIER = "direct_identifier"
    QUASI_IDENTIFIER = "quasi_identifier"
    FINANCIAL_SENSITIVE = "financial_sensitive"
    SENSITIVE_DEMOGRAPHIC = "sensitive_demographic"
    CONFIDENTIAL_RESTRICTED = "confidential_restricted"


class PolicyDenialReason(StrEnum):
    """Stable, safe explanations for denied outbound requests."""

    INTERNET_DISABLED = "internet_disabled"
    FEATURE_DISABLED = "feature_disabled"
    REMOTE_LLM_DISABLED = "remote_llm_disabled"
    MODEL_DOWNLOAD_DISABLED = "model_download_disabled"
    UPDATE_CHECK_DISABLED = "update_check_disabled"
    PROVIDER_REQUIRED = "provider_required"
    PROVIDER_NOT_ALLOWED = "provider_not_allowed"
    REMOTE_TRANSMISSION_DISABLED = "remote_transmission_disabled"
    TRANSMISSION_EXCEEDS_POLICY = "transmission_exceeds_policy"
    RESTRICTED_DATASET_REQUIRES_POLICY = "restricted_dataset_requires_policy"
    EXPLICIT_ROW_APPROVAL_REQUIRED = "explicit_row_approval_required"
    SENSITIVE_CONTEXT_REQUIRED = "sensitive_context_required"


@dataclass(frozen=True, slots=True)
class OutboundRequest:
    """Complete policy input for a proposed future outbound operation."""

    action: OutboundAction
    provider: str | None = None
    transmission_level: RemoteTransmissionLevel = RemoteTransmissionLevel.REMOTE_DISABLED
    dataset_classifications: frozenset[DatasetClassification] = field(default_factory=frozenset)
    dataset_policy_level: RemoteTransmissionLevel | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.action, OutboundAction):
            raise ValueError("Outbound actions must use OutboundAction values")
        if not isinstance(self.transmission_level, RemoteTransmissionLevel):
            raise ValueError("Transmission levels must use RemoteTransmissionLevel values")
        if self.dataset_policy_level is not None and not isinstance(
            self.dataset_policy_level, RemoteTransmissionLevel
        ):
            raise ValueError("Dataset policy levels must use RemoteTransmissionLevel values")
        if self.provider is not None:
            validate_provider_identifier(self.provider)
        if not all(
            isinstance(classification, DatasetClassification)
            for classification in self.dataset_classifications
        ):
            raise ValueError("Dataset classifications must use DatasetClassification values")


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Safe policy outcome that grants permission but never performs an operation."""

    allowed: bool
    action: OutboundAction
    reason: PolicyDenialReason | None = None
    allowed_transmission_level: RemoteTransmissionLevel | None = None


@dataclass(frozen=True, slots=True)
class OutboundPolicyState:
    """Non-secret immutable diagnostics for the active outbound policy."""

    internet_enabled: bool
    remote_llm_enabled: bool
    model_download_enabled: bool
    update_check_enabled: bool
    default_transmission_level: RemoteTransmissionLevel
    allowed_remote_provider_count: int


class OutboundPolicy:
    """Evaluate all outbound layers with deny-by-default behavior."""

    def __init__(
        self,
        *,
        internet_enabled: bool,
        remote_llm_enabled: bool,
        remote_llm_feature_enabled: bool,
        allowed_remote_providers: Iterable[str],
        model_download_enabled: bool,
        update_check_enabled: bool,
        default_transmission_level: RemoteTransmissionLevel,
    ) -> None:
        self._internet_enabled = internet_enabled
        self._remote_llm_enabled = remote_llm_enabled
        self._remote_llm_feature_enabled = remote_llm_feature_enabled
        self._allowed_remote_providers = frozenset(
            validate_provider_identifier(provider) for provider in allowed_remote_providers
        )
        self._model_download_enabled = model_download_enabled
        self._update_check_enabled = update_check_enabled
        self._default_transmission_level = default_transmission_level

    @staticmethod
    def _deny(request: OutboundRequest, reason: PolicyDenialReason) -> PolicyDecision:
        return PolicyDecision(allowed=False, action=request.action, reason=reason)

    def evaluate(self, request: OutboundRequest) -> PolicyDecision:
        """Return a deterministic decision without performing network activity."""
        if not self._internet_enabled:
            return self._deny(request, PolicyDenialReason.INTERNET_DISABLED)

        if request.action is OutboundAction.REMOTE_LLM:
            return self._evaluate_remote_llm(request)
        if request.action is OutboundAction.MODEL_DOWNLOAD and not self._model_download_enabled:
            return self._deny(request, PolicyDenialReason.MODEL_DOWNLOAD_DISABLED)
        if request.action is OutboundAction.UPDATE_CHECK and not self._update_check_enabled:
            return self._deny(request, PolicyDenialReason.UPDATE_CHECK_DISABLED)
        if request.provider is not None and request.provider not in self._allowed_remote_providers:
            return self._deny(request, PolicyDenialReason.PROVIDER_NOT_ALLOWED)
        return PolicyDecision(allowed=True, action=request.action)

    def _evaluate_remote_llm(self, request: OutboundRequest) -> PolicyDecision:
        if not self._remote_llm_enabled:
            return self._deny(request, PolicyDenialReason.REMOTE_LLM_DISABLED)
        if not self._remote_llm_feature_enabled:
            return self._deny(request, PolicyDenialReason.FEATURE_DISABLED)
        if request.provider is None:
            return self._deny(request, PolicyDenialReason.PROVIDER_REQUIRED)
        if request.provider not in self._allowed_remote_providers:
            return self._deny(request, PolicyDenialReason.PROVIDER_NOT_ALLOWED)
        if request.transmission_level is RemoteTransmissionLevel.REMOTE_DISABLED:
            return self._deny(request, PolicyDenialReason.REMOTE_TRANSMISSION_DISABLED)

        classifications = request.dataset_classifications
        if (
            request.transmission_level.rank
            >= RemoteTransmissionLevel.SANITIZED_AGGREGATES_ANONYMIZED_EXAMPLES.rank
            and not classifications
        ):
            return self._deny(request, PolicyDenialReason.SENSITIVE_CONTEXT_REQUIRED)
        if (
            DatasetClassification.CONFIDENTIAL_RESTRICTED in classifications
            and request.dataset_policy_level is None
        ):
            return self._deny(
                request,
                PolicyDenialReason.RESTRICTED_DATASET_REQUIRES_POLICY,
            )
        if (
            request.transmission_level is RemoteTransmissionLevel.EXPLICITLY_APPROVED_SAMPLE_ROWS
            and request.dataset_policy_level is None
        ):
            return self._deny(request, PolicyDenialReason.EXPLICIT_ROW_APPROVAL_REQUIRED)

        allowed_level = request.dataset_policy_level or self._default_transmission_level
        if request.transmission_level.rank > allowed_level.rank:
            return self._deny(request, PolicyDenialReason.TRANSMISSION_EXCEEDS_POLICY)
        return PolicyDecision(
            allowed=True,
            action=request.action,
            allowed_transmission_level=allowed_level,
        )

    def require_allowed(self, request: OutboundRequest) -> PolicyDecision:
        """Return an allowed decision or raise a safe domain error."""
        decision = self.evaluate(request)
        if not decision.allowed:
            assert decision.reason is not None
            raise IPSPError(
                "SYS-OUTBOUND_DENIED",
                "The outbound operation is denied by policy.",
                details={
                    "action": request.action.value,
                    "provider": request.provider,
                    "reason": decision.reason.value,
                },
            )
        return decision

    def diagnostics(self) -> OutboundPolicyState:
        """Return safe policy facts without provider identifiers or mutation."""
        return OutboundPolicyState(
            internet_enabled=self._internet_enabled,
            remote_llm_enabled=self._remote_llm_enabled,
            model_download_enabled=self._model_download_enabled,
            update_check_enabled=self._update_check_enabled,
            default_transmission_level=self._default_transmission_level,
            allowed_remote_provider_count=len(self._allowed_remote_providers),
        )
