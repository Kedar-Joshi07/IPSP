# Implementation Progress

Specification baseline: **IPSP v1.0 frozen**  
Accepted application implementation: **Phase 1 / v0.1.0: FORMALLY ACCEPTED — independent final review PASS.**

Active reconciliation milestone: **v0.1.1: F-002 Architecture Reconciliation — IN PROGRESS.** F2-A
was independently accepted at SHA `2605325a357b372057bbf57fbab90be0f83ace1e`; F2-B was
independently accepted at SHA `1f2422f74a5a9f5c6b26a218db0ab68a026d561d`; F2-C was
independently accepted at SHA `262909194568f40e9ca384479dfbbca9ebb06e20`; F2-D capability,
engine, license, and modelling reconciliation was independently accepted at SHA
`1791041904d5531eb1fb2c7beb1969baf4853dee`; F2-E simulation, Composite/Cross-Domain, Finance,
Trust, Evidence, and reproducibility contract reconciliation was independently accepted at SHA
`697a55567919e13c3087b0334ef14d89a5220055`; F2-F governed learning, outcome reconciliation, LLM,
and evidence-access contract reconciliation was independently accepted at SHA
`81df9fedf84c7c02b837d5ca1509c81c34648fcd`; F2-G platform-contract reconciliation was
independently accepted at SHA `0c621a9f70d5568d36a13193f8f14b96c6bd79ff`; F2-H flows, tests,
acceptance, benchmark, governance, agent-instruction, and active-prompt reconciliation is complete
after review correction and pending independent re-review. No F-002 runtime capability is
implemented by these documentation work packages.

Following capability milestone: **v0.2.0: NOT STARTED.** F-002 architecture approval does not
authorize implementation start; the required v0.2 contract freeze has not started.

| Milestone | Target app version | Status | Gate |
|---|---|---|---|
| Specification & plan generation | — | PHASE 0 COMPLETE | 40+ numbered specs + implementation plan ready |
| Architecture reconciliation | — | **PHASE 0.5 PASS** | 24 audit/completeness items resolved; all 20 gates verified |
| Foundation/security/repo skeleton | v0.1.0 | **FORMALLY ACCEPTED — independent final review PASS** | Accepted foundation code SHA: `cd0dca48ded8d68f18e861f2427dfeb746d52ea7` |
| F-002 architecture/roadmap reconciliation | v0.1.1 | **IN PROGRESS — F2-H REVIEW CORRECTION COMPLETE, INDEPENDENT RE-REVIEW PENDING** | Initial F2-H implementation at `6852e5a2487197602a0a4a07b89cac4109ce6141`; F2-I remains blocked pending independent review of the corrected SHA |
| Ingestion/storage/provenance | v0.2.0 | **NOT STARTED** | Contract freeze not started; F-002 does not authorize implementation start |
| Deterministic data understanding & relationships | v0.3.0 | NOT STARTED | Milestone contracts not frozen |
| Semantic intelligence & Dataset Semantic Manifest | v0.4.0 | NOT STARTED | Milestone contracts not frozen |
| Metric & Formula Registry + Domain Experience foundation | v0.5.0 | NOT STARTED | Milestone contracts not frozen |
| Capability Discovery + Engine/License Registry | v0.6.0 | NOT STARTED | Milestone contracts not frozen |
| Core modelling + model lifecycle | v0.7.0 | NOT STARTED | Milestone contracts not frozen |
| Simulation core + universal scenario/execution contracts | v0.8.0 | NOT STARTED | Milestone contracts not frozen |
| Trust + Evidence + history + comparison | v0.9.0 | NOT STARTED | Milestone contracts not frozen |
| Cross-Domain Composite intelligence | v0.10.0 | NOT STARTED | Milestone contracts not frozen |
| Domain intelligence completion | v0.11.0 | NOT STARTED | Milestone contracts not frozen |
| Learning + Outcome Reconciliation foundation | v0.12.0 | NOT STARTED | Milestone contracts not frozen |
| Local AI | v0.13.0 | NOT STARTED | Milestone contracts not frozen |
| Full dynamic product UI | v0.14.0 | NOT STARTED | Milestone contracts not frozen |
| v1.0 release candidate / hardening | v0.15.0 | NOT STARTED | Milestone contracts not frozen |
| First General Availability release | v1.0.0 | TARGET — NOT RELEASED | Full v1.0 acceptance gate |

## F2-H — Flows / Tests / Acceptance / Benchmark / Governance / Agent Instructions

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** REVIEW CORRECTION COMPLETE (2026-08-18), awaiting independent re-review
- **Starting and accepted F2-G SHA:** `0c621a9f70d5568d36a13193f8f14b96c6bd79ff`
- **Initial F2-H implementation SHA:** `6852e5a2487197602a0a4a07b89cac4109ce6141`
- **Scope:** canonical F-002 lifecycle and authority flows; future test strategy; bounded-v1.0
  acceptance and explicit post-v1 deferrals; multi-domain/Cross-Domain benchmark strategy;
  milestone/workstream contract governance; repository and scoped agent instructions; revised
  v0.2.0–v1.0.0 prompt map; current-workstream state; active first-use, code-review, and testing
  prompt entry points; documentation completeness audit
- **Flow reconciliation:** flows 01, 06–09, 16, and 20 now express the applicable F-002 boundaries;
  new numbered flows 22–30 cover Domain Experience activation, Metric & Formula resolution,
  Engine/License resolution, Scenario Intent and exactly three bases, CompositeSimulationGraph,
  Cross-Domain reconciliation, Finance reconciliation/stress, SimulationLearningStore/
  OutcomeReconciliation, and Local AI memory/adaptation governance. Existing flow numbering and
  historical files were preserved.
- **Current/target boundary:** documentation/governance only; no F-002 runtime capability was
  implemented, and v0.2.0 remains NOT STARTED with contract freeze not started
- **Change boundary:** no production code, tests, migrations, schemas, dependencies, lockfiles, or
  feature flags changed
- **Review correction:** from SHA `6852e5a2487197602a0a4a07b89cac4109ce6141`, reconciled
  `prompts/FIRST_COPILOT_PROMPT.md`, `prompts/CODE_REVIEW_PROMPTS.md`, and
  `prompts/TESTING_PROMPTS.md` to the F-002 authority order, current gate, milestone-aware review,
  and testing boundaries; this progress record is the only other correction file
- **Cumulative changed-file scope:** 47 Markdown files relative to the accepted F2-G SHA; the review
  correction itself changes exactly four Markdown files
- **Documentation validation:** 47 changed Markdown files have balanced fences/tables and 45
  valid relative links; repository-wide validation resolved 202 relative links across 128 Markdown
  files; all 30 numbered flows contain one structurally valid Mermaid block and sequence 01–30 is
  complete; stale identity/provider/roadmap/basis/metric occurrences were classified, with retained
  occurrences limited to authoritative optional boundaries or clearly historical evidence/prompts
- **Quality evidence:** `git diff --check` PASS; compileall PASS; Ruff lint PASS; Ruff format check
  PASS for 95 files; strict mypy PASS for 67 source files; `pip check` PASS; architecture conformance
  13/13 PASS
- **Initial regression evidence:** complete suite PASS in split execution: 215/215 unaffected tests plus the
  unchanged timing-sensitive recovery test 1/1. The isolated recovery test first exceeded its
  hardcoded 10-second Windows child-exit deadline, then passed on a clean rerun with the previously
  documented above-normal test-process scheduling. No production or test change was made for this
  environment timing behavior.
- **Review-correction revalidation:** exact four-file documentation-only correction scope PASS;
  repository Markdown links/tables/fences PASS; Mermaid structural validation 30/30 PASS;
  `git diff --check`, compileall, Ruff lint, Ruff format for 95 files, strict mypy for 67 source
  files, and `pip check` PASS; architecture conformance 13/13 PASS; 215/215 unaffected regression
  tests PASS and the isolated Windows recovery test passed 1/1 on its first correction-run attempt
  with the documented above-normal test-process scheduling
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Independent re-review state:** REQUIRED on the corrected committed SHA
- **Next gate:** independent F2-H re-review; F2-I must not begin before PASS on the corrected SHA

## F2-G — UI / API / Storage / Jobs / Security / Configuration / Operations Reconciliation

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** ACCEPTED (2026-08-18) — independent review PASS
- **Accepted F2-G SHA:** `0c621a9f70d5568d36a13193f8f14b96c6bd79ff`
- **Starting and accepted F2-F SHA:** `81df9fedf84c7c02b837d5ca1509c81c34648fcd`
- **Scope:** IPSP target UI/navigation/five-step composition, conceptual SQLite homes and future API
  resource families, provider-neutral jobs, security/outbound/license/evidence/learning gates,
  provider-neutral configuration, observability/error/health/backup operations, and v0.2 ingestion/
  provenance compatibility
- **Current/target boundary:** documentation contracts only; no target page, API route, table,
  migration, job type/backend, provider, engine, probe, backup service, feature flag, or v0.2 runtime
  is implemented by F2-G
- **Change boundary:** documentation only; no production code, tests, migrations, schemas,
  dependencies, lockfiles, or production feature flags changed
- **Validation evidence:** `git diff --check` PASS; 12 relative Markdown links resolve; tables and
  fences PASS; no changed-file Mermaid block; exact fourteen-file documentation scope PASS; IPSP
  identity, frozen navigation and five simulation steps, manifest-driven/capability-driven UI,
  conceptual-only persistence homes and API resource families, current LocalJobBackend/synthetic-job
  boundaries, provider/license/evidence/consent/learning gates, provider-neutral configuration,
  target observability/error/health/backup representation, optional-service readiness boundary, and
  v0.2 provenance deferral verified; Ruff PASS; mypy 67 source files PASS; architecture conformance
  13/13 PASS; complete test coverage PASS in split execution (215/215 unaffected tests plus 1/1
  timing-sensitive recovery test). Two monolithic Windows runs reached the recovery test's hardcoded
  10-second child-exit deadline after the child emitted the expected `JOB-WORKER-INTERRUPTED` payload;
  the unchanged isolated test passed twice with above-normal test-process scheduling. No production
  or test change was made for this environment timing behavior.
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Gate outcome:** F2-H authorized from accepted F2-G SHA

