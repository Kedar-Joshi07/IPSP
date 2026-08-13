# Codex Prompt — Rewrite IPSP README as the Comprehensive Repository Entry Point

## Repository
`Kedar-Joshi07/IPSP`

## Starting point
Use the **current `main` HEAD after the parallel-development governance documentation has been merged**.

The currently accepted foundation baseline before that documentation change is:

```text
cd0dca48ded8d68f18e861f2427dfeb746d52ea7
```

Do not assume that SHA is still HEAD. Verify:

```text
git status --short
git rev-parse HEAD
git branch --show-current
```

This task modifies **README.md only** unless a broken README link proves that a tiny documentation-index correction is required. Do not change production code.

---

# Objective

Rewrite the root `README.md` so it becomes the **comprehensive, unambiguous entry point for both humans and AI agents**.

The existing README is directionally correct and its factual status/constraints must be preserved. The problem is not correctness; the goal is to make it much more complete.

A reader who knows nothing about IPSP should be able to understand, from the README alone:

- what IPSP is;
- why it exists;
- what business/technical problem it solves;
- what makes it different from a fixed-domain simulator;
- what v1.0 is intended to look and feel like when complete;
- the end-to-end data-to-simulation lifecycle;
- how deterministic evidence, ML, LLMs, trust, humans, and governance divide authority;
- how structured datasets are ingested, understood, semantically modeled, validated, modeled, simulated, explained, trusted, stored, reproduced, and exported;
- how the UI dynamically derives controls/results instead of hardcoding a domain;
- what is implemented today in v0.1.0;
- what is intentionally not implemented yet;
- how the repository is organized;
- how security, privacy, RBAC, jobs, observability, health, outbound policy, storage planes, and versioning work;
- the milestone roadmap from v0.1.0 to v1.0.0;
- how parallel development is governed;
- where to find deeper specifications and flow diagrams.

The README should function as:

1. product overview;
2. architecture overview;
3. implementation status guide;
4. developer onboarding guide;
5. AI-agent orientation document;
6. documentation map.

It must not replace the detailed specifications. It should summarize them and link to them.

---

# Governing truth rule

Read repository sources before rewriting.

Do not invent functionality.

Clearly distinguish:

```text
IMPLEMENTED NOW — v0.1.0 foundation
```

from:

```text
TARGET V1.0 ARCHITECTURE / ROADMAP
```

Never describe future engines as already implemented.

The accepted v0.1.0 foundation includes:

- typed configuration;
- environment-backed SecretProvider boundary;
- deny-by-default outbound policy;
- synchronous SQLite/SQLAlchemy 2.x control plane;
- Alembic migration management;
- users/roles/permissions;
- Role → RolePermission → Permission authorization;
- Argon2id password security;
- opaque server-side sessions;
- CSRF;
- failed-login lockout;
- first-admin bootstrap;
- structured runtime observability;
- durable SQLite audit events;
- persistent generic jobs;
- single-process local daemon-worker backend;
- owner-scoped job APIs;
- liveness/readiness/Admin System Health;
- static offline HTML/CSS/Vanilla-JS application shell;
- dark/light/system themes;
- Login, Overview, Jobs, Profile, System Health;
- responsive/accessibility/security foundation.

Do not claim that v0.1.0 already implements:

- dataset ingestion;
- Parquet analytical-plane orchestration;
- dataset ACLs;
- profiling/data understanding;
- relationships/semantic discovery;
- semantic manifests;
- capability discovery;
- model training/registry;
- simulations;
- Trust Engine;
- LLM provider execution;
- run history;
- PDF/Excel export;
- executable backup/restore;
- full dynamic metadata-driven product UI.

---

# Mandatory repository review

Before editing README, inspect the current production tree and all Markdown documentation.

At minimum read completely:

## Repository/agent guidance
- `AGENTS.md`
- `.github/copilot-instructions.md`
- all `.github/instructions/*.md`
- `FILE_INDEX.md`

## Product / scope / architecture
- `docs/00_SCOPE_FREEZE.md`
- `docs/01_PROJECT_SPEC.md`
- `docs/02_PRODUCT_REQUIREMENTS.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`
- `docs/32_DECISION_LOG.md`
- `docs/38_GLOSSARY.md`
- `docs/40_ANTI_CONTAMINATION.md`

