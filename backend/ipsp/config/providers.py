"""Explicit construction of configured Phase 1B foundation services."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ipsp.config.feature_flags import FeatureFlags
from ipsp.config.settings import Settings
from ipsp.security.outbound import OutboundPolicy
from ipsp.security.secrets import EnvironmentSecretProvider, SecretProvider


@dataclass(frozen=True, slots=True)
class FoundationServices:
    """Immutable composition result injected at the application boundary."""

    settings: Settings
    feature_flags: FeatureFlags
    secret_provider: SecretProvider
    outbound_policy: OutboundPolicy


def build_foundation_services(
    settings: Settings,
    *,
    environ: Mapping[str, str] | None = None,
) -> FoundationServices:
    """Construct Phase 1B services without mutable globals or provider side effects."""
    secret_provider = EnvironmentSecretProvider(environ)
    outbound = settings.outbound
    outbound_policy = OutboundPolicy(
        internet_enabled=outbound.internet_enabled,
        remote_llm_enabled=outbound.remote_llm_enabled,
        remote_llm_feature_enabled=settings.features.remote_llm_enabled,
        allowed_remote_providers=outbound.allowed_remote_providers,
        model_download_enabled=outbound.model_download_enabled,
        update_check_enabled=outbound.update_check_enabled,
        default_transmission_level=outbound.default_remote_transmission,
    )
    return FoundationServices(
        settings=settings,
        feature_flags=settings.features,
        secret_provider=secret_provider,
        outbound_policy=outbound_policy,
    )