## F2-F — Governed Learning / Outcome Reconciliation / LLM / Evidence Access Contract Freeze

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** ACCEPTED (2026-08-17) — independent review PASS
- **Accepted F2-F SHA:** `81df9fedf84c7c02b837d5ca1509c81c34648fcd`
- **Starting and accepted F2-E SHA:** `697a55567919e13c3087b0334ef14d89a5220055`
- **Scope:** SimulationLearningStore and empirical-data separation, evidence-authority tiers,
  OutcomeReconciliation and actual matching, LearningEligibilityGate, governed Training Dataset
  Builder, challenger/champion learning, exact LLM and evidence-access modes, Local AI registry/
  model-weight licensing, governed retrieval/memory and optional PEFT/LoRA boundaries
- **New specification:**
  [`51_SIMULATION_LEARNING_OUTCOME_RECONCILIATION_SPEC.md`](51_SIMULATION_LEARNING_OUTCOME_RECONCILIATION_SPEC.md)
- **Current/target boundary:** documentation contracts only; learning/reconciliation, LLM providers,
  evidence retrieval/connectors, model downloads, training/adaptation, and Internet access remain NOT
  IMPLEMENTED
- **Change boundary:** documentation only; no production code, tests, migrations, schemas,
  dependencies, or lockfiles changed
- **Validation evidence:** `git diff --check` PASS; 14 relative Markdown links resolve; tables and
  fences PASS; no changed-file Mermaid block; exact six-file documentation scope PASS; exact four
  LLM modes and four evidence-access modes, effective three-way permission intersection, six ordered
  evidence-authority tiers, SimulationLearningStore empirical separation, OutcomeReconciliation/
  actual matching, learning eligibility/training builder/leakage gates, all five explicit prohibited
  direct promotions, batch-default/River boundary, Local AI adaptation order, privacy/provenance and
  model-weight license metadata verified; Ruff PASS; mypy 67 source files PASS; architecture
  conformance 13/13 PASS; full unit/integration/security regression suite 216/216 PASS
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Gate outcome:** F2-G authorized from accepted F2-F SHA

## F2-E — Simulation / Composite / Finance / Trust / Evidence Contract Freeze

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** ACCEPTED (2026-08-17) — independent review PASS
- **Accepted F2-E SHA:** `697a55567919e13c3087b0334ef14d89a5220055`
- **Starting and accepted F2-D SHA:** `1791041904d5531eb1fb2c7beb1969baf4853dee`
- **Scope:** exact simulation bases, versioned ScenarioIntentManifest, CompositeSimulationGraph,
  Composite/Cross-Domain execution, Finance Domain Experience, expanded Trust, separate Evidence
  Profile, complete provenance/synthetic boundary, reproducibility, and result/export contracts
- **New specifications:**
  [`49_COMPOSITE_CROSS_DOMAIN_SIMULATION_SPEC.md`](49_COMPOSITE_CROSS_DOMAIN_SIMULATION_SPEC.md) and
  [`50_FINANCE_DOMAIN_EXPERIENCE_SPEC.md`](50_FINANCE_DOMAIN_EXPERIENCE_SPEC.md)
- **Current/target boundary:** documentation contracts only; simulation, Composite/Cross-Domain,
  Finance, Trust/Evidence, synthetic, history/reproduction, and export runtimes remain NOT IMPLEMENTED
- **Change boundary:** documentation only; no production code, tests, migrations, schemas,
  dependencies, or lockfiles changed
- **Validation evidence:** `git diff --check` PASS; 20 relative Markdown links resolve; tables and
  fences PASS; no changed-file Mermaid block; exact nine-file documentation scope PASS; exactly
  three canonical simulation bases, ScenarioIntentManifest fields/lifecycle, graph node/edge and
  reconciliation contracts, Finance capability families/schema-agnostic boundary, expanded Trust
  and separate Evidence Profile, all 12 provenance classes and synthetic metadata, and re-run/
  reproduce distinction verified; Ruff PASS; mypy 67 source files PASS; architecture conformance
  13/13 PASS; full unit/integration/security regression suite 216/216 PASS
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Gate outcome:** F2-F authorized from accepted F2-E SHA

## F2-D — Capability / Engine / License / Modelling Architecture Reconciliation

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** ACCEPTED (2026-08-14) — independent review PASS
- **Accepted F2-D SHA:** `1791041904d5531eb1fb2c7beb1969baf4853dee`
- **Starting and accepted F2-C SHA:** `262909194568f40e9ca384479dfbbca9ebb06e20`
- **Scope:** evidence-first Capability Discovery, baseline-first modelling, expanded model registry,
  EngineRegistry, LicenseRegistry, EngineResolver, Runtime Engine Inventory, organization policy,
  causal boundary, and optimization boundary
- **New specification:** [`48_ENGINE_LICENSE_REGISTRY_SPEC.md`](48_ENGINE_LICENSE_REGISTRY_SPEC.md)
- **Current/target boundary:** provider/library names are architecture candidates only; no package,
  model, solver, causal engine, or optimization runtime is installed or implemented by F2-D
- **Legacy SDV inventory:** compliant optional/license-gated wording remains in README, configuration,
  F-002, and the new registry; stale generic wording is assigned to F2-E (`docs/14`), F2-G
  (`docs/24`), and F2-H (`docs/00`, Copilot instructions, `flows/08`, and legacy phased prompts);
  the Phase 0 audit occurrence remains historical evidence
- **Change boundary:** documentation only; no production code, tests, migrations, schemas,
  dependencies, or lockfiles changed
- **Validation evidence:** `git diff --check` PASS; 17 relative Markdown links resolve; tables and
  fences PASS; no changed-file Mermaid block; exact eight-file scope PASS; seven license classes,
  three organization modes, three license-gate outcomes, seven ordered resolver gates, and six model
  lifecycle statuses verified; SDV inventory completed; architecture conformance 13/13 PASS; full
  unit/integration/security regression suite 216/216 PASS
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Gate outcome:** F2-E authorized from accepted F2-D SHA

## F2-C — Data / Semantics / Metric & Formula / Domain Experience Contract Freeze

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** ACCEPTED (2026-08-14) — independent review PASS
- **Accepted F2-C SHA:** `262909194568f40e9ca384479dfbbca9ebb06e20`
- **Starting and accepted F2-B SHA:** `1f2422f74a5a9f5c6b26a218db0ab68a026d561d`
- **Scope:** deterministic Data Intelligence Packet, Dataset Semantic Manifest, relationship/lineage
  reconciliation, Metric & Formula Registry, Domain Experience Pack/Registry, and
  CrossDomainSemanticGraph contracts
- **New specifications:** [`46_METRIC_FORMULA_REGISTRY_SPEC.md`](46_METRIC_FORMULA_REGISTRY_SPEC.md)
  and [`47_DOMAIN_EXPERIENCE_PACK_SPEC.md`](47_DOMAIN_EXPERIENCE_PACK_SPEC.md)
- **Anti-contamination boundary:** registered Domain Experience knowledge is allowed only behind
  versioned contracts; generic core and physical source schemas remain domain/benchmark agnostic
- **Change boundary:** documentation only; no production code, tests, migrations, schemas,
  dependencies, or lockfiles changed
- **Validation evidence:** `git diff --check` PASS; 11 relative Markdown links resolve; tables and
  fences PASS; no changed-file Mermaid block; exact nine-file scope PASS; fixed physical
  domain-column requirement scan PASS; architecture conformance 13/13 PASS; full
  unit/integration/security regression suite 216/216 PASS
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Gate outcome:** F2-D authorized from accepted F2-C SHA

## F2-B — Product / Core Architecture / Project Structure Reconciliation

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** ACCEPTED (2026-08-14) — independent review PASS
- **Accepted F2-B SHA:** `1f2422f74a5a9f5c6b26a218db0ab68a026d561d`
- **Starting and accepted F2-A SHA:** `2605325a357b372057bbf57fbab90be0f83ace1e`
- **Scope:** project definition, product requirements, layered architecture, provider-neutral planned
  structure, glossary, open questions, and high-level SQLite/API ownership vocabulary
- **Current/target boundary:** accepted v0.1.0 foundation behavior remains explicit; planned F-002
  capabilities are not described as implemented
- **Deferred detail:** exact schema/table and API/resource contracts remain assigned to F2-G and
  their owning capability milestones
- **Change boundary:** documentation only; no production code, tests, migrations, schemas,
  dependencies, or lockfiles changed
- **Validation evidence:** `git diff --check` PASS; 8/8 relative Markdown links resolve; Markdown
  tables and fences PASS; no changed-file Mermaid block; architecture conformance 13/13 PASS; full
  unit/integration/security regression suite 216/216 PASS
- **Following milestone:** v0.2.0 remains NOT STARTED
- **Gate outcome:** F2-C authorized from accepted F2-B SHA

## F2-A — Architecture Authority + Version / Development Roadmap Freeze

- **Application milestone:** v0.1.1 — F-002 Architecture Reconciliation
- **Status:** IN PROGRESS — F2-A authority/roadmap freeze
- **Work package:** ACCEPTED (2026-08-14) — independent review PASS
- **Accepted F2-A SHA:** `2605325a357b372057bbf57fbab90be0f83ace1e`
- **Milestone state:** v0.1.1 IN PROGRESS; not accepted by completion of this work package alone
- **Starting SHA:** `7fdfd1d97bc5d34ea29f2cb52e5c22bf2a7d5cfd`
- **Architecture authority:** [`44_F002_ARCHITECTURE_FREEZE.md`](44_F002_ARCHITECTURE_FREEZE.md)
- **Version and roadmap authority:**
  [`45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md`](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md)
- **Historical boundary:** Phase 1 / v0.1.0 remains formally accepted at foundation code SHA
  `cd0dca48ded8d68f18e861f2427dfeb746d52ea7`; its audit evidence below is unchanged
- **Change boundary:** documentation and agent-authority instructions only; no production code,
  tests, migrations, schemas, or dependencies changed
- **Following milestone:** v0.2.0 remains NOT STARTED; its contract freeze and implementation have
  not begun
