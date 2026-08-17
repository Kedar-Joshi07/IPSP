# Security & RBAC Specification

## Status and boundary

The accepted v0.1.0 authentication, session, role, permission, and foundation-resource controls
remain current. The F-002 license, evidence, provider, learning, and later-resource controls below are
target contracts and are not implemented by F2-G.

## Roles and permission authority

Expose `Admin` and `User` in v1.0 while implementing role-to-permission mapping.

`User.role_id → Role → RolePermission → Permission` is the positive role authorization authority.
V1.0 uses one role per user. Do not persist or authorize from an independent `is_admin` field; an API
convenience value, if needed, is computed from resolved role/permissions only.

Representative permission ownership may include `simulation.run`, `simulation.export`,
`dataset.view`, `dataset.upload`, `dataset.configure`, `dataset.assign`, `model.train`,
`model.promote`, `llm.configure`, `internet.configure`, `evidence.configure`, `license.review`,
`learning.review`, `user.manage`, `logs.view`, and `system.configure`. These names do not claim that
all permissions or resources exist in v0.1.1.

## Project, dataset, and data policy

Per-user/project dataset access may include `can_view`, `can_simulate`, `can_export_results`, and
`can_export_data`. Dataset, table, row/population, column, semantic, evidence, and artifact policy may
further limit an action by purpose and data classification.

Role permission is necessary but not sufficient for a governed resource action. Project/dataset
membership, resource ownership, column/data policy, purpose, privacy, license, evidence access,
learning eligibility, provider eligibility, and runtime consent may narrow permission; none can grant
an action absent from the resolved role.

## Consent, evidence, and outbound authorization

Effective outbound evidence or remote-provider permission is exactly:

```text
Admin policy ∩ project/dataset policy ∩ runtime user consent
```

Missing, ambiguous, expired, withdrawn, or denied policy/consent fails closed. Runtime consent is
scoped, purpose-bound, disclosed, time-bound/versioned, and audited. UI state, an LLM request, stored
credential, previously successful job, or configured provider is never authorization.

Evidence access remains one of `OFF`, `INTERNAL_ONLY`, `PUBLIC_WEB`, or `APPROVED_CONNECTORS`.
Access mode and LLM mode are independent. PUBLIC_WEB, connectors, and Remote/Hybrid LLM are planned,
not current v0.1.1 services.

## License, provider, and learning governance

- Engine, dependency, model-weight/adapter, solver, connector, dataset/evidence, and provider licenses
  pass the LicenseRegistry gate for the intended use. Only authorized reviewers may approve/change a
  decision; a role permission cannot waive `BLOCK`.
- Local and remote providers are independently gated by capability, security, privacy, outbound,
  resources, organization policy, license, and Trust. Local execution is not automatically safe;
  remote execution remains deny-by-default.
- Training-data inclusion requires a passed LearningEligibilityGate. Model/adapter evaluation and
  promotion require separate permissions and governed evidence. Training permission cannot promote
  a simulation, assumption, synthetic record, LLM proposal, or unverified evidence to observed truth.
- Authorization is rechecked when a queued job starts and before sensitive retrieval, transmission,
  artifact access, export, learning promotion, or provider fallback.

## Passwords

Use Argon2id through maintained `pwdlib[argon2]`. Never store plaintext passwords. Do not add a
bcrypt fallback unless legacy-hash migration becomes an explicit requirement. A pepper, if used,
must be stable and live outside SQLite/source control.

## User record

The minimum user fields are `id`, unique `username`, `display_name`, nullable `email`,
`password_hash`, `role_id`, `is_active`, `must_change_password`, `failed_login_count`, `locked_until`,
`last_login_at`, `password_changed_at`, `created_at`, `created_by`, and `updated_at`. Timestamps use
timezone-aware UTC. There is no persisted `is_admin`.

## Session security

Use server-side sessions with cryptographically random opaque bearer tokens. Issue a new token after
each successful login and store only its cryptographic hash when practical. Rotate or invalidate
sessions after password or role/privilege changes; enforce expiry and logout invalidation. Never log
the raw bearer token.

Cookies are HttpOnly and Secure under HTTPS/production. Localhost development behavior is explicit
and does not weaken production defaults. Apply a suitable SameSite policy plus CSRF validation for
POST/PUT/PATCH/DELETE browser requests. Failed authentication is throttled and may trigger temporary
lockout. Session timestamps use timezone-aware UTC.

## Bootstrap admin

Prefer a CLI bootstrap such as `scripts/create_admin.py`; first-run UI setup must permanently close
after successful initialization if used.

## Enforcement and safe failure

Checks occur server-side at API, service, repository/artifact, job-transition, provider/tool, export,
and promotion boundaries. Denials return safe codes/messages, trace IDs, and permitted remediation and
create audit events without leaking inaccessible metadata, secrets, policy internals, or stack traces.