## UI
- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`
- `reference/README.md`
- inspect `reference/Campaign_simulator_UI.html`
- inspect current `frontend/`

## Data understanding / semantics
- `docs/07_DATA_UNDERSTANDING_SPEC.md`
- `docs/08_SEMANTIC_MODEL_SPEC.md`
- `docs/09_RELATIONSHIPS_HIERARCHY_LINEAGE_SPEC.md`
- `docs/10_KPI_METRIC_DEPENDENCY_SPEC.md`
- `docs/20_INGESTION_STORAGE_SPEC.md`
- `docs/21_SAMPLING_PROVENANCE_SPEC.md`

## Capabilities / models / simulation / trust
- `docs/11_CAPABILITY_DISCOVERY_SPEC.md`
- `docs/12_MODELING_ENGINE_SPEC.md`
- `docs/13_MODEL_REGISTRY_LIFECYCLE_SPEC.md`
- `docs/14_SIMULATION_ENGINE_SPEC.md`
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`
- `docs/25_REPORTING_EXPORT_SPEC.md`
- `docs/26_SIMULATION_HISTORY_REPRODUCIBILITY.md`

## LLM / privacy / governance
- `docs/16_LLM_ARCHITECTURE.md`
- `docs/17_PRIVACY_REMOTE_LLM_POLICY.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`

## Foundation / operational behavior
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/24_JOB_PROCESSING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/36_BACKUP_RETENTION_RECOVERY.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `docs/39_BENCHMARK_CATALOG.md`

## Parallel development
- `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`
- `docs/42_ACTIVE_WORKSTREAMS.md`
- `docs/43_WORKSTREAM_CONTRACT_TEMPLATE.md`

## Flow diagrams
Read every file under `flows/`, especially:
- `flows/01_SYSTEM_ARCHITECTURE.md`
- `flows/02_DATASET_ONBOARDING.md`
- `flows/03_DATA_INTELLIGENCE_PACKET.md`
- `flows/04_SEMANTIC_CLARIFICATION.md`
- `flows/05_RELATIONSHIP_DISCOVERY.md`
- `flows/06_CAPABILITY_DISCOVERY.md`
- `flows/07_MODEL_LIFECYCLE.md`
- `flows/08_SIMULATION_EXECUTION.md`
- `flows/09_TRUST_VALIDATION.md`
- `flows/10_LLM_ROUTING.md`
- `flows/11_AUTH_RBAC.md`
- `flows/12_STORAGE_PLANES.md`
- `flows/13_OBSERVABILITY_TRACE.md`
- `flows/14_REPORT_EXPORT.md`
- `flows/15_BACKGROUND_JOBS.md`
- `flows/16_PRIVACY_REMOTE_LLM.md`
- `flows/17_PREDICTION_HORIZON_LEAKAGE.md`
- `flows/18_JOURNEY_STAGE_METRIC_GRAPH.md`
- `flows/19_WORKSPACE_HIERARCHY.md`
- `flows/20_END_TO_END_LIFECYCLE.md`
- `flows/21_PARALLEL_DEVELOPMENT.md`

## Current implementation
Inspect current code, not only specs:
- `backend/ipsp/main.py`
- `backend/ipsp/config/**`
- `backend/ipsp/database/**`
- `backend/ipsp/auth/**`
- `backend/ipsp/security/**`
- `backend/ipsp/observability/**`
- `backend/ipsp/jobs/**`
- `backend/ipsp/repositories/**`
- `backend/ipsp/services/**`
- `backend/ipsp/api/**`
- `frontend/**`
- `tests/**`
- `database/migrations/**`
- `pyproject.toml`
- `requirements.lock`

---

# README writing goals

The README should be comprehensive but navigable.

Prefer:
- strong section hierarchy;
- concise explanatory paragraphs;
- tables where comparison/status is clearer;
- Mermaid diagrams where they materially improve understanding;
- relative links to detailed repository docs;
- explicit current-vs-target labels;
- concrete examples that are generic, not benchmark-specific.

Avoid:
- a giant unstructured wall of text;
- repeating detailed specs verbatim;
- benchmark-specific domain assumptions;
- fake implementation status;
- marketing language without technical substance.

---

# Mandatory README structure

Use this structure unless the repository evidence requires a minor improvement.

## 1. Title and identity

Include:

```text
Intelligent Predictive Simulation Platform (IPSP)
Initial experience: CampaignSim — Powered by IPSP
Target specification: v1.0
Current accepted implementation: v0.1.0 foundation
```

Explain in one strong paragraph what IPSP is.

## 2. The problem IPSP solves