- **Gate outcome:** F2-B authorized from accepted F2-A SHA

## Independent final review

- **Phase 1L.1 independent review:** PASS
- **Phase 1 / v0.1.0:** FORMALLY ACCEPTED — independent final review PASS
- **Accepted foundation code SHA:** `cd0dca48ded8d68f18e861f2427dfeb746d52ea7`
- **v0.2.0 ingestion/storage/provenance:** AUTHORIZED — NOT STARTED
- **Change boundary:** Subsequent governance and README commits contain documentation only and do
  not change the accepted production foundation.

The Phase 1L and Phase 1L.1 sections below preserve the status, failure, correction, and re-audit
evidence recorded at each historical audit point.

## Phase 1L.1 — Acceptance Reproducibility Hardening

- **Implementation Status:** COMPLETE (2026-08-13)
- **Gate Result:** PASS; v0.1.0 foundation ready for independent final acceptance, with v0.2 not
  started and still blocked pending that review
- **Starting SHA:** `d8c4db477f7d213516589658435be142a9dc9e89`
- **Original Blocker:** Phase 1L correctly failed when the blocked-worker subprocess exceeded one
  aggregate `communicate(timeout=10)` deadline even though its complete lifecycle file subsequently
  passed. No production defect had been confirmed
- **Protocol Diagnosis:** The aggregate deadline combined Python startup, imports, service
  construction, SQLite access, worker scheduling, handler start, bounded backend shutdown, normal
  database disposal, and interpreter exit. It therefore did not isolate whether an abandoned daemon
  worker could hold the process after cleanup
- **Harness Correction:** The child now emits a flushed `normal_cleanup_complete` JSON marker only
  after shutdown, persisted snapshot read, and database disposal. The parent permits 30 seconds for
  setup/protocol completion, preserves the product assertion `backend.shutdown() < 0.5` seconds,
  then applies a dedicated 2-second process-exit bound. Daemon pipe readers prevent blocking reads;
  both subprocesses and their pipes are killed/reaped/closed in failure-safe cleanup
- **Targeted Stability:** Three separately invoked exact blocker tests passed: 1/1 in 16.75 seconds,
  1/1 in 9.35 seconds, and 1/1 in 9.54 seconds
- **Lifecycle / Full-Suite Evidence:** The complete lifecycle module passed 18/18 in 22.67 seconds.
  Planned full-suite run 1 passed 216/216 with zero failures/skips/warnings in 130.17 seconds; run 2
  passed 216/216 with zero failures/skips/warnings in 93.01 seconds
- **Focused / Security Evidence:** Phase 1K focused proof passed 3/3 in 3.14 seconds. Compileall,
  Ruff lint/format, strict mypy, current `pip check`, diff check, and all prior auth/session/CSRF/
  RBAC/redaction/outbound protections passed through the two complete suites
- **Dependency / Schema Evidence:** A disposable environment installed the exact lock and project
  `--no-deps`, imported IPSP, constructed Settings/application at `0.1.0`, and passed `pip check`
  before removal. Alembic heads/current/check passed at `20260812_05`; FK enforcement and exactly
  seven application/ORM tables were confirmed
- **Browser / Hygiene Evidence:** Isolated live QA passed Admin, permission-denial,
  required-password, themes, route freshness, desktop/390px overflow, same-origin assets, and zero
  application warnings/errors. The Uvicorn process, port 8767 listener, QA database/logs, browser
  tabs, and disposable environments were removed
- **Classification Correction:** Criterion 14 is `DEFERRED_BY_ROADMAP`; criterion 31 is `PASS`.
  Final totals are 15 PASS, 22 DEFERRED_BY_ROADMAP, 0 NOT_APPLICABLE, and 0 BLOCKED
- **Production / Schema / Dependency Changes:** None. Only the lifecycle regression harness and
  acceptance documentation changed; no architecture decision was added

Phase 1/v0.1.0 is accepted pending independent final review. The next planned milestone remains
v0.2.0 ingestion/storage/provenance, not started and blocked until that review accepts Phase 1L.1.

## Phase 1L — Final Phase 1 Acceptance Audit

- **Audit Status:** COMPLETE (2026-08-13)
- **Gate Result:** FAIL; v0.1.0 not accepted and v0.2 remains blocked
- **Audited SHA:** `33a5901c67c706290c5f05087555dc315eff4cf4`
- **Acceptance Blocker:** The mandatory 216-test suite produced 215 passes and one failure in
  `test_noncooperative_daemon_worker_cannot_hold_child_process_and_recovers`: its child process did
  not terminate within `communicate(timeout=10)`. The complete job lifecycle file then passed all
  18 tests independently, demonstrating a load-sensitive, non-reproducibly-green acceptance gate
- **Focused Evidence:** Both Phase 1K proof modules passed all 3 tests; the isolated job lifecycle
  module passed all 18 tests; compileall, Ruff lint/format, strict mypy, `pip check`, diff check,
  Alembic heads/current/check, exact seven-table/FK checks, static architecture/privacy sweeps, and
  live browser journeys passed their application assertions
- **Browser Evidence:** Admin, ordinary-user permission denial, and required-password journeys
  completed with local-only assets and no desktop overflow. Three Chrome extension message-channel
  closure errors were recorded as tooling noise rather than application exceptions
- **Production Defects / Changes:** No production defect was confirmed and no production source,
  API, schema, migration, dependency, frontend, or architecture change was made
- **Audit Artifact:** `docs/PHASE_1_ACCEPTANCE_REPORT.md` contains the complete Phase 1 matrix, all
  37 V1 criteria exactly once, evidence, constraints, blocker, and release recommendation
- **Documentation Result:** README remains unchanged because the gate failed. Phase 1/v0.1.0 stays
  in progress; no tag/release was created and v0.2 was not started

Phase 1 and v0.1.0 remain in progress. Phase 1L failed final acceptance; v0.2 is blocked.

## Phase 1K — Foundation Integration & Security Test Consolidation

- **Implementation Status:** COMPLETE (2026-08-13)
- **Gate Result:** PASS; ready for independent review before Phase 1L
- **Consolidated Proof Layer:** Two cohesive Phase 1K test modules add three isolated cross-layer
  regressions rather than duplicating focused subsystem tests. They join startup/migration/worker
  lifecycle; first-Admin bootstrap/auth/cookies/jobs/health/audit/runtime logs/outbound policy; and
  static-host containment/API/error/privacy boundaries
- **Fresh Lifecycle Evidence:** An absent isolated database leaves liveness and the frontend/API
  roots available, readiness safely returns `SYS-MIGRATION-REQUIRED`, and the worker does not start.
  At migration head `20260812_05`, readiness and all active dependencies are ready, analytical
  storage remains explicitly deferred, and two successive application lifespans start and stop the
  local daemon worker without a non-daemon worker leak
- **Integrated Security Evidence:** The canonical bootstrap creates one active Argon2id-backed
  Admin with all 13 permission mappings and a durable audit event; a second bootstrap is denied.
  Real HTTPS TestClients prove secure separated cookies, hash-only session persistence, explicit
  trace/request correlation, owner-hidden jobs, safe metadata/artifact handling, offline operation,
  deny-by-default outbound policy, server-side logout invalidation, and marker-free runtime logs
- **Static/Error Boundary Evidence:** A temporary frontend serves only its intended index/CSS/JS;
  API and health routes retain precedence; relative, encoded, slash, backslash, hidden-file,
  SQLite, and log-path attempts cannot expose parent markers. Readiness retains its minimal 503
  contract and central authentication errors retain the safe trace-correlated envelope
- **Browser Evidence:** Live same-origin in-app browser QA passed Admin login, Overview, Jobs,
  Profile, authorized System Health, light-theme selection, logout, an ordinary user's permission
  state, and a required-password user's blocked navigation and Sign out. Desktop and 390-pixel
  mobile layouts had no horizontal overflow; all page assets were same-origin; browser
  warnings/errors were zero
- **Prior-Phase Regression:** The full Phase 1A through Phase 1J.2 suite remains green, including
  cookie/session/CSRF/password/lockout/RBAC matrices, job cancel/retry/recovery and permanent-blocked
  worker proofs, observability correlation, health degradation, secret/outbound safety, frontend
  lifecycle guards, and architecture/anti-contamination scans
- **Test Evidence:** `pytest` — 216 passed, 0 failed, 0 skipped, 0 warnings in 125.09 seconds
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format passed for 95 files; strict
  mypy passed for 67 source files; `pip check` and `git diff --check` passed; isolated Alembic
  heads/current/check passed at `20260812_05`; exactly seven application ORM tables were present
- **Unchanged Contracts:** No production source, ORM table/model, migration, Python/npm dependency,
  API, authentication/session/CSRF/RBAC authority, job state, health contract, frontend asset, or
  architecture changed. Phase 1L and all later-domain implementation remain unstarted
- **Architecture Decisions Added:** None; Phase 1K verifies the frozen Phase 1 architecture

Phase 1 and v0.1.0 remain in progress. Phase 1L has not begun and remains blocked pending independent
review of Phase 1K.

## Phase 1J.2 — Authentication Transition Hardening

- **Implementation Status:** COMPLETE (2026-08-13)
- **Gate Result:** PASS; ready for independent review before Phase 1K
- **Canonical Auth Transition:** One application helper now navigates to the required authentication
  destination and refreshes through the canonical router only when the target hash is already
  active. Login/session-expiry redirection, local or server-confirmed logout, successful
  authentication, and successful password change all use this helper
- **Same-Hash Correctness:** A required-password identity at `#/login` continues to render the
  blocked password-change view. Sign out and successful password change clear local identity and
  force an actual Login render even when the URL already equals `#/login`
- **Password 401 Handling:** Password-change failures first reject stale or aborted route work, then
  pass HTTP 401 through the centralized session-expiry handler. Handled 401 responses clear local
  identity and render Login without adding a password-form error; ordinary validation/password 4xx
  errors remain safely on the form
- **Lifecycle Preservation:** The helper performs either hash navigation or one router refresh,
  never both. No direct route rendering was reintroduced, so Phase 1J.1 generation, abort, and
  exactly-once cleanup behavior remains authoritative
