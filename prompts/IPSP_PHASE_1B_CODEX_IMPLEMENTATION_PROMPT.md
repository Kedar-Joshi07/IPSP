# IPSP v1.0 — Phase 1B Codex Implementation Prompt
## Configuration, SecretProvider, Feature Flags & Outbound Policy

You are implementing IPSP v1.0 in the existing repository.

**Authoritative repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** commit `9374b2ea34f6160d0f5586f088a8943f8b2d3721` or a direct descendant containing no unreviewed Phase 1B work.

Current gate state:
- Phase 0: COMPLETE
- Phase 0.5: PASS
- Documentation Freeze: PASS
- Phase 1A: PASS
- Phase 1A.1: PASS
- Phase 1B: AUTHORIZED
- Current app version remains `v0.1.0`

This task is **Phase 1B only**.

---

# 1. Governing rule

The frozen repository documentation is the implementation authority.

Do not redesign IPSP.

Do not introduce a second configuration system, secret store, outbound-policy path, feature-flag system, provider registry, route hierarchy, or error taxonomy.

If an implementation choice requires a technology or architectural decision that is not resolved by the frozen specifications, stop and report it rather than silently choosing a new architecture.

Preserve all Phase 1A/1A.1 hardening, especially:
- client-safe error sanitization;
- recursive structured-log redaction;
- explicit LogRecord field allowlisting;
- correct request success/failure status;
- request/trace propagation;
- offline/no-CDN behavior;
- canonical FastAPI route ownership.

---

# 2. Required reading before editing

Read the current repository state first.