Explain why ordinary fixed-schema analytics/simulation applications fail when datasets differ.

Describe IPSP's core idea:

> Rather than asking "how do we make this dataset fit a simulator?", IPSP asks "what can this dataset responsibly support?"

Explain practical usefulness:
- unknown structured datasets;
- semantic discovery;
- capability discovery;
- safe modelling/simulation;
- refusal when unsupported;
- repeatability/governance.

## 3. Product definition and non-goals

Include the formal concept:

```text
DATA → UNDERSTANDING → SEMANTIC CONTRACT → CAPABILITY DISCOVERY
     → MODEL VALIDATION → DYNAMIC UI → SIMULATION → TRUST GATE
     → RESULTS / HISTORY / EXPORT
```

State:
- structured/tabular data focus;
- not a universal document AI system;
- not a marketing-specific simulator;
- not a guarantee of causal inference;
- no arbitrary autonomous joins;
- no executable LLM code against raw datasets.

Link:
- `docs/00_SCOPE_FREEZE.md`
- `docs/01_PROJECT_SPEC.md`
- `docs/02_PRODUCT_REQUIREMENTS.md`

## 4. Current implementation vs target v1.0

Create a clear table.

Columns:

```text
Area
v0.1.0 status
Target v1.0
Deep-dive link
```

Rows should include:
- Foundation/runtime
- Authentication/RBAC
- Jobs
- Observability/audit
- Health
- Frontend shell
- Ingestion/storage
- Data understanding
- Semantics
- Relationships/lineage
- Capability discovery
- Modelling/model registry
- Simulation
- Trust
- LLM
- History/reproducibility
- Reports/exports
- Backup/restore

This is one of the most important README sections.

## 5. End-to-end target lifecycle

Use a Mermaid diagram based on repository flows:

```text
Login
→ Workspace
→ Upload + context
→ Secure staging/validation
→ Canonical dataset/version
→ Deterministic profiling
→ Data Intelligence Packet
→ Semantic proposal
→ Clarification if needed
→ Versioned Semantic Manifest
→ Capability discovery
→ Model/engine validation
→ Dynamic controls
→ Simulation
→ Trust validation
→ Persisted result
→ History / compare / reproduce / PDF / Excel
```

Link to:
- `flows/20_END_TO_END_LIFECYCLE.md`
- `flows/02_DATASET_ONBOARDING.md`

## 6. Architecture overview

Explain:

```text
HTML/CSS/Vanilla JS
        ↓
FastAPI
        ↓
Auth/RBAC + Application Services + Jobs
        ↓
Ingestion / Understanding / Semantics / Capability
        ↓
Models / Simulation / Explainability
        ↓
Trust
        ↓
Results / History / Exports
```

Discuss cross-cutting:
- permissions;
- privacy;
- outbound policy;
- secrets;
- versioning;
- jobs;
- observability;
- errors.

Link:
- `docs/03_ARCHITECTURE.md`
- `flows/01_SYSTEM_ARCHITECTURE.md`

## 7. Storage architecture

Explain the two-plane model.

### SQLite control/knowledge plane
Metadata, security, versions, manifests, capabilities, registry, runs, jobs, audit.

### Source/Parquet analytical plane
Original uploads, canonical datasets, analytical/training data references.

Explain why millions of analytical rows are not forced into SQLite.

Use/link:
- `flows/12_STORAGE_PLANES.md`
- `docs/20_INGESTION_STORAGE_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`

## 8. Dataset onboarding and versioning

Explain target flow:
- authorization;
- validation;
- staging/quarantine;
- immutable original;
- checksum;
- dataset identity;
- immutable dataset version;
- tables/sheets;
- provenance;
- canonical Parquet;
- no default flattening.

Discuss supported target formats:
CSV/TSV, XLSX, Parquet, JSON/JSONL, ZIP.

Make clear this is v0.2+ target functionality, not yet v0.1 runtime behavior.

## 9. Data Understanding Engine

Explain deterministic profiling first.

Include evidence categories:
- types;
- nulls;
- cardinality;
- distributions;
- examples;
- grain;
- keys;
- entity;
- dimensions/measures;
- time;
- targets/controls;
- units;
- sensitive fields;
- associations;
- functional dependencies;
- join multiplication;
- time ordering;
- leakage candidates.

Explain "never rely on names alone."

Link:
- `docs/07_DATA_UNDERSTANDING_SPEC.md`
- `flows/03_DATA_INTELLIGENCE_PACKET.md`