- **Regression Evidence:** Deterministic frontend contracts cover a required-password identity at an
  already-active Login hash, actual Login rendering after sign out and password-change success,
  centralized handling order for password-change 401, and absence of duplicate route rendering or
  cleanup. All prior Phase 1J.1 frontend/security contracts remain green
- **Test Evidence:** `pytest` — 213 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall, Ruff lint, Ruff format for 93 files, strict mypy for 67 source
  files, `pip check`, `git diff --check`, isolated Alembic upgrade/heads/current/check at
  `20260812_05`, and exactly seven ORM tables passed
- **Unchanged Contracts:** No schema, ORM model, migration, Python/npm dependency, backend API,
  authentication/session/CSRF authority, permission, frontend architecture, or Phase 1K behavior
  changed
- **Architecture Decisions Added:** None; this correction stays within the existing canonical
  router and centralized authentication boundaries

Phase 1 and v0.1.0 remain in progress. Phase 1K has not begun and remains blocked pending independent
review of Phase 1J.2.

## Phase 1J.1 — Frontend Lifecycle & State Hardening

- **Implementation Status:** COMPLETE (2026-08-13)
- **Gate Result:** PASS; ready for independent review before Phase 1K
- **Route Lifecycle:** The canonical hash router now owns an AbortController and monotonically
  increasing generation for every dispatch. A new route immediately aborts and invalidates the old
  route, invokes the active cleanup exactly once, and safely invokes a late cleanup returned by a
  stale pending route without installing it. Only the winning route may focus its heading
- **Cleanup Wiring:** Application rendering now returns Login, Jobs, Profile, required-password,
  Overview, System Health, and not-found cleanup values to the router. Login readiness/login
  callbacks detach safely; password forms reset and deactivate; Jobs closes only its owned dialogs;
  refresh uses the same router lifecycle; and the required-password same-route render shortcut was
  removed
- **Stale Result Suppression:** Async readiness, login, password, Jobs list/detail/mutation,
  Overview, and System Health requests receive the active route signal and check current-route
  authority before any post-await DOM, error, busy-state, navigation, title, or focus mutation.
  Deterministic source regressions verify abort-before-await and stale-generation rejection before
  cleanup installation
- **Theme Correction:** A stored preference remains authoritative over the configured initial
  default. `System` now always resolves through the operating-system media preference and continues
  responding to OS changes; configured dark/light defaults no longer override a stored `System`
  choice
- **Jobs Corrections:** Detail completion clears its busy ID before the final redraw. Cancel remains
  available for QUEUED jobs and for RUNNING jobs only before cancellation is requested. Retry is
  offered only for retryable FAILED/CANCELLED jobs whose attempt count remains below the maximum;
  mutation responses remain server-authoritative
- **Readiness Semantics:** The browser client validates minimal readiness documents and accepts both
  HTTP 200 `ready` and HTTP 503 `not_ready`. Malformed, unexpected-status, non-JSON, and network
  failures remain safe errors. Login distinguishes ready/not-ready/unavailable, and Overview renders
  a valid `not_ready` result while the independent Jobs request succeeds
- **Required-Password Sign-Out:** The blocked password-change view now includes a duplicate-safe
  Sign out action that uses the centralized protected logout flow. It remains visible at the mobile
  breakpoint while normal navigation remains unavailable
- **Browser Evidence:** Live local QA passed a rapid Jobs-to-Profile route change with the completed
  old request unable to overwrite Profile, Jobs detail control restoration, route-owned dialog
  disposal, configured default dark plus stored System plus light OS resolving to light, a real 503
  readiness response displayed as not ready while Jobs succeeded, and 390-pixel required-password
  Sign out returning to Login with normal navigation hidden. Browser warnings/errors: 0
- **Security Regression:** Unsafe DOM/code sinks, non-theme storage, cookie ownership, session-token
  access, external resources/CDNs, role-name authorization, job submission, raw logs, benchmark
  contamination, and fake later-phase features remain absent under the architecture/security tests
- **Test Evidence:** `pytest` — 208 passed, 0 failed, 0 skipped, 0 warnings, including all Phase
  1E–1J behavior and the new lifecycle/state regressions
- **Quality Evidence:** Compileall, Ruff lint, Ruff format for 93 files, strict mypy for 67 source
  files, `pip check`, `git diff --check`, Alembic heads/current/check at `20260812_05`, exactly seven
  ORM tables, browser runtime QA, dependency/schema diff, and runtime-residue checks passed
- **Unchanged Contracts:** No ORM table/model, migration, Python/npm dependency, permission, backend
  authentication/session/CSRF, job state/API, system-health authority, preference persistence,
  external resource, or Phase 1K behavior was added or changed
- **Architecture Decisions Added:** None; this hardening remains within the frozen FastAPI/static
  HTML/CSS/Vanilla-JS architecture

Phase 1 and v0.1.0 remain in progress. Phase 1K has not begun and remains blocked pending independent
review of Phase 1J.1.

## Phase 1J — Frontend Design-System Expansion

- **Implementation Status:** COMPLETE (2026-08-13)
- **Gate Result:** PASS; ready for independent review before Phase 1K
- **Browser Bootstrap:** The public typed `/api/v1` response retains name/version/foundation status
  and adds only default theme plus configured CSRF cookie/header names. Custom safe settings and
  privacy exclusions are tested; no token values, session-cookie name, database URL, environment,
  password, or secret configuration is returned
- **Authenticated Workspace:** A static hash-routed Vanilla-JS shell provides login, session
  bootstrap, required password change, Overview, owner-only Jobs, read-only Profile, authorized
  System Health, logout, and safe not-found/empty/loading/error/permission states. Identity remains
  in memory and server state remains authoritative
- **API and Browser Security:** One same-origin client owns fetch and CSRF-cookie access, handles
  JSON/204 and safe errors, includes credentials, and applies configured CSRF only to logout,
  password change, cancel, and retry. Production JS uses safe DOM construction and contains no
  unsafe HTML/code-execution sinks, session-token access, role-name authorization, payload logging,
  unsafe artifact links, or non-theme browser storage
- **Design System:** Matching semantic dark/light token sets, System/Dark/Light preference,
  compact layered cards, badges, alerts, forms, buttons, progress, tables, tabs, stepper, dialog,
  trust meter, responsive shell/navigation, reduced motion, and Jobs/System Health print styling
  extend the canonical near-black indigo/violet visual language without copying demo behavior
- **Truthful Pages:** Overview uses `/api/v1`, `/health/ready`, `/auth/me`, and a bounded recent-jobs
  request; future projects/datasets/semantics/models/simulation are disabled roadmap states. Jobs
  exposes list/detail/cancel/retry with confirmation and no submission path. Rich diagnostics use
  only the permission-protected Admin endpoint and preserve every honest Phase 1I state
- **Responsive/Runtime Evidence:** In-app browser verification passed for login, authenticated
  Overview, authorized diagnostics, desktop layout, a 390-pixel mobile drawer, no page overflow,
  and zero browser warnings/errors. No Node/npm install, build pipeline, CDN, remote font, analytics,
  or runtime browser dependency was introduced
- **Test Evidence:** `pytest` — 198 passed, 0 failed, 0 skipped, 0 warnings, including frontend
  architecture/security/anti-contamination, custom browser bootstrap, auth/session/CSRF/RBAC,
  owner-only jobs/local-worker concurrency, observability/audit, readiness, and system health
- **Quality Evidence:** Compileall, Ruff lint, Ruff format for 93 files, strict mypy for 67 source
  files, `pip check`, `git diff --check`, isolated Alembic heads/current/check, seven-table ORM
  inspection, browser runtime QA, dependency/schema diff, and runtime-residue checks passed
- **Unchanged Contracts:** No table, ORM model, migration, Python/npm dependency, permission,
  backend auth/jobs/health authority, remote call, ingestion, analytics, modelling, simulation,
  reports, or LLM-provider behavior was added
- **Architecture Decisions Added:** None; Phase 1J implements the frozen FastAPI/static
  HTML/CSS/Vanilla-JS architecture without beginning Phase 1K

Phase 1 and v0.1.0 remain in progress. Phase 1K has not begun and remains blocked pending independent
review of Phase 1J.

## Phase 1I — Readiness & Authorized System Health

- **Implementation Status:** COMPLETE (2026-08-13)
- **Gate Result:** PASS; ready for independent review before Phase 1J
- **Health Separation:** `/health/live` remains an unauthenticated process-only response with only
  status and timestamp. `/health/ready` remains unauthenticated and minimal. Rich typed diagnostics
  live only at `/api/v1/admin/system/health` behind `system.configure`
- **Startup and Runtime Readiness:** Startup preconditions check application/configuration, SQLite,
  foreign keys, migration head, and required runtime-log storage before worker start. Full runtime
  readiness additionally requires the local worker to be running and accepting work, avoiding the
  previous startup dependency cycle. Worker start and bounded shutdown run through the threadpool;
  safe startup failures leave liveness available and runtime readiness unavailable
- **Active and Deferred Dependencies:** Readiness now reports application, configuration, database,
  foreign keys, migration, runtime logs, and job worker. `analytical_storage` is the sole deferred
  check because ingestion and Parquet storage are not implemented
- **Rich Diagnostics:** `SystemHealthService` reports sanitized SQLite connectivity/FK/migration/
  quick-check/size, data/artifact/log storage and free space, local-worker and persisted-queue state,
  honest unimplemented local/remote LLM states, outbound policy facts, model-artifact storage,
  latest persisted backup-job summary, bounded CRITICAL runtime-event summaries, and portable CPU/
  memory fields
- **Privacy and Network Boundary:** Display paths are basename-only; no DB URL, absolute path,
  secret, token, raw exception, SQL, message, metadata, or raw log line is returned. LLM diagnostics
  perform no DNS, HTTP, socket, provider, model-loading, or download operation
- **Authorization:** The Admin route uses the existing `CorePermission.SYSTEM_CONFIGURE` dependency.
  Tests prove 401 anonymous, 403 without mapping, 200 for a non-Admin mapped role, and denial for an
  `Admin`-named role after its mapping is removed