Read completely:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_PROJECT_STRUCTURE.md`
6. `docs/16_LLM_ARCHITECTURE.md`
7. `docs/17_PRIVACY_REMOTE_LLM_POLICY.md`
8. `docs/18_SECURITY_RBAC_SPEC.md`
9. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
10. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
11. `docs/23_ERROR_HANDLING_SPEC.md`
12. `docs/28_REST_API_CONTRACT.md`
13. `docs/29_TEST_STRATEGY.md`
14. `docs/30_ACCEPTANCE_CRITERIA.md`
15. `docs/31_IMPLEMENTATION_PROGRESS.md`
16. `docs/32_DECISION_LOG.md`
17. `docs/34_CODING_STANDARDS.md`
18. `docs/35_CONFIGURATION_SPEC.md`
19. `docs/40_ANTI_CONTAMINATION.md`
20. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Then inspect the current implementation, especially:

- `backend/ipsp/config/`
- `backend/ipsp/security/`
- `backend/ipsp/errors/`
- `backend/ipsp/observability/`
- `backend/ipsp/main.py`
- `.env.example`
- `pyproject.toml`
- `requirements.lock`
- relevant current tests

Before editing, run:

```text
git status --short
git rev-parse HEAD
```

If the worktree contains unrelated user changes, preserve them and do not overwrite them.

---

# 3. Phase 1B objective

Implement the **configuration/security policy foundation** required by later authentication, LLM, ingestion, model-download and Admin configuration phases.

Phase 1B must establish:

1. a clean typed configuration model;
2. a first-class feature-flag model;
3. a `SecretProvider` abstraction;
4. a production-usable environment-injected secret provider;
5. safe secret references/value handling;
6. backend-enforced outbound policy evaluation;
7. remote-transmission policy levels from the frozen privacy specification;
8. provider allowlisting;
9. explicit policy denial behavior;
10. composition/provider-registry wiring for the Phase 1B services;
11. safe configuration documentation and `.env.example`;
12. meaningful unit/integration/security tests;
13. Phase 1B progress evidence.

The foundation must remain local-first and deny outbound behavior by default.

---

# 4. Explicitly DO NOT implement in Phase 1B

Do NOT implement:

- SQLite/SQLAlchemy models;
- Alembic migrations beyond the existing placeholder;
- persisted provider/configuration records;
- Admin configuration API routes;
- Admin configuration UI;
- users/roles/permissions;
- login/logout/session cookies;
- CSRF;
- password hashing;
- RBAC;
- audit-event persistence;
- actual remote LLM providers;
- actual local LLM providers;
- HTTP clients for remote providers;
- network calls;
- model downloads;
- update-check calls;
- dataset uploads;
- data classification engine;
- column masking engine;
- semantic analysis;
- ML;
- simulation;
- Redis/Celery;
- vault/cloud secret backends;
- automatic operating-system keychain technology selection.

Do not add `keyring`, Vault clients, cloud secret-manager SDKs, or similar dependencies unless a frozen specification explicitly selects them. It currently does not.

Environment injection is an explicitly allowed production secret source and is sufficient for this Phase 1B implementation.

No fake network requests.

No demo API keys.

No real secret values.

---

# 5. Configuration architecture

The current Phase 1A `Settings` object is the starting point.

Refactor/extend it without introducing scattered environment lookups.

The target must keep these concerns distinct:

## 5.1 Runtime/application settings

Examples already implemented:
- environment;
- app name/version;
- debug;
- host/port;
- log level;
- data/artifact/log/frontend paths;
- theme.

Keep these typed.

## 5.2 Feature flags

Implement a typed feature-flag contract for the frozen examples:

- `local_llm_enabled`
- `remote_llm_enabled`
- `sdv_enabled`
- `optimization_enabled`
- `causal_engine_enabled`
- `experimental_rag_enabled`

All default to the safe/off state unless a frozen spec says otherwise.

Feature flags mean **the application feature is enabled/available**.

They are not authorization.

They are not outbound permission.

They are not evidence that a dataset supports a capability.

Do not confuse platform feature flags with IPSP capability discovery.

## 5.3 Outbound settings

Implement typed policy configuration for:

- global Internet enabled/disabled;
- remote LLM outbound enabled/disabled;
- allowed remote provider identifiers;
- model download permission;
- update-check permission;
- default remote-transmission policy.

The policy defaults must be deny/off.

Keep outbound settings separate from feature flags.

For example, it must be possible for:

```text
feature.remote_llm_enabled = true
outbound.remote_llm_enabled = false
```

and the effective result is **remote calls denied**.

Do not silently merge those meanings into one Boolean.

## 5.4 Environment-variable shape

Use the existing Pydantic Settings foundation.

A nested typed configuration model is preferred if it remains clear and testable.

If nested models are used, configure an explicit environment nested delimiter and update `.env.example` and README/config documentation accordingly.

Do not preserve obsolete environment variables merely by creating duplicate source-of-truth fields.

If Phase 1A environment names are intentionally migrated, do it once, document the migration, and test the canonical names.

No real `.env` is committed.

---

# 6. SecretProvider foundation

Implement a provider abstraction suitable for later environment, protected-OS, vault and cloud implementations.

A reasonable conceptual shape is:

```python
class SecretProvider(Protocol):
    def get(self, ref: SecretRef) -> SecretValue | None: ...
    def require(self, ref: SecretRef) -> SecretValue: ...
