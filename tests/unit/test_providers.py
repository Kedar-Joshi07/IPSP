"""Phase 1B composition wiring tests."""

from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Settings
from ipsp.security.outbound import (
    OutboundAction,
    OutboundRequest,
    RemoteTransmissionLevel,
)
from ipsp.security.secrets import SecretRef


def test_foundation_services_are_explicitly_composed() -> None:
    marker = "DO_NOT_LEAK_PHASE1B_SECRET"
    settings = Settings(
        _env_file=None,
        features={"remote_llm_enabled": True},
        outbound={
            "internet_enabled": True,
            "remote_llm_enabled": True,
            "allowed_remote_providers": ["provider-a"],
            "default_remote_transmission": "sanitized_schema_only",
        },
    )

    services = build_foundation_services(
        settings,
        environ={"PROVIDER_A_API_KEY": marker},
    )

    secret = services.secret_provider.require(
        SecretRef(provider="environment", key="PROVIDER_A_API_KEY")
    )
    decision = services.outbound_policy.evaluate(
        OutboundRequest(
            action=OutboundAction.REMOTE_LLM,
            provider="provider-a",
            transmission_level=RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY,
        )
    )

    assert services.settings is settings
    assert services.feature_flags is settings.features
    assert services.database_sessions is not None
    assert services.migration_state is not None
    assert services.readiness_service is not None
    assert secret.reveal() == marker
    assert decision.allowed is True
    assert marker not in repr(services)
    services.database_engine.dispose()