- **Unchanged Contracts:** No ORM model, table, migration, dependency, permission catalog, job state,
  public job API, authentication/CSRF/RBAC authority, frontend, provider, backup, or Phase 1J feature
  was added
- **Test Evidence:** `pytest` — 191 passed, 0 failed, 0 skipped, 0 warnings, including public/Admin
  separation, startup degradation, permission-only access, SQLite/storage safety, bounded critical
  history, backup selection, honest LLM/policy diagnostics, and all Phase 1E–1H.2 regressions
- **Quality Evidence:** Compileall, Ruff lint/format for 93 files, strict mypy for 67 source files,
  `pip check`, `git diff --check`, isolated Alembic heads/current/check, seven-table ORM inspection,
  architecture/privacy scans, and runtime-artifact checks passed
- **Architecture Decisions Added:** None; Phase 1I implements the frozen health architecture without
  introducing a new architecture

Phase 1 and v0.1.0 remain in progress. Phase 1J has not begun and remains blocked pending independent
review of Phase 1I.

## Phase 1H.2 — Atomic worker-generation authority hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1I ready for independent review
- **Atomic Authority:** Start and persistence authority are synchronized by one generation-owned
  mutex rather than Boolean snapshots. A worker holds the mutex only across one short
  infrastructure-owned QUEUED-to-RUNNING claim, progress write, artifact write, or terminal-state
  transaction; `stop_starting()` and `abandon()` revoke authority while holding the same mutex
- **Abandonment Safety:** Once abandonment wins the mutex, the old generation cannot begin another
  progress, artifact, success, failure, or cancellation write. Runtime terminal events are emitted
  only for state changes that actually persisted
- **Bounded Shutdown:** Arbitrary handler code never holds the authority mutex. Daemon-thread workers
  retain the finite one-second default shutdown grace, so a permanently blocked handler still cannot
  prevent interpreter termination. An already-authorized short database action may complete before
  revocation
- **Restart Safety:** A `LocalJobBackend` rejects `start()` with `JOB-WORKER-UNAVAILABLE` while any
  abandoned prior-generation daemon thread remains alive. Once all such threads have exited, the
  same backend may start a new generation and perform interrupted-job recovery safely
- **Deterministic Race Evidence:** Event-gated tests force abandonment ahead of terminal persistence,
  late progress and artifact calls after abandonment, start revocation ahead of a queued claim, and
  revocation waiting for an already-authorized short persistence action. Persisted rows remain
  recoverable without false terminal state or late mutation
- **Phase 1H.1 Regression:** The ordinary pytest suite retains the permanent-block subprocess
  termination and fresh-process `JOB-WORKER-INTERRUPTED` recovery proof, daemon-worker checks,
  graceful completion, safe persistence decoding, owner-only API, audit, and ContextVar isolation
- **Unchanged Contracts:** No schema, migration, dependency, status/type, public API, retry,
  authentication, RBAC, audit-envelope, readiness, frontend, or Phase 1I change was introduced
- **Test Evidence:** `pytest` — 182 passed, 0 failed, 0 skipped, 0 warnings, including all
  deterministic authority interleavings and the permanent-block subprocess termination/recovery
  proof
- **Quality Evidence:** Compileall, Ruff lint/format for 89 files, strict mypy for 64 source files,
  `pip check`, `git diff --check`, isolated Alembic heads/current/check, seven-table ORM inspection,
  architecture scans, and artifact checks passed
- **Architecture Decisions Added:** None; this is a concurrency correction within the frozen local
  single-process worker architecture

Phase 1 and v0.1.0 remain in progress. Phase 1I has not begun and remains blocked pending independent
review of Phase 1H.2.

## Phase 1H.1 — Local Worker Shutdown & Persistence Hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1I ready for independent review
- **Bounded Process Shutdown:** `LocalJobBackend` now uses a standard-library queue and a bounded set
  of at most 32 explicit daemon worker threads rather than `ThreadPoolExecutor`. Shutdown rejects new
  work immediately, drains queued local IDs, waits a finite one-second grace period by default, and then
  abandons completion authority for any still-running generation. The constructor accepts a bounded
  grace override for deterministic tests
- **Completion and Recovery Safety:** Cooperative handlers may finish or acknowledge cancellation
  during grace. A handler returning after grace cannot persist progress or a false terminal result;
  its row remains `RUNNING` and the next worker start converts it to retryable `FAILED` with
  `JOB-WORKER-INTERRUPTED` / `Job execution was interrupted.`
- **Process-Level Evidence:** A child process started a permanently blocked non-cooperative handler,
  completed backend shutdown in under 0.5 seconds, exited normally without releasing the handler,
  and left the job non-succeeded. A fresh recovery child using the same isolated migrated database
  produced the required retryable interrupted failure
- **Safe Persistence Decoding:** Job metadata now has a `json.loads`-only sanitized decoder that
  returns `{}` for malformed text. Artifact references use one canonical bounded relative-reference
  validator on both writes and reads; corrupt absolute, traversal, unsupported-character, oversized,
  non-string, and malformed entries are never exposed through snapshots or the API
- **Deployment Constraint:** `LocalJobBackend` is explicitly documented as a single-process provider.
  Multiple active local worker processes sharing one control-plane database are unsupported;
  multi-process/distributed execution requires a future provider with worker ownership and leases
- **Unchanged Contracts:** The job schema, revision `20260812_05`, seven-table ORM allowlist, frozen
  statuses/types/transitions, owner-only API, authentication, CSRF, RBAC, audit schema/actions,
  observability envelope, readiness behavior, dependency declarations, and lock file are unchanged
- **Test Evidence:** `pytest` — 177 passed, 0 failed, 0 skipped, 0 warnings, including the subprocess
  termination/recovery proof, grace-period completion, late-completion suppression, repeated app
  lifespan cleanup, corruption/tampering decoding, and all Phase 1E–1H regressions
- **Quality Evidence:** Compileall, Ruff lint/format, strict mypy, `pip check`, `git diff --check`,
  Alembic heads/check, architecture scans, and artifact checks passed with no migration or dependency
  changes
- **Architecture Decisions Added:** None; this pass hardens the frozen local-first provider without
  adding distributed coordination or beginning Phase 1I

Phase 1 and v0.1.0 remain in progress. Phase 1I has not begun and remains blocked pending independent
review of Phase 1H.1.

## Phase 1H — Persistent Job Service & Local Worker Backend

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; ready for independent review before Phase 1I
- **Persistent Contract:** Revision `20260812_05` adds only `jobs`, producing the exact seven-table
  ORM allowlist: `audit_events`, `jobs`, `permissions`, `role_permissions`, `roles`, `user_sessions`,
  and `users`. Job rows contain bounded generic lifecycle/progress, owner and trace correlation,
  bounded manual-attempt/cancellation state, safe artifact references, sanitized metadata/errors,
  and UTC timestamps. They contain no analytical rows, arbitrary payload, credentials, traceback,
  callable/module path, pickle, or artifact bytes
- **Lifecycle and Concurrency:** Guarded SQL updates enforce exactly queued→running/cancelled,
  running→succeeded/failed/cancelled, and eligible failed/cancelled→queued. Claims and retries are
  single-winner under competing sessions; success ends at 100%; retries reuse the logical job ID,
  increment the bounded attempt count, reset transient state, and remain manual only
- **Local Worker:** A bounded two-thread `ThreadPoolExecutor` schedules persisted IDs through an
  immutable trusted `JobType`→handler registry. Application construction starts no threads; FastAPI
  lifespan starts/stops the worker only when existing readiness is green. Production composition
  registers zero domain handlers, no client submission route exists, and no dynamic imports,
  arbitrary code, network queue, Redis, Celery, RabbitMQ, or Kafka were introduced
- **Cancellation and Shutdown:** Queued cancellation atomically reaches `CANCELLED`; running
  cancellation is cooperative through the execution context and never force-kills a Python thread.
  Shutdown stops acceptance and queued futures without falsely marking a non-cooperative running
  handler successful; unresolved `RUNNING` work is recovered safely on the next start
- **Recovery and Safe Failure:** Startup converts stale `RUNNING` rows to retryable `FAILED` with
  `JOB-WORKER-INTERRUPTED`, while queued jobs are re-enqueued only when a trusted handler is
  registered. Unexpected handler failures persist only `JOB-EXECUTION-FAILED` and the generic
  message `Job execution failed.`; runtime JSONL keeps only safe exception type/frame metadata
- **API and Governance:** Authenticated owner-only `GET /api/v1/jobs`, `GET /api/v1/jobs/{job_id}`,
  `POST /api/v1/jobs/{job_id}/cancel`, and `POST /api/v1/jobs/{job_id}/retry` expose immutable safe
  schemas. Cross-owner and absent IDs share `JOB-NOT-FOUND`; cancel/retry require CSRF; ownerless jobs
  are not exposed. No new permission code or role-name authority was invented
- **Observability and Audit:** Runtime submission/start/progress/success/failure/cancellation/retry/
  recovery events use job resource IDs and persisted worker trace/request context. Durable
  `job.submit`, `job.cancel`, and `job.retry` record control actions; interrupted recovery is also
  audited, while progress ticks remain out of SQLite
- **Worker Health:** `JobBackendHealth` exposes only `running`, `accepting_jobs`, `worker_count`, and
  `queue_depth`. Readiness integration is intentionally deferred to Phase 1I; Phase 1H preserves the
  existing minimal readiness response and its explicit `job_worker` deferred check
- **Migration Evidence:** Isolated empty→`20260812_05`, current/check, `20260812_05`→`20260812_04`→
  `20260812_05` passed. `alembic check` reported no new upgrade operations
- **Test Evidence:** `pytest` — 172 passed, 0 failed, 0 skipped, 0 warnings, including schema,
  state-machine, competing claim/retry, worker lifecycle, cancellation, recovery, shutdown, privacy,
  owner isolation, CSRF, audit, context separation, and all prior authentication/RBAC/observability
  regressions
- **Quality Evidence:** Compileall, Ruff lint/format, strict mypy, `pip check`, `git diff --check`,
  Alembic head/current/check/downgrade/re-upgrade, architecture scans, and artifact checks passed;
  dependencies and lock remain unchanged
