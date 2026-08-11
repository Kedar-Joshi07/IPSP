# Configuration Specification

## Configuration domains
- App/runtime
- Database paths
- Storage roots/limits
- Auth/session/security
- Logging/retention
- Feature flags
- Local LLM
- Remote LLM
- Outbound policy
- Job worker
- Report generation
- Trust thresholds

## Principles
- Typed settings object.
- Environment-specific values are not committed as secrets.
- Required production secrets have no generated startup defaults; production fails closed when they are absent. Development bootstrap is explicit.
- Admin-editable settings are validated and audited.
- Security-critical policy changes create audit events.
- Provider credentials are secret references only.

## Dependency policy

Resolve current maintained compatible versions at implementation time. Declare direct dependencies in `pyproject.toml` and use a reproducible lock or constraints mechanism. Architecture documents do not freeze stale exact package pins. `sqlite3` is standard library; browser sessions do not require JWT/python-jose; new passwords use maintained `pwdlib[argon2]` without bcrypt fallback unless legacy migration is explicitly introduced.