## 10. Semantic Model Engine

Explain target Dataset Semantic Manifest.

Include:
- entity;
- identifier;
- dimension;
- measure families;
- target;
- control;
- context;
- time;
- event/state;
- hierarchy;
- relationships;
- KPI/derived measure;
- constraint;
- attribution;
- provenance;
- sensitivity;
- lineage;
- prediction-horizon availability.

Explain evidence + user confirmation + optional LLM proposal.

Explain conflict workflow.

Link:
- `docs/08_SEMANTIC_MODEL_SPEC.md`
- `flows/04_SEMANTIC_CLARIFICATION.md`

## 11. Relationships, hierarchy, lineage, KPI dependency

Summarize:
- structural relationships;
- identity joins;
- temporal joins;
- ordered journey;
- state/lifecycle;
- measure dependency;
- plan vs actual;
- commercial flow;
- hierarchy;
- feature lineage;
- join-safety/multiplication;
- metric dependency graph.

Link:
- `docs/09_RELATIONSHIPS_HIERARCHY_LINEAGE_SPEC.md`
- `docs/10_KPI_METRIC_DEPENDENCY_SPEC.md`
- `flows/05_RELATIONSHIP_DISCOVERY.md`

## 12. Capability Discovery

Explain:

> What can responsibly be calculated, diagnosed, predicted, simulated, explained, or refused?

List major capability families.

Explain four gates:
1. semantic;
2. data;
3. model/engine;
4. trust.

Explain lifecycle:
`DISCOVERED → VALIDATING → VALIDATED → ENABLED`
and limited/disabled/blocked states.

Explain responsible refusal as a feature.

Link:
- `docs/11_CAPABILITY_DISCOVERY_SPEC.md`
- `flows/06_CAPABILITY_DISCOVERY.md`

## 13. Modelling and model lifecycle

Explain candidate routing:
- regression;
- classification;
- count;
- forecasting;
- similarity/look-alike.

Explain:
- simple baseline first;
- validation strategy chosen by data grain/time/entity;
- leakage protection;
- champion/challenger;
- shadow evaluation;
- no silent self-rewriting.

Link:
- `docs/12_MODELING_ENGINE_SPEC.md`
- `docs/13_MODEL_REGISTRY_LIFECYCLE_SPEC.md`
- `flows/07_MODEL_LIFECYCLE.md`

## 14. Simulation engines

Explain target engines:
- predictive ML scenario;
- deterministic what-if;
- benchmark scenario;
- Monte Carlo;
- SDV synthetic context.

Explain control eligibility:
- only semantic controls or explicitly allowed assumptions;
- no outcome/post-outcome/unsafe sensitive ordinary controls.

Explain support/extrapolation checks.

Link:
- `docs/14_SIMULATION_ENGINE_SPEC.md`
- `flows/08_SIMULATION_EXECUTION.md`

## 15. Trust & Validation Engine

Give this section strong prominence.

Include governing principle:

```text
AI proposes.
Evidence validates.
Rules constrain.
Models compete.
Humans arbitrate exceptions.
The system remembers the outcome.
```

Explain dimensions:
- data quality;
- semantic confidence;
- model validation;
- support;
- drift/extrapolation;
- constraints;
- privacy/governance.

Explain intrinsic vs confirmed semantic vs business vs empirical expectation.

Explain Green/Amber/Red.

Explicitly mention that negative financial values are not universally invalid.