- **Architecture Decisions Added:** None; Phase 1H implements the frozen local-first job architecture
  without beginning rich Admin health, frontend work, domain jobs, ingestion, analytics, models,
  simulation, LLMs, or Phase 1I

Phase 1 and v0.1.0 remain in progress. Phase 1I has not begun and remains blocked pending independent
review of Phase 1H.

## Phase 1G.1 — Observability context and correlation hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1H ready for independent review
- **H-001 Authenticated Context:** Authentication is now a two-stage dependency: a synchronous helper
  performs `AuthService`/SQLAlchemy work in FastAPI's worker thread, then an async wrapper binds safe
  identity ContextVars and request state in the request task. Protected sync routes and downstream
  sync dependencies inherit user/session-correlation/role plus trace/request IDs; centralized error
  logs use the safe request-state bridge required across `BaseHTTPMiddleware` task boundaries
- **H-001 Isolation Evidence:** Tests prove authenticated context visibility, anonymous follow-up
  reset, and deterministic two-user interleaving without identity cross-contamination. Existing
  dependency caching, 401/403, CSRF, session, RBAC, and request-state behavior remains unchanged
- **H-002 Multi-Sink Correlation:** `JsonFormatter` now freezes timestamp, event ID, trace ID, and
  request ID on each `LogRecord`. Repeated formatting and the real console-plus-JSONL handler path
  produce identical four-field event identity, including when no request context exists
- **H-003 Static Messages:** An AST conformance guard scans production `logger.debug/info/warning/error/
  exception/critical` calls and requires exactly one positional literal string message with runtime
  values confined to structured fields
- **Test Evidence:** `pytest` — 160 passed, 0 failed, 0 skipped, 0 warnings, including request-task
  binding, downstream sync inheritance, handled-error identity, anonymous reset, deterministic
  concurrent isolation, and repeated/dual-handler correlation identity
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 79 files;
  strict mypy passed for 56 source files; `pip check`, `git diff --check`, Alembic heads/check,
  architecture scans, and artifact checks passed. Migration `20260812_04`, the six-table ORM
  allowlist, dependency files, rotation defaults, streams/actions, and audit/RBAC/auth architecture
  remain unchanged
- **Architecture Decisions Added:** None; this is a narrow correction to the Phase 1G context and
  logging contracts and introduces no Phase 1H implementation

Phase 1 and v0.1.0 remain in progress. Phase 1H has not begun and remains subject to independent
review of this hardening pass.

## Phase 1G — Structured Observability & Durable Audit

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; ready for independent review before Phase 1H
- **Canonical Envelope:** One immutable typed event model supplies aware UTC timestamps,
  unpredictable UUID event IDs, trace/request correlation, component/action/status/severity,
  sanitized metadata, and the frozen optional identity/resource/model/run/LLM context. The exact 12
  streams are audit, security, application, frontend, data_processing, ml, llm, simulation,
  performance, export, errors, and system
- **Context and Runtime Logs:** Middleware isolates and resets request/trace plus authenticated user,
  resolved-role, and non-secret session-correlation context. Every request emits one minimal
  performance event. Console and `<log_dir>/ipsp-runtime.jsonl` share the formatter; JSONL rotates at
  10 MiB with five backups and safe handler replacement across repeated app construction
- **Safe Diagnostics:** Unexpected exceptions expose only exception type and at most 32 frames with
  basename, function, and line number. Messages, args, traceback text, source lines, locals, object
  reprs, absolute paths, and environment values are excluded
- **Durable Audit:** Revision `20260812_04` adds only append-only `audit_events`. The repository owns
  inserts/reads without update/delete or commits; `AuditService.record_in_session` atomically couples
  security mutations with sanitized deterministic JSON audit insertion
- **Selected Coverage:** Durable events cover login success/failure, logout, password-change
  success/failure, bootstrap, CSRF failure, permission denial, user-role change, role-mapping change,
  and changed catalog synchronization. No-op RBAC mutations emit no false change event, and ordinary
  health/request/auth-me performance logs never populate SQLite
- **Correlation and Privacy:** Integration tests correlate response IDs to runtime JSONL and durable
  permission-denial events, while markers for passwords/hashes/session/token/CSRF/cookies/headers,
  attempted unknown usernames, exception messages/args/locals/paths, and request bodies remain absent
- **Migration and Schema:** Head is `20260812_04`; isolated 03→head→03→head and Alembic check pass.
  The exact ORM allowlist is `audit_events`, `permissions`, `role_permissions`, `roles`,
  `user_sessions`, and `users`; dependencies and lock remain unchanged
- **Test Evidence:** `pytest` — 154 passed, 0 failed, 0 skipped, 0 warnings, including event model,
  runtime rotation/reconfiguration, exception-frame privacy, schema constraints, selected auth/RBAC
  durability, atomic rollback, trace continuity, runtime/SQLite separation, and all prior regressions
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 79 files;
  strict mypy passed for 56 source files; `pip check`, `git diff --check`, isolated Alembic
  heads/upgrade/current/check/downgrade/re-upgrade, architecture scans, and artifact checks passed
- **Architecture Decisions Added:** None; Phase 1G implements the frozen observability/audit contract
  without beginning jobs, rich Admin health, frontend expansion, or later domain phases

Phase 1 and v0.1.0 remain in progress. Phase 1H has not begun and remains blocked pending independent
review of Phase 1G.

## Phase 1F.1 — RBAC CLI safe-failure hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1G ready for independent review
- **Safe Operational Boundary:** `ipsp-sync-rbac` now converts the finite expected set of IPSP,
  migration-state, SQLAlchemy, and Pydantic settings failures into one generic non-zero CLI result.
  Raw exception text, SQL, database URLs and paths, configuration values, stack traces, and
  password/session/CSRF/token markers are never printed; `KeyboardInterrupt` and `SystemExit` remain
  unswallowed
- **Resource Cleanup:** Once foundation services exist, engine disposal is guaranteed for successful,
  no-op, stale-migration, migration-inspection, and database-inspection outcomes, including process
  control exceptions
- **Regression Evidence:** Focused tests preserve successful and idempotent synchronization, prove
  safe below-head refusal, inject `MigrationStateError`, SQLAlchemy inspection failure, and invalid
  settings, verify marker suppression, and assert post-construction engine disposal
- **Test Evidence:** `pytest` — 145 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall, Ruff lint/format for 73 files, strict mypy for 52 source files,
  `pip check`, and `git diff --check` passed. `pyproject.toml`, `requirements.lock`, migration head
  `20260811_03`, and the five-table ORM allowlist remain unchanged by this hardening pass
- **Architecture Decisions Added:** None; this is a narrow Phase 1F CLI failure-boundary correction
  and introduces no Phase 1G implementation

Phase 1 and v0.1.0 remain in progress. Phase 1G has not begun and remains subject to independent
review of this hardening pass.

## Phase 1F — RBAC Permission Enforcement

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; ready for independent review before Phase 1G
- **Runtime Authority:** `User.role_id → Role → RolePermission → Permission` is the sole permission
  path. `RBACService.has_permission` performs a fresh fail-closed database query, and
  `enforce_permission` raises the safe `PermissionDeniedException` mapped to HTTP 403
  `AUTHZ-PERMISSION_DENIED`. There is no role-name, persisted Admin Boolean, wildcard, access-level,
  cookie, session, or cached permission shortcut
- **Core Catalog:** A typed first-party `CorePermission` catalog contains exactly the 13 frozen codes:
  `simulation.run`, `simulation.export`, `dataset.view`, `dataset.upload`, `dataset.configure`,
  `dataset.assign`, `model.train`, `model.promote`, `llm.configure`, `internet.configure`,
  `user.manage`, `logs.view`, and `system.configure`. Persisted permission strings remain extensible
- **Provisioning:** Additive, idempotent synchronization ensures Admin/User roles, all 13 core
  Permission rows, and 13 explicit Admin mappings. User receives no automatic grants, and custom
  roles, permissions, and mappings are preserved without pruning. Admin is usable only because of
  its mappings, not its name
- **API Boundary:** The reusable permission dependency authenticates first, resolves the composed
  RBAC service, and enforces using the authenticated user ID. Temporary integration routes prove
  401 authentication precedence, safe 403 denials, allowed mapped access, and independent CSRF plus
  RBAC composition for state-changing requests; no new production endpoint was added
- **Privilege Changes:** Narrow transactional primitives change a user's role or replace a role's
  mappings and invalidate all active sessions for exactly the affected users. Same-role and
  identical-mapping operations are no-ops. Catalog privilege expansion invalidates existing Admin
  users' sessions while no-op synchronization and unrelated-role sessions remain valid
- **Bootstrap and Existing Installations:** Fresh `ipsp-create-admin` now provisions the catalog and
  creates the first Admin with explicit mappings. `ipsp-sync-rbac` requires the database at current
  migration head, supports databases with users, reports only safe counts, and is repeatable
- **Schema and Dependencies:** No table, column, session snapshot, or Alembic migration was added;
  head remains `20260811_03` and the five-table ORM allowlist is unchanged. No dependency was added,
  `requirements.lock` is unchanged, and `pyproject.toml` changed only for `ipsp-sync-rbac`
- **Test Evidence:** `pytest` — 140 passed, 0 failed, 0 skipped, 0 warnings, including catalog,
  extensibility, anti-bypass, fail-closed matrix, dependency/CSRF, bootstrap/CLI, runtime freshness,
  privilege invalidation, and all Phase 1E/1E.1 authentication regressions
- **Quality Evidence:** Compileall, Ruff lint/format, strict mypy, `pip check`, `git diff --check`,
  Alembic heads/current/check, architecture scans, and runtime-artifact checks passed
- **Architecture Decisions Added:** None; Phase 1F implements locked decision D-016 without beginning
  Phase 1G durable audit/observability work

Phase 1 and v0.1.0 remain in progress. General user management, dataset ACL, and durable audit
persistence remain incomplete; Phase 1G must not begin until Phase 1F receives independent review.

## Phase 1E.1 — Authentication side-channel and regression hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1F ready for independent review
- **Authentication Failure Equalization:** Unknown, disabled, and currently locked login attempts now
  each perform exactly one dummy Argon2 verification. Active wrong-password and successful attempts
  each perform one real verification without an additional dummy operation. All four public failure
  classes retain the identical safe `AUTH-INVALID_CREDENTIALS` HTTP 401 response
