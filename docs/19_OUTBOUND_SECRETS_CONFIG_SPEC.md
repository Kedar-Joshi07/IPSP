# Outbound Access, Secrets & Configuration

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** v0.1.1 retains only the accepted foundation configuration/secrets
boundary; Remote/Hybrid LLM, PUBLIC_WEB, and APPROVED_CONNECTORS are NOT IMPLEMENTED

This specification freezes backend enforcement and non-secret/secret configuration boundaries. It
does not enable network access, install a provider, download a model, create a connector, or store a
credential.

## Outbound Access Policy Manager

Backend-enforced policy controls at least:

- global network/Internet availability and purpose;
- exact evidence-access mode: `OFF`, `INTERNAL_ONLY`, `PUBLIC_WEB`, or `APPROVED_CONNECTORS`;
- remote/Hybrid LLM eligibility and allowed provider/model/endpoint/region combinations;
- approved public-source classes and registered connector identities/scopes;
- model, model-weight, adapter, package, and update-check/download permission;
- organization, project/dataset, user, data-class, field/row, purpose, destination, payload, retention,
  and provider-training restrictions;
- feature flags, rate/resource limits, and emergency disablement.

UI state, LLM mode, provider availability, connector capability, or stored credential never grants
outbound access.

## Effective permission and request snapshot

Every outbound evidence or LLM operation computes:

```text
Admin policy ∩ project/dataset policy ∩ runtime user consent
```

The effective decision is scoped to the exact actor, purpose, evidence-access and LLM modes, source,
destination/provider/connector, requested fields/data classes, transformations, time, and retention.
Any missing or denied component fails closed.

The request records immutable references to policy/consent versions, allow/deny reason, minimization/
sanitization profile, provider/connector and license decisions, non-secret configuration, and audit/
trace. It never stores credential values. PUBLIC_WEB and APPROVED_CONNECTORS remain planned modes and
cannot be inferred as operational from this contract.

## SecretProvider

SQLite stores provider/connector metadata and secret references, not ordinary plaintext passwords,
API keys, tokens, certificates, auth cookies, or credentials. A `SecretProvider` abstraction supports
local protected storage and future vault/cloud providers behind the same authority boundary.

Required production secrets are stable and supplied through `SecretProvider`, protected environment
injection, or approved operating-system storage. Production startup or the affected operation fails
closed when a required secret is absent; it never silently generates a replacement or falls back to
an unapproved provider. Development bootstrap is explicit and development-only.

Secret metadata may include stable reference, purpose/provider scope, owner, creation/rotation/expiry,
availability, and audit facts. Secret values are never written to ordinary SQLite fields, manifests,
LLM prompts/responses, retrieval memory, training artifacts, exports, logs, traces, or error responses.

## Provider and connector configuration

Non-secret Local LLM configuration may include endpoint/runtime, provider/model/adapter registry
references, context/resource limits, timeout, structured-output/tool capabilities, health, and
fallback policy. Remote LLM configuration may include provider/model/endpoint/region, credential
reference, token/size/timeout limits, data policy, retention/training behavior, and fallback policy.

Evidence-source/connector configuration may include registered identity/version, approved source and
destination classes, scopes, endpoint/region, credential reference, query/payload limits, rate limits,
license/terms, data classification, retention, health, and policy owner. Configuration never implies
availability, approval, evidence accuracy, or runtime implementation.

Provider fallback is explicit, policy-compatible, schema-compatible, and audit-recorded. It cannot
expand evidence access, payload sensitivity, retention, license rights, or remote permission. A
blocked/unavailable credential or provider produces safe failure rather than ungoverned fallback.

## Local model and model-weight configuration

Local model configuration references exact EngineRegistry/Runtime Inventory records and independent
dependency, base-model-weight, tokenizer, adapter, and bundled-resource license decisions. It also
records checksum/source, compatibility, security/isolation, resources, evaluation/Trust, and approved
uses. Presence on disk is not installation approval or license approval.

Download/update permission is separately governed from inference permission. No download is performed
by F2-F, and no later implementation may download or update a model merely because Local LLM mode or
a feature flag is enabled.

## Feature flags

Representative non-authoritative flags may include `local_llm_enabled`, `remote_llm_enabled`,
`synthetic_data_enabled`, `optimization_enabled`, `causal_engine_enabled`, and
`experimental_retrieval_enabled`. Flags only narrow an otherwise eligible path; they never bypass
capability, permission, consent, privacy, outbound, security, provider, license, Trust, or resource
gates.

## Artifact provenance and reproducibility

Outbound results, retrieved evidence, memory items, training snapshots, and adapted-model artifacts
retain source provenance, privacy classification, effective policy/consent, evidence and model-weight
licenses, configuration/schema/tool/provider versions, validation/evaluation, and audit lineage.
Reproduction resolves non-secret configuration and secret-reference availability without capturing
the original secret value.

## Deferred implementation detail

Exact policy/configuration schemas, connector/provider registries, protected-secret backend,
rotation, discovery/health probes, network sandbox, download manager, APIs, and UI require later
contract freezes and accepted milestones.