Link:
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`
- `flows/09_TRUST_VALIDATION.md`

## 16. ML vs LLM authority

Explain:

```text
ML/statistics = numerical/statistical authority
Local LLM = semantic intelligence
Remote LLM = optional escalation
```

Modes:
- ML_ONLY
- LOCAL_LLM
- REMOTE_LLM
- HYBRID_LLM

Explain deterministic profiler → compact Dataset Intelligence Packet → optional LLM.

Explain raw datasets are never wholesale transmitted.

Link:
- `docs/16_LLM_ARCHITECTURE.md`
- `docs/17_PRIVACY_REMOTE_LLM_POLICY.md`
- `flows/10_LLM_ROUTING.md`
- `flows/16_PRIVACY_REMOTE_LLM.md`

## 17. Security, RBAC, privacy, outbound

Document current foundation accurately.

Include current roles:
Admin/User backed by permissions.

Current authority:
`User → Role → RolePermission → Permission`

List canonical 13 permissions.

Explain:
- Argon2id;
- opaque server-side sessions;
- hash-only persistence;
- HttpOnly/Secure/SameSite;
- CSRF;
- lockout;
- session invalidation;
- first-admin CLI;
- SecretProvider;
- outbound deny-by-default;
- remote data policy.

Clearly state dataset ACL/column policy execution is target future work because datasets are not yet implemented.

Link:
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `flows/11_AUTH_RBAC.md`

## 18. Background jobs

Describe implemented v0.1 job architecture:
- persisted SQLite metadata;
- exact statuses;
- generic job types;
- progress;
- cancellation;
- retry;
- safe errors;
- owner scoping;
- recovery;
- bounded shutdown;
- single-process LocalJobBackend.

Explain future distributed provider possibility without claiming Redis/Celery exists.

Link:
- `docs/24_JOB_PROCESSING_SPEC.md`
- `flows/15_BACKGROUND_JOBS.md`

## 19. Observability, audit, errors, health

Explain:
- trace_id;
- request_id;
- event_id;
- session_correlation_id;
- user/role/resource refs;
- rotating structured runtime logs;
- durable audit/security SQLite events;
- redaction;
- stable error codes.

Current health endpoints:
- `/health/live`
- `/health/ready`
- `/api/v1/admin/system/health`

Link:
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `flows/13_OBSERVABILITY_TRACE.md`

## 20. Results, history and export target

Explain Run Result Object and target:
- baseline/scenario;
- predictions;
- intervals;
- trust;
- warnings;
- model/data lineage;
- seed/config;
- compare;
- re-run;
- reproduce;
- PDF;
- Excel.

Clearly label as later roadmap.

Link:
- `docs/25_REPORTING_EXPORT_SPEC.md`
- `docs/26_SIMULATION_HISTORY_REPRODUCIBILITY.md`
- `flows/14_REPORT_EXPORT.md`

## 21. UI/UX vision

Explain current production frontend:
HTML/CSS/Vanilla JS ES modules, no React/Vue/Angular/Svelte/Streamlit/CDN.

Describe:
- CampaignSim — Powered by IPSP initial branding;
- dark/light/system;
- responsive app shell;
- Login/Overview/Jobs/Profile/System Health today.

Explain target dynamic v0.7 behavior:
UI controls/results derived from discovered metadata/capabilities, not fixed campaign fields.

The reference HTML is visual language only.

Link:
- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`
- `reference/README.md`

## 22. Anti-contamination and benchmark strategy

Explain why benchmarks exist.

List the seven benchmark families briefly as tests of generic discovery, not production assumptions.

State benchmark-specific names are prohibited from core.

Link:
- `docs/39_BENCHMARK_CATALOG.md`
- `docs/40_ANTI_CONTAMINATION.md`

## 23. Technical stack

Separate **currently active foundation dependencies** from **target v1.0 analytical stack** if useful.

Architecture direction includes:
- Python 3.11+
- FastAPI/Uvicorn
- SQLAlchemy/SQLite
- Polars
- Pandas as required
- PyArrow
- OpenPyXL
- scikit-learn
- LightGBM
- CatBoost
- Statsmodels
- SDV
- NumPy/SciPy
- SHAP
- Optuna
- HTML/CSS/Vanilla JS
- locally vendored Plotly.js when charts require it

Do not imply every target library is already exercised in v0.1.0.

## 24. Repository structure

Show a concise repository tree and explain canonical ownership:
- ORM;
- API schemas;
- routers;
- migrations;
- repositories;
- services;
- engines;
- frontend;
- tests;
- docs;
- flows;
- prompts;
- benchmarks/reference.

Link:
- `docs/04_PROJECT_STRUCTURE.md`

## 25. Current API surface

Document only actually implemented routes:
- `/`
- `/api/v1`
- auth endpoints;
- jobs endpoints;
- System Health;
- liveness/readiness.

Explain future API families are architectural reservations, not current runtime routes.

Link:
- `docs/28_REST_API_CONTRACT.md`

## 26. Local development

Preserve and improve current instructions:
- Python environment;
- install;
- migration;
- first Admin bootstrap;
- start Uvicorn;
- localhost Secure-cookie development exception;
- browser URL;
- offline operation.

Do not weaken production HTTPS/security defaults.

## 27. Quality and testing

Explain layers:
- unit;
- integration;
- security;
- architecture;
- benchmark;
- acceptance.

Include current commands.

Mention v0.1.0 foundation acceptance evidence without pasting the entire acceptance report.