- **Dummy Credential Policy:** `PasswordService` constructs its non-secret dummy Argon2 hash once
  with the same active `PasswordHash.recommended()` policy used for production hashes. It is not
  hard-coded, generated per request, or capable of authenticating
- **CSRF Regressions:** Integration coverage now proves a present CSRF header with a missing CSRF
  cookie is rejected, and a CSRF cookie/header from one valid session cannot authorize a different
  valid bearer session. Existing missing-header, mismatch, persisted-hash, Unicode, and leak checks
  remain intact
- **Session Fixation Regression:** An explicitly attacker-selected session cookie is replaced by a
  fresh server-generated bearer token at login; neither its raw value nor its digest becomes the
  authenticated session, while the stored SHA-256 digest matches only the newly issued token
- **Test Evidence:** `pytest` — 125 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall, Ruff lint and format, strict mypy, `pip check`, and
  `git diff --check` passed. Dependency files, migration history, and the five-table ORM allowlist
  remained unchanged
- **Architecture Decisions Added:** None; this is a narrow correction within the frozen Phase 1E
  authentication architecture and introduces no Phase 1F permission enforcement

Phase 1 and v0.1.0 remain in progress. Phase 1F must not begin until this hardening pass receives
independent review.

## Phase 1E — Authentication & Server-Side Session Security

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; ready for independent review before Phase 1F
- **Passwords:** Maintained `pwdlib[argon2]` produces Argon2id hashes, supports verify-and-update,
  preserves bounded Unicode input, and performs a real dummy Argon2 verification for unknown users.
  No plaintext, bcrypt, passlib, JWT, pepper, or generated default password path exists
- **Sessions:** Every successful login generates independent 256-bit-or-greater opaque session and
  CSRF tokens. Only deterministic SHA-256 hashes are stored in `user_sessions`; bearer values remain
  cookies only. Sessions use fixed expiry, UTC timestamps, last-seen updates, fresh non-secret UUID
  correlation IDs, fixation protection, logout invalidation, and user-scoped all-session invalidation
- **Browser Security:** Central cookie helpers set the session cookie HttpOnly and both cookies
  Secure by default, SameSite `lax`, Path `/`, and aligned expiry. Production rejects insecure-cookie
  configuration; explicit insecure cookies are limited to development/localhost HTTP. Authenticated
  logout and password change enforce the readable CSRF-cookie/header/hash contract
- **Login & Identity:** Generic authentication failures conceal unknown, wrong-password, disabled,
  and locked states. Failed attempts increment the persisted counter, apply temporary lockout at the
  configured threshold, and reset after an eligible successful login. Disabled users cannot log in
  or continue old sessions. Safe identity context resolves role ID/name but no permissions
- **API:** Thin `/api/v1/auth/login`, `/me`, `/logout`, and `/change-password` routes use explicit
  Pydantic `SecretStr` requests, safe response schemas, reusable session/CSRF dependencies, stable
  IPSP errors, no-store responses, and no bearer values in JSON
- **Password Change:** Current-password verification precedes persisted replacement; success updates
  the Argon2id hash and UTC password timestamp, clears forced-change and lock state, invalidates every
  session for that user, clears cookies, and leaves other users' sessions unchanged
- **Bootstrap:** The interactive `ipsp-create-admin` CLI requires an already migrated empty database,
  reads/confirm passwords with `getpass`, ensures only the canonical Admin/User role rows, assigns the
  first user to Admin, creates no permission mappings, and refuses subsequent bootstrap attempts
- **Migration:** Revision `20260811_03` directly descends from `20260811_02`, creates only
  `user_sessions`, downgrades only that table, re-upgrades cleanly, leaves one head, and retains the
  five-table ORM allowlist
- **Dependencies:** Added `pwdlib[argon2]>=0.3.0,<0.4`; the Python 3.12 lock resolves pwdlib 0.3.0,
  argon2-cffi 25.1.0, argon2-cffi-bindings 25.1.0, cffi 2.1.1, and pycparser 3.0
- **Test Evidence:** `pytest` — 121 passed, 0 failed, 0 skipped, 0 warnings, covering password,
  settings, session schema/lifecycle, login/lockout, cookies, identity, CSRF, logout, password change,
  disabled users, scoped invalidation, bootstrap, readiness, leak markers, and conformance behavior
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 68 files;
  strict mypy passed for 48 source files; `pip check`, `git diff --check`, and the isolated Alembic
  upgrade/current/check/downgrade/re-upgrade smoke passed
- **Clean Environment Evidence:** The exact lock installed in a disposable Python 3.12.0 environment;
  IPSP installed with `--no-deps`; all 121 tests, Ruff checks, strict mypy, compileall, and `pip check`
  passed, after which the environment was removed
- **Architecture Decisions Added:** None; Phase 1E implements the frozen authentication authorities
  and intentionally does not implement RBAC permission enforcement or Admin-name authorization

Phase 1 and v0.1.0 remain in progress. RBAC permission enforcement remains owned by Phase 1F and
must not begin until Phase 1E receives independent review.

## Phase 1D — User / Role / Permission Security-Schema Foundation

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for independent review before Phase 1E
- **Schema:** Canonical typed SQLAlchemy 2.x mappings add exactly `roles`, `permissions`,
  `role_permissions`, and `users`. Model metadata contains no other tables, and the migration inserts
  no production role, permission, mapping, user, password, or credential data
- **Authorization Structure:** `User.role_id → Role → RolePermission → Permission` is the only
  structural authorization path. Role-permission mappings use a composite primary key, and no
  persisted `is_admin`, equivalent bypass Boolean/level, permission blob, wildcard, or role hierarchy
  exists
- **User Schema:** The frozen minimum identity/lifecycle fields are present; username is unique,
  email and creator are nullable, role is required, creator is a self-FK, lifecycle defaults agree
  between ORM and migration, and `failed_login_count >= 0` is enforced intrinsically
- **UTC Boundary:** One reusable `UTCDateTime` rejects naive input, normalizes aware values to UTC
  before SQLite persistence, and restores aware UTC datetimes. UTC, `+05:30`, nullable, default, and
  all-security-timestamp round trips pass on real SQLite
- **Migration:** Revision `20260811_02` directly descends from `20260811_01`, creates only the four
  authorized tables, downgrades cleanly to the Phase 1C baseline, re-upgrades cleanly, leaves one
  script head, and passes `alembic check`
- **Constraint Evidence:** Real SQLite inserts prove username, role name, permission code, and mapping
  uniqueness; user role, self-creator, and both mapping FKs; and non-negative failed-login enforcement
- **ORM Evidence:** Canonical session transactions insert all four entities and query them using
  `select()`, `Session.execute()`, `Session.scalars()`, and an explicit
  `User → Role → RolePermission → Permission` join without a repository or RBAC service
- **Readiness:** A Phase 1D-head database returns HTTP 200; a Phase 1C-baseline database returns HTTP
  503 with `SYS-MIGRATION-REQUIRED`; FK-disabled readiness and database-independent liveness remain
  unchanged
- **Dependencies:** No direct or resolved dependency changes; `pyproject.toml` and
  `requirements.lock` remain unchanged
- **Test Evidence:** `pytest` — 101 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 53 files;
  strict mypy passed for 36 source files; `pip check` and `git diff --check` passed
- **Conformance Evidence:** The exact four-table allowlist, sole ORM/Alembic ownership, synchronous
  SQLAlchemy, no production `create_all()`, no authorization bypass, no session/preference tables, no
  authentication/RBAC/password behavior, and all prior framework/network/contamination guards pass
- **Intentionally Deferred:** Password hashing, login/logout, sessions, cookies, CSRF, lockout
  behavior, authentication routes, bootstrap administration, and RBAC permission enforcement remain
  owned by Phase 1E/1F
- **Architecture Decisions Added:** None; Phase 1D implements locked decisions D-004, D-014, D-015,
  D-016, and the security schema authorities

Phase 1 and v0.1.0 remain in progress. Phase 1E functionality was not introduced and must not begin
until Phase 1D receives independent review.

## Phase 1C.1 — Database foundation hardening

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; Phase 1D ready for independent review
- **H-001 Readiness Semantics:** Healthy readiness returns HTTP 200; migration-required,
  database-unavailable, FK-disabled, and invalid migration-state responses return HTTP 503 with the
  same minimal safe response contract. Liveness remains HTTP 200 and database-independent
- **H-002 SQL Parameter Privacy:** Every engine forces SQLAlchemy `hide_parameters=True`; echo and
  `StatementError` regression coverage proves the `DO_NOT_LEAK_DATABASE_PARAMETER` bound value is
  absent from captured logs, output, and rendered errors
- **H-003 Deterministic Default:** The no-environment default resolves through SQLAlchemy URL
  utilities to `<repository>/database/ipsp.db` and remains unchanged when the process CWD changes.
  `.env.example` leaves the optional absolute URL override commented out
- **H-004 Synchronous Driver Restriction:** Database URL validation accepts only `sqlite` and
  `sqlite+pysqlite`; `sqlite+aiosqlite`, non-SQLite, malformed, credential-bearing, and host-bearing
  URLs fail closed without installing another driver
- **H-005 FK Readiness:** Readiness now requires `PRAGMA foreign_keys=1`. Tests verify two distinct
  DBAPI connection lifecycles and prove a real test-only invalid child insert raises an integrity error
- **H-006 Migration Heads:** Script and database inspection use multi-head APIs, require one script
  head, allow zero database heads before migration, accept one matching head, and convert multiple or
  malformed heads into a safe migration-state failure and HTTP 503
- **H-007 Conformance:** Automated guards now cover frontend frameworks, Streamlit, legacy and async
  SQLAlchemy, aiosqlite, production `create_all()`, duplicate Declarative Bases/Alembic roots,
  Phase-1C business tables, runtime CDNs, JWT libraries, outbound HTTP clients, Redis, and Celery. The
  no-business-table assertion is explicitly documented as a Phase-1C-only guard for Phase 1D evolution
