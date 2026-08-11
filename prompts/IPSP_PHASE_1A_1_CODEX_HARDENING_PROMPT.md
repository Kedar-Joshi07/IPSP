# IPSP v1.0 — Phase 1A.1 Independent Hardening Prompt

You are working in the existing IPSP repository after Phase 1A.

Phase 1A's broad implementation is approved, but independent source review found several foundation-level safety/observability issues that must be corrected **before Phase 1B begins**.

This is a narrow hardening pass. Do not implement Phase 1B functionality.

## Absolute rules

- Do not redesign IPSP.
- Do not add authentication, RBAC, database schema, SecretProvider, dataset ingestion, ML, LLM, simulation, or distributed job execution.
- Do not introduce benchmark/domain-specific logic.
- Modify only the Phase 1A foundation files/tests/docs required by the findings below.
- Run the full Phase 1A test/lint/format/type/conformance gates afterward.
- Do not start Phase 1B.

## Read first

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/34_CODING_STANDARDS.md`
- current Phase 1A backend/tests

## H-001 — Client-safe error details must be enforced

Current behavior allows `IPSPError.details` to contain an arbitrary mapping and the central FastAPI handler returns that mapping directly in the API response.

That means a future caller could accidentally expose values such as passwords, tokens, API keys, or other internal details even though the top-level message is safe.

### Required correction

Implement an explicit **client-safe details contract**.

Acceptable approaches include:
- rename/internalize the field as `safe_details` and sanitize it before response serialization; or
- keep the public field name `details` but enforce client-safe sanitization before it enters `ErrorResponse`.

Requirements:
- known secret-bearing keys must be redacted;
- nested mappings/lists must be handled recursively;
- unexpected object types must not expose unsafe representations unnecessarily;
- internal exception/stack details never enter the client envelope;
- the API response contract remains stable unless a frozen spec requires otherwise.

Add tests proving nested sensitive values cannot escape through `IPSPError` details.

Do not reuse a logging-specific helper if that creates undesirable coupling; shared sanitization may live in an appropriate neutral security/safety module if useful.

## H-002 — Strengthen structured-log redaction

Current `sanitize_metadata()` redacts only a small exact-key set.

Independent review demonstrated that keys such as:

- `access_token`
- `refresh_token`
- `client_secret`
- `secret_key`
- `x-api-key`
- `set-cookie`
- `proxy-authorization`

can currently pass through unredacted.

### Required correction

Strengthen secret-key detection in a deterministic, testable way.

At minimum recognize:
- password/password_hash and password-like suffixes;
- token/access_token/refresh_token/session_token and token-like suffixes;
- secret/client_secret/secret_key and secret-like suffixes;
- api_key/x-api-key and key forms used for credentials;
- authorization/proxy-authorization;
- cookie/set-cookie.

Requirements:
- case-insensitive;
- support underscore and hyphen header/key forms;
- recursive;
- do not redact ordinary unrelated business values merely because a substring happens to contain `key` or `token`;
- tests must cover nested structures and the examples above.

The system still follows the rule that developers must never intentionally interpolate secrets into free-form log messages. Add/retain documentation or code comments making that boundary explicit.

## H-003 — Request event status must reflect HTTP outcome

`RequestContextMiddleware` currently emits:

`ipsp_status = "success"`

for every completed response, including HTTP 4xx/5xx responses.

### Required correction

Set the structured request event status from the actual HTTP outcome.

Minimum:
- status codes below 400 -> `success`
- status codes 400 and above -> `failure`

Keep `status_code` in metadata.

Add integration/unit coverage for at least one successful response and one error response.

## H-004 — Preserve the optional observability envelope extension points

The frozen observability spec says the required core envelope is:

- timestamp_utc
- event_id
- trace_id
- request_id
- component
- action
- status
- severity
- sanitized metadata

and optional context fields should be included when supplied, such as:
- session_correlation_id
- user_id
- resolved role
- duration_ms
- error_code
- resource_type
- resource_id
- project/dataset/version/model/run references

Current formatter handles only duration and error code among these optional fields.

### Required correction

Make the formatter able to include approved optional IPSP context fields **when the LogRecord supplies them**, without inventing authentication/session data now.

Use an explicit allowlist of optional structured fields rather than serializing arbitrary LogRecord attributes.

Tests should verify:
- absent optional fields are omitted;
- supplied approved optional fields are emitted;
- sensitive metadata is still redacted.

Do not add user/session generation or auth behavior.

## H-005 — Verify generated build/cache artifacts remain untracked

The review ZIP contained:
- `backend/ipsp.egg-info/`
- multiple `__pycache__/` directories

The existing `.gitignore` appears to cover them, so this is probably packaging noise rather than a source defect.

Verify with Git that these artifacts are ignored and not tracked.

Do not commit:
- `*.egg-info/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`

If any are tracked, remove them from the Git index without deleting required source files.

## H-006 — Reconfirm the lock snapshot in a clean environment

Do not redesign dependency management.

Using the project's canonical Python runtime, create a fresh temporary virtual environment and verify:

1. `requirements.lock` installs successfully.
2. `pip check` passes.
3. the local package installs with `--no-deps`.
4. pytest, Ruff, formatting check and mypy pass from that clean environment.
5. direct dependency constraints in `pyproject.toml` are satisfied by the lock snapshot.

If the lock was intentionally generated on Python 3.12, state that clearly in the report. Do not claim the same exact transitive snapshot is cross-Python portable unless actually tested.

Do not update package versions merely because newer ones exist.

## Tests to add/update

At minimum add coverage for:

- client error details redact nested password/token/secret/API-key material;
- log metadata redacts `access_token`;
- log metadata redacts `refresh_token`;
- log metadata redacts `client_secret`;
- log metadata redacts `secret_key`;
- log metadata redacts `x-api-key`;
- log metadata redacts `set-cookie`;
- normal non-secret fields remain intact;
- request log status is `success` for 2xx;
- request log status is `failure` for 4xx/5xx;
- approved optional envelope fields are included when supplied;
- unknown arbitrary LogRecord extras are not automatically serialized.

## Documentation

Update `docs/31_IMPLEMENTATION_PROGRESS.md` only after the hardening gate passes.

Record this as:
`Phase 1A.1 — Foundation hardening`

Do not mark the overall v0.1.0 milestone complete.

Update `docs/32_DECISION_LOG.md` only if a genuine new architectural decision is required. These corrections should preferably implement already-frozen safety rules.

## Mandatory verification

Run:

- `python -m compileall -q backend tests`
- full pytest
- Ruff lint
- Ruff format check
- strict mypy
- `pip check`
- architecture/conformance scans
- `git diff --check`
- `git status --short`
- `git diff --stat`

Also verify no Phase 1B functionality was introduced.

## Final response

Report:

1. files created
2. files modified
3. exact corrections for H-001 through H-006
4. test counts
5. lint/format/type results
6. clean-environment lock verification
7. ignored/generated artifact verification
8. conformance scan results
9. git status/diff stat
10. unresolved issues

End exactly with one of:

`Phase 1A.1: PASS — Phase 1B ready for independent review`

or

`Phase 1A.1: FAIL — Phase 1B blocked`

Do not begin Phase 1B.