Link:
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/PHASE_1_ACCEPTANCE_REPORT.md`

## 28. Version roadmap

Create a clear table:

```text
v0.1.0 Foundation — COMPLETE
v0.2.0 Ingestion/storage/provenance
v0.3.0 Data understanding/relationships
v0.4.0 Semantic manifest/clarification
v0.5.0 Capability/model validation
v0.6.0 Simulation/trust/history
v0.7.0 Dynamic frontend
v0.8.0 Local LLM
v0.9.0 Remote/hybrid LLM
v1.0.0 Production-ready integration
```

Use current progress doc as source of truth.

Link:
- `docs/31_IMPLEMENTATION_PROGRESS.md`

## 29. Parallel development workflow

Explain same-version/different-module approach.

State:
- `main` = accepted milestones;
- `integration/vX.Y.Z` = Kedar-owned milestone candidate;
- feature branches = isolated workstreams;
- Kedar alone merges/finalizes;
- contributors push only own branches;
- one migration owner;
- frozen shared contracts;
- branch gate → integration gate → milestone gate.

Link:
- `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`
- `docs/42_ACTIVE_WORKSTREAMS.md`
- `docs/43_WORKSTREAM_CONTRACT_TEMPLATE.md`
- `flows/21_PARALLEL_DEVELOPMENT.md`

## 30. Documentation map

Create a compact categorized table linking the most important docs.

Categories:
- Start here;
- Product/scope;
- Architecture;
- UI;
- Data/semantics;
- Capability/models/simulation/trust;
- LLM/privacy/security;
- Operations;
- Testing/release;
- Development workflow;
- Flows/reference.

Do not list 80 links as an undifferentiated bullet dump.

Link to `FILE_INDEX.md` for the exhaustive list.

## 31. Key glossary

Include a compact set of critical terms:
- Capability;
- Dataset Semantic Manifest;
- Control plane;
- Analytical data plane;
- Prediction horizon;
- Feature lineage;
- Attribution;
- Look-alike;
- Trust Score;
- Champion/Challenger.

Link:
- `docs/38_GLOSSARY.md`

## 32. Current limitations / intentional boundaries

State plainly:
- v0.1 is foundation, not completed v1.0 product;
- local SQLite control plane;
- LocalJobBackend single-process;
- no ingestion yet;
- no dataset ACL runtime yet;
- no semantic/model/simulation engines yet;
- no LLM provider execution yet;
- no export/backup execution yet.

This section prevents humans/AIs from assuming roadmap specs are already implemented.

---

# Accuracy requirements

Before finalizing README:

1. Search every claim that says `implemented`, `supports`, `currently`, or `available` against production code/tests.
2. Search every roadmap claim against specifications/progress.
3. Verify every relative Markdown link exists.
4. Ensure future functionality uses wording such as:
   - `target v1.0`;
   - `planned`;
   - `roadmap`;
   - `will`;
   - `not yet implemented`.
5. Ensure current foundation uses:
   - `implemented`;
   - `accepted v0.1.0`;
   only where evidence exists.
6. Do not claim v1.0 is production ready.
7. Do not hardcode benchmark-domain fields or examples into the product definition.

---

# README style

The README should feel like a strong open-source/enterprise architecture README:

- comprehensive;
- professional;
- technically precise;
- readable by non-authors;
- navigable;
- not marketing-heavy;
- not a spec dump;
- sufficiently detailed for AI orientation.

Use tables and diagrams to reduce text density.

Aim for roughly **4,000–7,000 words if needed**, but prioritize completeness and clarity over arbitrary length. It is acceptable to be shorter if nothing important is lost.

---

# Verification

After editing:

```text
git diff -- README.md
git diff --check
```

Programmatically verify that every relative `.md` link in README resolves to an existing repository path.

Run the relevant documentation/static tests if any test asserts README content. Run the full test suite only if repository rules require it for documentation-only changes.

---

# Final report

Return:

```text
A. Starting SHA
B. README sections created
C. Current-vs-target distinctions
D. Architecture/lifecycle diagrams
E. Implemented v0.1 details documented
F. Target v1.0 engine details documented
G. Documentation links added
H. Parallel-development section
I. Relative-link validation
J. Files modified
K. Tests/checks
L. Deviations
M. Final status
```

Expected files modified:

```text
README.md
```

Do not modify production code.

End:

```text
README REWRITE: PASS — comprehensive repository entry point ready for review
```
