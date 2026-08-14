# Configuration Specification

## Status boundary

The accepted v0.1.0 foundation implements typed application, database, authentication/session,
logging, outbound, secret-reference, feature-flag, and local-job configuration. F-002 engine,
license, evidence, analytical, and modelling configuration described below is planned and must not be
advertised as current runtime inventory or installed capability.

## Configuration domains

- Application/runtime and environment mode.
- Database paths and migration state.
- Storage roots, limits, staging, artifacts, and retention.
- Authentication, session, CSRF, lockout, and security policy.
- Logging, audit, redaction, and retention.
- Feature flags and capability exposure.
- Local, remote, hybrid, and no-LLM modes.
- Outbound and evidence-access policy plus runtime-consent requirements.
- Job worker and resource limits.
- Report generation.
- Trust thresholds and validation policy.
- Engine/provider declarations and organization preference.
- Dependency, model-weight, solver/commercial, and evidence-license policy references.
- Runtime engine-inventory refresh/verification policy when implemented.

## Principles

- Configuration uses typed, schema-validated contracts with safe defaults.
- Environment-specific values and secrets are not committed.
- Required production secrets have no generated startup defaults; production fails closed when they
  are absent. Development bootstrap is explicit.
- Admin-editable settings are permission-checked, validated, versioned where reproducibility matters,
  and audited.
- Security, outbound, license, and provider-policy changes create audit events.
- Provider credentials remain SecretProvider references only.
- A configured provider is not necessarily installed, available, licensed, healthy, or eligible.
- Architecture-candidate lists never populate runtime facts.

## Engine and license policy

Organization engine/license mode is one of:

- `OPEN_SOURCE_ONLY`
- `OPEN_SOURCE_PREFERRED` — default
- `COMMERCIAL_ALLOWED`

Configuration may express provider enablement, preference, resource caps, allowed execution
location, feature flags, and references to reviewed license decisions. It cannot override semantic
capability validity, a LicenseRegistry `BLOCK`, security/outbound policy, Trust, or resource facts.

Dependency, model-weight, solver/commercial, dataset/evidence, and hosted-service permissions remain
separate decisions. Unknown or missing mandatory license/security facts fail closed.

## Runtime Engine Inventory boundary

Runtime inventory is discovered evidence, not editable configuration. Configuration may control
verification frequency, timeouts, approved probes, or cache lifetime; inventory records whether a
provider is actually installed, loadable, available, healthy, and resource-compatible, with safe
reason and provenance metadata.

Unknown, never-checked, not-installed, unavailable, disabled, and blocked remain distinct. Exact
inventory implementation is deferred to the owning milestone and
[Engine & License Registry Specification](48_ENGINE_LICENSE_REGISTRY_SPEC.md).

## Resource and security policy

Provider configuration declares bounded CPU, memory, disk, GPU/accelerator, concurrency, latency,
and execution-location policy where applicable. Remote transmission additionally requires Admin
policy ∩ project/dataset policy ∩ runtime user consent.

Configuration and diagnostics never expose plaintext credentials, auth cookies, raw dataset rows,
license keys, unsafe exception values, or unapproved provider probes.

## Dependency policy

Resolve maintained compatible versions at implementation time. Add a direct dependency only when an
authorized milestone approves its dependency/license contract. Declare it in `pyproject.toml` and
update the reproducible lock/constraints mechanism together; architecture documentation does not
freeze stale pins or imply installation.

`sqlite3` is standard library. Browser sessions do not require JWT/python-jose. New passwords use
maintained `pwdlib[argon2]` without bcrypt fallback unless a separately authorized legacy migration
is introduced.

F2-D adds no dependencies. DoWhy, EconML, CVXPY, OSQP, SCS, Synthcity, SDV, and all other F-002
candidates remain architecture options subject to later installation and license review.