```

Exact naming may differ if the frozen structure or current code suggests a better cohesive design.

## 6.1 SecretRef

Implement a validated non-secret reference/value object.

It should identify:
- provider kind/name;
- secret key/reference identifier.

The reference is metadata, not the secret value.

It must be safe to persist later in SQLite as provider configuration metadata.

Do not persist actual secret values.

## 6.2 SecretValue

Prefer a wrapper rather than passing raw secret strings through configuration/service objects.

Requirements:
- `repr()` must never expose the secret;
- `str()` must never expose the secret;
- equality/debug output must not accidentally print plaintext;
- revealing the value must require an explicit method/property intended for the code path that needs it;
- the wrapper must not be JSON serializable into plaintext accidentally through ordinary Pydantic/model dumping.

Keep the design simple.

Do not create cryptography theater: the secret will necessarily exist in process memory when used.

The goal is preventing accidental logging/config serialization/persistence, not claiming memory encryption.

## 6.3 EnvironmentSecretProvider

Implement a concrete environment-backed provider.

Requirements:
- reads only the specifically requested environment variable/reference;
- no broad environment dump;
- missing optional secret returns `None`;
- missing required secret fails closed with a safe typed IPSP/domain exception;
- no plaintext value appears in exception messages/details/logs;
- no secret is copied into normal Settings fields;
- secret names/references may be retained as metadata if safe.

Environment injection is valid for production according to the frozen configuration policy.

## 6.4 Test-only provider

A small in-memory provider may exist under tests or as an explicitly test-focused implementation if useful.

Do not make an insecure in-memory provider the production default.

## 6.5 OS/vault/cloud providers

Do not choose or install an OS keychain/vault/cloud SDK in this phase.

The interface must allow such providers later without changing callers.

---

# 7. Outbound policy foundation

Implement backend-enforced policy evaluation.

UI state must never be the enforcement mechanism.

Create clear typed concepts for:

- outbound action/purpose;
- provider identifier where relevant;
- requested remote-transmission level;
- dataset classification/context where relevant;
- policy decision;
- denial reason/code.

The policy service must be usable by future LLM providers, model downloaders, update checks and other external-call components.

## 7.1 Remote-transmission policy levels

Preserve the frozen privacy policy:

1. Remote disabled
2. Sanitized schema only
3. Original column names but no values
4. Sanitized aggregate statistics/anonymized examples
5. Explicitly approved sample rows

Use explicit enum/value-object names.

Do not invent a sixth level.

Do not collapse these into a simple raw-data yes/no flag.

## 7.2 Dataset classifications relevant to policy

Provide policy vocabulary for the frozen classifications at minimum:

- ordinary business data;
- direct identifier;
- quasi-identifier;
- financial/sensitive;
- sensitive demographic;
- confidential/restricted.

This phase implements the **policy vocabulary and evaluation input**, not automatic classification.

Do not implement column classification/profiling yet.

## 7.3 Required policy rules

At minimum:

- global Internet OFF → every Internet-dependent action denied;
- remote LLM outbound OFF → remote LLM action denied;
- model-download permission OFF → model download denied;
- update-check permission OFF → update check denied;
- provider not in the configured allowlist → provider-specific remote action denied;
- requested transmission level above the allowed/default policy → denied;
- raw dataset rows are never treated as remotely allowed by default;
- confidential/restricted dataset context defaults to local-only/remote-disabled unless an explicit higher policy input is supplied by a future authorized Admin workflow;
- feature flags cannot override outbound denial.

The system must default deny when policy context is insufficient for a sensitive remote transmission.

## 7.4 Policy API design

Prefer a side-effect-free evaluation API such as:

```python
decision = outbound_policy.evaluate(request)
```

and a convenience enforcement method such as:

```python
outbound_policy.require_allowed(request)
```

where denial raises a typed IPSP/domain exception with a safe `SYS-*` or other existing taxonomy-compatible code.

Do not raise FastAPI `HTTPException` in policy/domain code.

Do not perform the network request inside the policy service.

A positive decision is permission to proceed to a future outbound adapter; it is not execution.

---

# 8. Provider/composition registry

The frozen implementation plan defines a provider/composition layer.

Implement only what Phase 1B needs.

It should be possible for application composition to obtain:

- the configured `SecretProvider`;
- the configured outbound policy;
- the feature-flag/configuration object.

Do not implement actual `SemanticLLMProvider` selection yet.

Do not create a service locator used everywhere.

Prefer explicit dependency construction/injection.

Avoid mutable global provider singletons.

`create_app()` may place immutable/configured foundation services on application state if that matches the existing Phase 1A composition approach, but keep domain modules independently testable.

---

# 9. Production fail-closed behavior

The frozen rule is:

> Required production secrets have no generated startup defaults.

Apply it precisely.

Important: Phase 1B does not yet have to invent an application/session secret merely so startup can fail.

If no current implemented feature genuinely requires a secret, production startup may remain secret-free.

However:
- `SecretProvider.require()` must fail closed;
- future components must have a clear mechanism to declare/validate required refs;
- no code may silently create random replacement secrets;
- no fallback plaintext credential may be committed.

Do not introduce `secret_key="development-secret"` or similar.

---

# 10. Safe configuration representation

Configuration and service objects must not leak secrets through:

- `repr`;
- model dump;
- JSON;
- structured logs;
- exception details;
- README examples;
- `.env.example`.

Add tests proving this.

Secret **references** may appear in safe configuration snapshots; secret **values** may not.

Do not log the process environment.

---

# 11. Readiness integration

Phase 1A readiness currently reports future dependencies honestly.

Phase 1B may extend readiness only for **implemented configuration/policy initialization**.

Do not report remote providers as healthy.

Do not call the Internet from readiness.

If no outbound provider is configured, that is not a readiness failure for the local-first application.

A denied outbound policy is a valid operational state, not an unhealthy process.

---

# 12. Errors and observability

Reuse the current central `IPSPError` infrastructure.

Add only the minimum typed errors required by this phase, using the established error-code taxonomy.

Examples of concerns:
- required secret missing;
- outbound policy denied;
- invalid provider reference/policy configuration.

Do not expose:
- secret values;
- credential-bearing headers;
- raw environment values.

Use current recursive redaction.

Policy evaluation may emit safe structured diagnostic logs if useful, but:
- never log actual secrets;
- do not log raw dataset values;
- do not log every pure evaluation if that creates noise;
- security-critical policy changes are future durable audit events once persistence/Admin flows exist.

Do not implement audit persistence now.

Remember the known Phase 1G item: safe internal stack diagnostics are intentionally deferred to Phase 1G. Do not expand that scope here.

---

# 13. Dependencies

Avoid adding a new runtime dependency unless genuinely necessary.

Pydantic/Pydantic Settings and the Python standard library should be sufficient for the expected Phase 1B foundation.

If a new dependency is proposed:
- explain why the standard library/current dependencies cannot meet the need;
- verify it is maintained and compatible;
- add it to `pyproject.toml`;
- refresh `requirements.lock` reproducibly;
- test from a clean environment.

Do not add:
- keyring;
- cryptography merely to encrypt env values;
- Vault/cloud SDKs;
- requests/httpx for actual outbound calls;
- feature-flag SaaS SDKs.

---

# 14. Expected source areas

Use the frozen structure as authority.

Likely cohesive areas include:

```text
backend/ipsp/config/
    settings.py
    feature_flags.py
    providers.py

