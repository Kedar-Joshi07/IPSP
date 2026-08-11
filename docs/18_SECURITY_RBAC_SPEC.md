# Security & RBAC Specification

## Roles
Expose `Admin` and `User` in v1.0 while implementing role-to-permission mapping.

`User.role_id → Role → RolePermission → Permission` is the sole authorization authority. V1.0 uses one role per user. Do not persist or authorize from an independent `is_admin` field; an API convenience value, if needed, is computed from the resolved role/permissions only.

### Permission examples
`simulation.run`, `simulation.export`, `dataset.view`, `dataset.upload`, `dataset.configure`, `dataset.assign`, `model.train`, `model.promote`, `llm.configure`, `internet.configure`, `user.manage`, `logs.view`, `system.configure`.

## Dataset permissions
Per-user/project dataset access may include `can_view`, `can_simulate`, `can_export_results`, `can_export_data`.

## Passwords
Use Argon2id through maintained `pwdlib[argon2]`. Never store plaintext passwords. Do not add a bcrypt fallback unless legacy-hash migration becomes an explicit requirement. A pepper, if used, must be stable and live outside SQLite/source control.

## User record

The minimum user fields are `id`, unique `username`, `display_name`, nullable `email`, `password_hash`, `role_id`, `is_active`, `must_change_password`, `failed_login_count`, `locked_until`, `last_login_at`, `password_changed_at`, `created_at`, `created_by`, and `updated_at`. Timestamps are timezone-aware UTC. There is no persisted `is_admin`.

## Session security
Use server-side sessions with cryptographically random opaque bearer tokens. Issue a new token after every successful login and store only its cryptographic hash when practical. Rotate or invalidate sessions after password changes and role/privilege changes; enforce explicit expiry and logout invalidation. Never log the raw bearer token.

Cookies are HttpOnly and Secure under HTTPS/production. Localhost development behavior must be explicit and must not weaken production defaults. Apply a suitable SameSite policy plus CSRF validation for POST/PUT/PATCH/DELETE browser requests. Failed authentication is throttled and can trigger temporary lockout. Session timestamps are timezone-aware UTC.

## Bootstrap admin
Prefer a CLI bootstrap such as `scripts/create_admin.py`; first-run UI setup must permanently close after successful initialization if used.
