# F-002 and IPSP v0.1.1 Final Acceptance Report

Audit date: **2026-08-18**  
Audited branch and SHA: **`main` at `226033430d6366e75099b5791aed57526cb470fd`**  
Audit work package: **F2-J**  
Gate result: **FAIL — interactive browser acceptance evidence is incomplete**

This report is the independent F2-J audit record. It does not replace or rewrite the historical
[Phase 1 Acceptance Report](PHASE_1_ACCEPTANCE_REPORT.md). No production defect was found and no
production source, test, schema, migration, dependency, lockfile, configuration, CI, frontend, or
feature-flag change was made during this audit. Because one required acceptance stream could not be
completed, v0.1.1 is not promoted and v0.2 remains blocked and not started.

## A. Starting State

The audit began from the user-accepted F2-I SHA
`226033430d6366e75099b5791aed57526cb470fd` on `main`, with a clean working tree. The accepted
historical v0.1.0 foundation remains identified by
`cd0dca48ded8d68f18e861f2427dfeb746d52ea7`. At audit start, v0.1.1 was implemented and pending
F2-J acceptance, while v0.2.0 was blocked and `NOT STARTED`.

The F-002 scope is the frozen post-v0.1.0 architecture and bounded v1.0 roadmap. The v0.1.1
reconciliation scope is deliberately narrow: neutral IPSP runtime identity, provider-neutral
synthetic-capability naming, application/package version 0.1.1, current license inventory and
project notice, architecture conformance, and foundation CI gates. It does not implement an F-002
analytical capability.

## B. Source-of-Truth Hierarchy

The audit applied this authority order:

1. [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and
   [Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md);
2. locked decisions in [Scope Freeze](00_SCOPE_FREEZE.md) and
   [Decision Log](32_DECISION_LOG.md), preserving accepted historical meanings;
3. explicit numbered and F-002 specifications under `docs/`;
4. future structured contracts and schemas;
5. confirmed persisted user/admin semantic metadata;
6. deterministic profiling evidence;
7. LLM proposals;
8. benchmark narrative and commentary.

F-002 supersedes conflicting older target-architecture wording without making planned capabilities
implemented or rewriting the accepted v0.1.0 history.

## C. F-002 Architecture Coherence Matrix

The classification describes current implementation availability. A `DEFERRED_BY_ROADMAP` row has
a coherent frozen F-002 contract but no current runtime implementation; that is not an architecture
defect.

| # | Area | Classification | Audit evidence |
|---:|---|---|---|
| 1 | Product identity | PASS | IPSP is the only generic product/runtime identity; CampaignSim is historical/reference material. |
| 2 | Canonical lifecycle | PASS | The authority and flow set consistently use data-to-understanding-to-governed-learning with responsible refusal. |
| 3 | Domain Experience architecture | DEFERRED_BY_ROADMAP | The neutral pack boundary and non-ownership of formula truth are frozen; runtime starts later. |
| 4 | Domain families | DEFERRED_BY_ROADMAP | Family taxonomy and activation boundaries are frozen without hard-coding a current domain. |
| 5 | Metric & Formula Registry | DEFERRED_BY_ROADMAP | Versioned numerical authority is frozen; runtime starts at its roadmap milestone. |
| 6 | CrossDomainSemanticGraph | DEFERRED_BY_ROADMAP | Evidence-based graph construction and no-invented-edge rules are frozen. |
| 7 | ScenarioIntentManifest | DEFERRED_BY_ROADMAP | Intent validation and supported-capability gating are frozen. |
| 8 | Exact simulation bases | DEFERRED_BY_ROADMAP | Exactly `DATA_BASED`, `MIXED`, and `INTENT_BASED` are authoritative. |
| 9 | CompositeSimulationGraph | DEFERRED_BY_ROADMAP | Typed, validated graph construction and graph-safety rules are frozen. |
| 10 | EngineRegistry | DEFERRED_BY_ROADMAP | Provider-neutral engine metadata contract is frozen. |
| 11 | LicenseRegistry | DEFERRED_BY_ROADMAP | License compatibility is an explicit pre-selection gate. |
| 12 | EngineResolver | DEFERRED_BY_ROADMAP | Capability, license, Trust, suitability, security, and resource gates precede selection. |
| 13 | Provider neutrality | PASS | Current configuration is capability-oriented and no future provider is selected or installed. |
| 14 | Open-source-preferred policy | PASS | Governance and current dependency inventory preserve preference without asserting future candidates are installed. |
| 15 | Model selection and baselines | DEFERRED_BY_ROADMAP | Baseline-first, leakage-safe selection and lifecycle contracts are frozen. |
| 16 | Causal boundary | DEFERRED_BY_ROADMAP | Predictive association cannot be presented as causality; causal claims require adequate design/evidence. |
| 17 | Optimization boundary | DEFERRED_BY_ROADMAP | Optimization is constrained by validated objectives, semantics, feasibility, evidence, and refusal. |
| 18 | Finance architecture | DEFERRED_BY_ROADMAP | Currency, units, grain, time, reconciliation, and stress boundaries are explicit and domain-safe. |
| 19 | Trust | DEFERRED_BY_ROADMAP | Trust remains distinct from Evidence Profile and model/LLM confidence. |
| 20 | Evidence Profile | DEFERRED_BY_ROADMAP | Evidence quality, access, and lineage remain distinct from Trust. |
| 21 | Provenance including `SYNTHETIC_DATA` | DEFERRED_BY_ROADMAP | Synthetic/simulation/assumption sources cannot be promoted directly to observed truth. |
| 22 | SimulationLearningStore | DEFERRED_BY_ROADMAP | Governed, provenance-preserving learning storage is frozen for a later milestone. |
| 23 | OutcomeReconciliation | DEFERRED_BY_ROADMAP | Mature observed outcomes must be reconciled before governed learning. |
| 24 | Champion/challenger learning | DEFERRED_BY_ROADMAP | Promotion requires controlled evaluation and cannot self-promote from unverified results. |
| 25 | LLM modes | DEFERRED_BY_ROADMAP | Local, remote, and hybrid governance is frozen; no LLM has numerical authority. |
| 26 | Evidence access modes | DEFERRED_BY_ROADMAP | Access/transmission boundaries are frozen and raw rows remain local by default. |
| 27 | UI/navigation | DEFERRED_BY_ROADMAP | Target capability-driven navigation is frozen; only the neutral v0.1.1 foundation shell exists. |
| 28 | Backend layering | PASS | Current typed services, repositories, thin routers, injected providers, and job abstraction conform. |
| 29 | Two-plane storage | DEFERRED_BY_ROADMAP | SQLite control-plane and future analytical-plane responsibilities are separated; no analytical store exists yet. |
| 30 | Revised roadmap/v1.0 boundary | PASS | The frozen v0.1.1 → v0.2.0 → … → v0.15.0 → v1.0.0 sequence is consistently authoritative. |

Counts: **6 PASS, 24 DEFERRED_BY_ROADMAP, 0 BLOCKED, 0 NOT_APPLICABLE**. No F-002
architecture-coherence blocker was found.

## D. Roadmap and Versioning Matrix

| Boundary | Audited state | Result |
|---|---|---|
| F-002 | Frozen architecture authority, not an application version | PASS |
| v0.1.0 | Historical independently accepted foundation | PASS |
| v0.1.1 | F-002 foundation reconciliation implemented; F2-J acceptance incomplete | BLOCKED |
| v0.2.0 | Contract freeze not started; implementation not started | PASS |
| v0.3.0–v0.15.0 | Frozen ordered capability roadmap; not started | DEFERRED_BY_ROADMAP |
| v1.0.0 | First GA target; not released | DEFERRED_BY_ROADMAP |

Authorization is distinct from implementation start. Because F2-J does not pass, v0.2 contract-freeze
preparation is not authorized by this audit.

## E. Current-versus-Future Status Matrix

| Surface | Current v0.1.1 foundation | F-002 target status |
|---|---|---|
| API/runtime | FastAPI factory, `/api/v1`, safe errors, typed settings | Capability-driven APIs are deferred |
| Control plane | Synchronous SQLAlchemy, SQLite, one Alembic tree, seven tables | Expanded control metadata is deferred |
| Security | Local authentication, RBAC, opaque sessions, CSRF, lockout, deny-by-default outbound policy | Dataset/project/column and consent governance are deferred |
| Jobs | Persistent generic jobs, `JobBackend`, `LocalJobBackend` | Additional provider implementations are deferred |
| Frontend | Neutral local IPSP Login/Overview/Jobs/Profile/System Health shell | Full dynamic target navigation is deferred |
| Analytical plane | Not implemented | Ingestion, canonical Parquet, manifests, metrics, models, simulation, evidence, and learning are deferred |
| AI/providers | Policy boundaries only; no analytical/AI provider installed | Governed local/remote/hybrid capabilities are deferred |

## F. Active-Document Contradiction Sweep

Repository-wide inspection covered active documentation, instructions, prompts, flows, source, tests,
configuration, migrations, and dependency artifacts. Historical references were retained only where
clearly identified as historical evidence.

| Prohibited direction | Result |
|---|---|
| CampaignSim as current product identity | PASS — no active generic-runtime direction found |
| SDV as generic synthetic architecture | PASS — only optional/candidate or historical contexts remain |
| Superseded roadmap | PASS — current authorities use the frozen v0.1.1 through v1.0.0 roadmap |
| Superseded simulation basis | PASS — exactly three authoritative bases remain |
| Bypass Domain Experience/Metric/Engine registries | PASS — authority order and resolution gates are explicit |
| Simulated/synthetic data as empirical truth | PASS — provenance and governed-learning safeguards are explicit |
| LLM numerical authority | PASS — deterministic/schema/evidence validation remains mandatory |

Documentation structure validation before the report covered **137 Markdown files**, **203 relative
links**, **581 Markdown table rows**, balanced fences, and all **30/30** numbered Mermaid flows.

## G. v0.1.1 Production Reconciliation Matrix

| Check | Result | Evidence |
|---|---|---|
| Generic IPSP branding | PASS | Production shell, metadata, routes, tests, and runtime response are neutral. |
| Provider-neutral synthetic flag | PASS | `synthetic_data_enabled` is safe-off; no vendor alias/provider is active. |
| Version 0.1.1 consistency | PASS | Package, settings, API, environment example, tests, frontend, and installed editable metadata agree. |
| No v0.2 implementation | PASS | No ingestion/dataset/Parquet/manifest/metric/engine/model/simulation/learning runtime added. |
| Seven-table foundation | PASS | ORM and isolated migrated database contain exactly the seven accepted tables. |
| Job backend behavior | PASS | `JobBackend`/`LocalJobBackend` and lifecycle suites remain green. |
| Security/observability | PASS | Authentication, RBAC, sessions, CSRF, outbound, audit, errors, and correlation coverage remain green. |
| Architecture conformance | PASS | Generic frontend/config/core checks pass 16/16. |
| License artifacts | PASS | Project notice and exact current third-party inventory reconcile. |
| No target dependency installed | PASS | Candidate analytical/AI libraries are absent. |

## H. Anti-Contamination Matrix

| Boundary | Result |
|---|---|
| No benchmark source-column constants in generic production logic | PASS |
| No fixed funnel/campaign/order/hotel/product/customer/inventory/finance runtime assumptions | PASS |
| No silent `Unknown`-to-negative, zero-to-missing, or non-negative-money assumptions | PASS |
| No universal monotonic-funnel assumption | PASS |
| No same-period outcome-derived persona leakage rule | PASS |
| No unsafe one-to-many measure aggregation rule | PASS |
| No domain pack ownership of generic numerical truth | PASS |
| No invented semantic/composite graph edge | PASS |
| No collapse of Trust, Evidence Profile, or model/LLM confidence | PASS |

## I. Security and Privacy Regression

The two complete suites and focused foundation/security/job suites found no regression. Live isolated
HTTP journeys confirmed Admin and User authentication, ordinary-user `403` denial for System
Health, CSRF-protected logout, session invalidation, and required-password change/re-login. Raw data
transmission remains disabled by default, secrets remain behind the provider boundary, production
errors remain safe, and no credential/cookie artifact was retained.

## J. Database, Migration, Schema, and Dependency Evidence

An isolated temporary SQLite database produced:

- one Alembic tree;
- `heads`: `20260812_05 (head)`;
- `current`: `20260812_05 (head)`;
- `alembic check`: `No new upgrade operations detected`;
- synchronous SQLAlchemy operation with foreign keys enabled;
- exactly `audit_events`, `jobs`, `permissions`, `role_permissions`, `roles`, `user_sessions`, and
  `users` as application tables;
- no v0.2 dataset or analytical tables and no migration drift.

The lock file, installed environment, and `THIRD_PARTY_LICENSES.md` reconcile exactly at **41
packages**. All **11** direct/development declarations resolve to locked versions. Editable IPSP
metadata reports 0.1.1. No analytical/AI candidate dependency is installed, `pip check` reports no
broken requirements, and no dependency or lockfile changed.

## K. Test and Quality Evidence

The full suite was declared as two planned independent invocations and was not rerun until green:

| Gate | Result |
|---|---|
| Full suite run 1 | **220 passed**, 0 failed, 0 skipped, no warnings; pytest 114.82 s (wall 126.9 s) |
| Full suite run 2 | **220 passed**, 0 failed, 0 skipped, no warnings; pytest 97.20 s (wall 104.9 s) |
| Architecture | **16 passed** in 3.34 s |
| Phase 1 foundation + security | **3 passed** in 3.84 s |
| Complete job lifecycle | **18 passed** in 26.24 s |
| Compileall | PASS |
| Ruff lint | PASS |
| Ruff format | PASS — 96 files already formatted |
| Strict mypy | PASS — no issues in 67 source files |
| `pip check` | PASS — no broken requirements |
| `git diff --check` before report creation | PASS |

The known Windows noncooperative-daemon recovery case passed inside both monolithic runs under the
documented AboveNormal parent-process scheduling. No retry loop or one-off rerun was used.

## L. Browser QA

Isolated live HTTP/UI-boundary validation passed for:

- neutral IPSP shell and API version 0.1.1;
- **13/13** same-origin frontend assets and no public CDN/remote runtime asset;
- Admin login, identity/Profile data, Overview/Jobs API dependencies, and System Health;
- ordinary User login, identity/Profile data, Overview/Jobs dependencies, and `403` Admin denial;
- CSRF-protected logout and post-logout `401` identity denial;
- required-password identity gate, password change, old-session invalidation, and re-login with the
  requirement cleared;
- System, Dark, and Light controls present in the served shell.

Interactive browser control could not initialize because the host rejected the bundled browser
runtime dependency as outside its configured trusted code path. Consequently, this audit could not
independently inspect desktop and approximately 390-pixel mobile rendering, horizontal overflow, or
the live application console. Existing integration and architecture coverage for responsive CSS,
theme contracts, local-only assets, route behavior, and error safeguards is green, but it is not a
substitute for the explicitly required interactive F2-J evidence. This is the acceptance blocker.

## M. Repository and Runtime Hygiene

The disposable server processes, QA SQLite database, logs, PID file, directories, sessions, and
credentials were removed. Final residue checks found no listener on the QA port, orphan QA process,
QA database/WAL/SHM, browser profile, temporary virtual environment, archive, cookie, credential, or
untracked test/prompt debris.

After this report was created, repository-wide documentation validation passed across **138
Markdown files**, **208 relative links**, **678 Markdown table rows**, balanced fences, and all
**30/30** structurally valid Mermaid flows. Final `git diff --check` also passed, and Git reported
this report as the only changed path.

During initial QA setup, an incorrectly named nested database environment variable caused Alembic to
apply the accepted migrations to the pre-existing empty ignored runtime database. Inspection proved
that all seven application tables contained zero rows. The audit immediately downgraded exactly
those migrations, removed the empty Alembic version table, and verified that no tables remain. The
subsequent QA run used the correctly isolated database. No user data was present or removed.

## N. Deferred v0.2+ Capabilities

All ingestion, original-file storage, canonical Parquet, dataset versioning, provenance runtime,
profiling, semantic manifests, clarification, relationship inference, Metric & Formula Registry,
Domain Experience activation, capability discovery, Engine/License resolution, modelling,
simulation, Finance, Trust, Evidence Profile, cross-domain composition, learning, outcome
reconciliation, Local AI, and full target UI work remains deferred to its frozen roadmap milestone.
None exists because of F2-J.

## O. Blockers and Unresolved Issues

| Blocker | Product defect | Required resolution |
|---|---|---|
| Interactive browser acceptance evidence is incomplete because the host browser runtime could not initialize under its trusted-path policy. | No | Re-run desktop, approximately 390-pixel mobile, theme interaction, overflow, and console QA in a working approved browser-control environment, then perform an independent F2-J re-audit. |

No architecture, production, schema, migration, dependency, license, security, or test defect was
found. The blocker is nevertheless mandatory under the F2-J contract.

## P. Final Recommendation

- **Production defects found:** None.
- **Production source changes during F2-J:** None.
- **Files created:** `docs/F002_V0_1_1_ACCEPTANCE_REPORT.md` only.
- **Files modified:** None.
- **v0.1.1:** reconciliation implemented, **not accepted** by F2-J.
- **v0.2.0:** **BLOCKED — NOT STARTED**.
- **Recommendation:** repair or provide the approved browser-control environment and repeat the
  incomplete browser stream plus final repository validation. Do not modify production in this
  audit, do not promote README/progress status, and do not begin v0.2.

## Q. Gate Result

**F2-J FAIL.** All architecture, contradiction, production-compatibility, test, quality, migration,
schema, dependency/license, live HTTP journey, and hygiene evidence passed. Required interactive
browser evidence did not complete, so IPSP v0.1.1 F-002 foundation reconciliation is not accepted.

F2-J: FAIL — IPSP v0.1.1 F-002 reconciliation not accepted; v0.2 remains blocked