backend/ipsp/security/
    secrets.py
    outbound.py
    redaction.py

tests/unit/
tests/integration/
tests/security/   # if appropriate
```

This is illustrative, not mandatory.

Do not create duplicate package ownership.

Do not move Phase 1A code merely for cosmetic reorganization.

---

# 15. Required tests

Add meaningful tests.

At minimum test:

## Configuration
- default configuration is offline/deny-by-default;
- feature flags default off;
- canonical environment variables populate nested/typed settings correctly;
- malformed provider/policy/transmission values are rejected;
- remote feature enabled does not automatically enable outbound access;
- configuration serialization contains no secret values.

## SecretProvider
- optional missing secret returns `None`;
- required missing secret raises a safe IPSP/domain error;
- existing env secret resolves correctly;
- `SecretValue.__repr__` does not reveal plaintext;
- `SecretValue.__str__` does not reveal plaintext;
- normal serialization/logging does not expose plaintext;
- exceptions never contain resolved secret plaintext;
- provider does not dump unrelated environment variables.

## Outbound policy
- global Internet off denies remote LLM;
- global Internet off denies model download;
- global Internet off denies update check;
- remote LLM outbound off denies remote LLM;
- model-download off denies model download;
- update-check off denies update check;
- unapproved provider is denied;
- approved provider can pass when every required policy layer allows it;
- each transmission level obeys ordering/allowed maximum;
- restricted classification defaults to local-only;
- explicit approved-row transmission cannot occur from default policy;
- feature flag cannot bypass policy;
- insufficient sensitive transmission context fails closed;
- `require_allowed()` raises a safe domain exception without FastAPI coupling.

## Regression
All existing Phase 1A/1A.1 tests must still pass.

Architecture scans must still prove:
- no Streamlit;
- no benchmark/domain contamination;
- no `Session.query()`;
- no runtime CDN;
- no JWT/python-jose browser auth;
- no fake campaign/demo outputs;
- no actual outbound HTTP/network implementation.

---

# 16. Security-focused negative tests

Include negative tests attempting to leak a known marker such as:

```text
DO_NOT_LEAK_PHASE1B_SECRET
```

through:
- `repr(SecretValue)`;
- `str(SecretValue)`;
- configuration representation/dump;
- IPSP error response details where applicable;
- structured metadata sanitization;
- policy denial error;
- logs produced during missing/denied operations.

The marker must not appear.

Do not use a real credential.

---

# 17. Quality gates

Run at minimum:

```text
python -m compileall -q backend tests
pytest
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
```

Run the architecture/conformance tests/scans.

If dependencies change, repeat the clean Python 3.12 lock verification performed in Phase 1A.1.

If dependencies do not change, do not regenerate the lock merely to change timestamps/comments.

Do not claim tests passed unless they actually ran.

---

# 18. Documentation updates

After all gates pass:

Update:
- `.env.example`
- relevant config README/root README only where needed;
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Record:

`Phase 1B — Configuration, SecretProvider, Feature Flags & Outbound Policy`

Do not mark full Phase 1/v0.1.0 complete.

Update `docs/32_DECISION_LOG.md` only if an actual new architecture decision was unavoidable.

Do not rewrite frozen specs to make code drift appear compliant.

If implementation reveals a spec contradiction, stop and report it.

---

# 19. Git discipline

Before editing:

```text
git status --short
git rev-parse HEAD
```

After implementation:

```text
git status --short
git diff --stat
git diff --check
```

Do not automatically commit or push unless the user explicitly asks Codex to do so.

Do not delete unrelated files.

Do not add ZIP archives, caches, virtual environments, local databases, logs, or runtime secrets.

Generated artifacts must remain ignored.

---

# 20. Phase 1B acceptance gate

Phase 1B is PASS only if all of the following are true:

- typed configuration remains the sole environment/config source;
- platform feature flags exist and default safely;
- feature flags and outbound permissions are distinct;
- SecretProvider abstraction exists;
- environment-backed secret provider works;
- secret values have safe representation/serialization boundaries;
- required secret lookup fails closed;
- no plaintext secret is persisted or logged;
- outbound policy is backend-enforced and side-effect free;
- Internet/remote-LLM/model-download/update-check policies default deny;
- provider allowlisting is enforced;
- all five frozen remote-transmission levels are represented and enforced;
- restricted datasets default local-only in policy evaluation;
- raw rows are never remotely allowed by default;
- no actual network implementation was added;
- no database/auth/RBAC functionality was prematurely added;
- existing 1A/1A.1 functionality still passes;
- tests, lint, formatting and type checking pass;
- anti-contamination scans pass;
- progress documentation is accurate.

---

# 21. Mandatory final response

Return all of the following.

## A. Starting state
- starting commit SHA;
- branch;
- initial `git status --short`.

## B. Files created
List every created file.

## C. Files modified
List every modified file.

## D. Implementation summary
Explain:
- typed configuration structure;
- feature flag structure;
- secret-provider architecture;
- outbound-policy architecture;
- composition/wiring.

## E. Security behavior
Explain:
- fail-closed secret handling;
- secret representation protection;
- outbound default-deny rules;
- remote-transmission enforcement.

## F. Dependencies
For every added/changed direct dependency, explain why.
If none changed, say so explicitly.

## G. Tests
Give exact:
- tests passed;
- failed;
- skipped;
- warnings.

## H. Quality gates
Report:
- compileall;
- Ruff lint;
- Ruff format;
- mypy;
- pip check;
- git diff check.

## I. Security negative-test evidence
Report whether the test secret marker appeared anywhere it should not.

## J. Architecture/conformance
Explicitly report:
- benchmark/business contamination;
- Streamlit;
- `Session.query()`;
- runtime CDN;
- JWT/python-jose;
- actual outbound/network calls;
- premature Phase 1C+ functionality.

## K. Git state
Show:
- final `git status --short`;
- `git diff --stat`.

## L. Deviations / unresolved issues
If none, say `None`.

If OS-protected secret storage was not implemented because no technology is frozen, state that clearly as an intentional future provider extension, **not a Phase 1B failure**, because environment injection is an approved production secret source.

## M. Gate result

End exactly with one of:

`Phase 1B: PASS — ready for independent review before Phase 1C`

or

`Phase 1B: FAIL — Phase 1C blocked`

Do not begin Phase 1C.