- **Dependencies:** No direct or resolved dependency changes; `pyproject.toml` and
  `requirements.lock` remain unchanged
- **Test Evidence:** `pytest` — 84 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 49 files;
  strict mypy passed for 34 source files; `pip check` and `git diff --check` passed
- **Architecture Decisions Added:** None; this hardening pass corrects reviewed Phase 1C behavior
  within locked decisions D-004, D-014, and D-015

Phase 1 and v0.1.0 remain in progress. Phase 1D functionality was not introduced and remains blocked
until Phase 1C.1 receives independent review.

## Phase 1C Status

**Phase 1C - Synchronous SQLite Control-Plane Foundation & Alembic Baseline**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for independent review before Phase 1D
- **Configuration:** Immutable nested `IPSP_DATABASE__URL`, `IPSP_DATABASE__ECHO`, and
  `IPSP_DATABASE__CONNECTION_TIMEOUT_SECONDS` settings now configure the control plane. Only
  credential-free SQLite URLs are accepted; unsupported or malformed URLs fail closed
- **Database Foundation:** One canonical `DeclarativeBase` and `MetaData` with deterministic naming
  conventions live under `backend/ipsp/database/models/`. The explicit synchronous engine enables
  SQLite foreign keys on every connection and applies the configured timeout without global engines,
  automatic schema creation, WAL policy, or asynchronous SQLAlchemy
- **Sessions:** The typed session factory always closes sessions, never commits implicitly, commits
  only through an explicit transaction scope, and rolls failed transactions back
- **Migrations:** Root `alembic.ini` and the sole history under `database/migrations/` support online
  and offline execution through application Settings. The `20260811_01` no-op foundation baseline
  creates no business entity tables, and upgrade/current/downgrade/re-upgrade/check flows pass
- **Migration State & Readiness:** Side-effect-free revision inspection reports current revision,
  expected head, and head alignment. Readiness actively checks configuration, SQLite connectivity,
  and migration head with safe status codes; analytical storage and job workers remain explicitly
  deferred, while liveness remains database-independent
- **Dependencies:** Added maintained SQLAlchemy 2.0 and Alembic 1.x direct constraints. The exact
  Python 3.12 lock snapshot records SQLAlchemy 2.0.51, Alembic 1.19.1, and required transitive packages
- **Test Evidence:** `pytest` - 75 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 49 files;
  strict mypy passed for 34 source files; `pip check` and `git diff --check` passed
- **Clean Environment Evidence:** The exact lock installed in a fresh Python 3.12.0 virtual
  environment; the local package installed with no dependency resolution; all tests, Ruff checks,
  strict mypy, compileall, and `pip check` passed there
- **Conformance Evidence:** Exactly one Alembic root; no business/auth/RBAC/job ORM tables; no
  `create_all()`, legacy `Session.query()`, asynchronous SQLAlchemy, benchmark-specific production
  constants, runtime CDN, or prohibited architecture patterns
- **Architecture Decisions Added:** None; Phase 1C implements locked decisions D-004, D-014, and D-015

Phase 1 and v0.1.0 remain in progress. Phase 1D functionality was not introduced and must not begin
until Phase 1C receives independent review.

## Phase 1B Status

**Phase 1B — Configuration, SecretProvider, Feature Flags & Outbound Policy**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for independent review before Phase 1C
- **Configuration:** One immutable Pydantic Settings tree now separates runtime values, safe-off
  feature flags, secret-provider selection, and deny-by-default outbound permissions using canonical
  `IPSP_FEATURES__*`, `IPSP_OUTBOUND__*`, and `IPSP_SECRETS__*` environment variables
- **Secrets:** `SecretProvider`, validated `SecretRef`, redacted `SecretValue`, and the approved
  environment-injected provider are implemented. Required resolution fails closed without generated
  defaults, plaintext errors, configuration fields, logging, or ordinary JSON serialization
- **Outbound Policy:** Side-effect-free evaluation and enforcement cover global Internet, remote LLM,
  model-download, update-check, provider allowlisting, all five frozen transmission levels, explicit
  dataset-policy inputs, restricted-data local-only defaults, and context-sensitive fail-closed rules
- **Composition:** The app factory explicitly constructs immutable foundation services and exposes
  them through application state without mutable globals or a general service locator
- **Dependencies:** No direct or resolved dependency changes; `pyproject.toml` and
  `requirements.lock` remain unchanged
- **Test Evidence:** `pytest` — 59 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 41 files;
  strict mypy passed for 30 source files; `pip check` and `git diff --check` passed
- **Security Evidence:** The `DO_NOT_LEAK_PHASE1B_SECRET` marker remained absent from repr/str,
  configuration snapshots, Pydantic/JSON serialization, API error details, structured logs, secret
  lookup failures, and outbound-policy denials
- **Conformance Evidence:** Benchmark/business-term, Streamlit, legacy `Session.query()`, runtime CDN,
  JWT/browser-auth, actual network-call, and premature database/auth/upload/analytics scans passed
- **Intentional Extension Point:** Protected OS, vault, and cloud secret backends remain future
  `SecretProvider` implementations because no technology is frozen; approved environment injection
  is the production provider implemented in this phase
- **Architecture Decisions Added:** None; Phase 1B implements existing frozen configuration,
  privacy, secrets, and outbound-policy authorities

Phase 1 and v0.1.0 remain in progress. Phase 1C functionality was not introduced and must not begin
until Phase 1B receives independent review.

## Phase 1A.1 Status

**Phase 1A.1 — Foundation hardening**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; Phase 1B ready for independent review
- **H-001:** Domain error details now use a recursively sanitized client-safe contract, including
  final response-boundary sanitization and safe handling of unsupported objects
- **H-002:** Structured metadata redaction now recognizes case-insensitive password, token, secret,
  API-key, authorization, and cookie credential forms using deterministic exact/suffix rules
- **H-003:** Completed-request events derive `success` or `failure` from the actual HTTP status
- **H-004:** The JSON formatter emits supplied approved optional IPSP context through an explicit
  allowlist and does not serialize arbitrary `LogRecord` extras
- **H-005:** Egg-info, bytecode, pytest, mypy, and Ruff artifacts are ignored and none are tracked
- **H-006:** The existing lock snapshot installed successfully in a fresh Python 3.12.0 virtual
  environment; `pip check`, local `--no-deps` package installation, all eight direct constraints,
  compile, tests, Ruff lint/format, and strict mypy passed. Exact transitive portability to other
  Python versions was not claimed or tested
- **Test Evidence:** `pytest` — 26 passed, 0 failed, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 34 files;
  strict mypy passed for 26 source files; `pip check` and `git diff --check` passed
- **Conformance Evidence:** Benchmark/business-term, Streamlit, legacy `Session.query()`, runtime CDN,
  hardcoded campaign/demo output, and JWT/browser-auth scans passed
- **Architecture Decisions Added:** None; this pass implements existing frozen safety requirements

Phase 1 remains in progress. Phase 1B functionality was not introduced, and the full v0.1.0
milestone is not marked complete.

## Phase 1A Status

**Phase 1A — Minimal Production Foundation Skeleton**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for Phase 1B review
- **Implemented Scope:** FastAPI application factory, canonical versioned and health routes,
  environment-backed settings, safe central error envelopes, request/trace context, structured
  redacted logging, honest readiness checks, job contracts/enums, offline vanilla frontend shell,
  dark/light theme foundation, repository tooling, and meaningful automated tests
- **Intentionally Deferred:** Authentication, database schema/models, migrations, upload and data
  workflows, analytical execution, ML, LLM integration, simulation, and distributed job execution
- **Test Evidence:** `pytest` — 19 passed, 0 failed, 0 warnings
- **Quality Evidence:** Ruff lint passed; Ruff format check passed for 32 files; strict mypy passed
  for 25 source files; live Uvicorn liveness/readiness/frontend smoke probe passed
- **Conformance Evidence:** Benchmark/business-term, Streamlit, legacy `Session.query()`, runtime CDN,
  hardcoded campaign/demo output, and JWT/browser-auth scans passed
- **Architecture Decisions Added:** None; implementation follows the frozen authority set

Phase 1 remains in progress. Phase 1B must be separately reviewed and executed; this entry does not
mark the full v0.1.0 milestone complete.

## Phase 0.5 Status

**Phase 0.5 — Architecture Correction + Documentation Reconciliation**

- **Audit Status:** COMPLETE (2026-08-11)
- **Correction Execution:** COMPLETE (2026-08-11)
- **Findings:** 19 cross-document findings plus 5 completeness improvements; all resolved
- **Reconciliation Report:** [PHASE_0_5_RECONCILIATION_REPORT.md](PHASE_0_5_RECONCILIATION_REPORT.md)
- **Files Modified:** See reconciliation report and execution summary for the comprehensive list
- **Completion Gate:** 20/20 criteria verified

**Phase 1 Status:** 🟢 **READY** — Phase 0.5 completion gate passed

**Phase 0.5 PASS Criteria:**
```
✅ 1. Independent admin authorization removed
✅ 2. SQLAlchemy ORM ownership unified under database/models/
✅ 3. Duplicate ORM guidance removed; Pydantic API schemas separated
✅ 4. Synchronous SQLAlchemy 2.x execution model locked
✅ 5. Fake async database/repository guidance removed
✅ 6. Legacy Session query guidance removed
✅ 7. Alembic migration root unified under database/migrations/
✅ 8. API route ownership unified under api/routes/
✅ 9. Session lifecycle security complete
✅ 10. Raw bearer tokens excluded from logs; session_correlation_id specified
✅ 11. Production secrets fail closed
✅ 12. Runtime CDN dependencies prohibited; assets vendored
✅ 13. Dark/light theme foundation included in v0.1.0
✅ 14. Dataset/semantic/capability/model/run references immutable
✅ 15. Multi-table status derived rather than persisted twice
✅ 16. Audit envelope and log-sink policy reconciled
✅ 17. Job contracts/schema included in v0.1.0
✅ 18. Liveness/readiness/Admin diagnostics separated
✅ 19. Documentation consistency and contamination scans passed
✅ 20. Reconciliation report and progress status updated after verification
```

Update this file after each phase. Do not mark complete without test evidence.
