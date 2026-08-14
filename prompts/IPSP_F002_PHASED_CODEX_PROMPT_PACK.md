# IPSP F-002 — Phased Codex Architecture-Reconciliation Prompt Pack
## F-002 Architecture Authority → v0.1.1 Foundation Reconciliation → Final Acceptance Gate

**Repository:** `Kedar-Joshi07/IPSP`  
**Initial required starting SHA:** `7fdfd1d97bc5d34ea29f2cb52e5c22bf2a7d5cfd`  
**Current accepted application foundation:** `v0.1.0` — formally accepted  
**Target reconciliation release:** `v0.1.1`  
**Following capability milestone:** `v0.2.0` — Data Ingestion, Storage & Provenance — **NOT STARTED**  
**Architecture freeze:** `F-002`

---

# 0. How to use this prompt pack

This file contains the complete F-002 reconciliation sequence. Execute **one phase at a time**.

Do not paste the entire pack into Codex as one implementation request.

For every phase after F2-A:

1. wait until the previous phase is completed and reviewed;
2. record the accepted commit SHA;
3. replace the placeholder `<<PREVIOUS_ACCEPTED_SHA>>` in the next prompt with that SHA;
4. start from a clean tracked worktree;
5. execute only that phase;
6. run the phase-specific gates;
7. review the diff before accepting the phase;
8. do not begin the next phase automatically.

The intended sequence is:

```text
v0.1.0 ACCEPTED FOUNDATION
        ↓
F2-A  Architecture Authority + Version/Roadmap Freeze
        ↓
F2-B  Product / Core Architecture / Structure Reconciliation
        ↓
F2-C  Data / Semantics / Metrics / Domain Experience Contracts
        ↓
F2-D  Capability / Engine / License / Modeling Contracts
        ↓
F2-E  Simulation / Composite / Finance / Trust / Evidence Contracts
        ↓
F2-F  Learning / Outcome Reconciliation / LLM / Evidence Access Contracts
        ↓
F2-G  UI / API / Storage / Jobs / Security / Operations Reconciliation
        ↓
F2-H  Flows / Tests / Acceptance / Governance / Agent Instructions
        ↓
F2-I  v0.1.1 Production Reconciliation
        ↓
F2-J  Independent F-002 + v0.1.1 Final Acceptance Audit
        ↓
v0.1.1 ACCEPTED
        ↓
v0.2.0 CONTRACT FREEZE MAY BEGIN
```

No phase in this pack authorizes v0.2 implementation.

---

# 1. Program-wide frozen rules

These rules apply to every F-002 phase.

## 1.1 Preserve accepted history

The following historical fact must not be rewritten:

```text
Phase 1 / IPSP v0.1.0 foundation
FORMALLY ACCEPTED
Independent Phase 1L.1 final review: PASS
Accepted foundation SHA:
cd0dca48ded8d68f18e861f2427dfeb746d52ea7
```

F-002 is a new architecture freeze and reconciliation program. It does not retroactively make the original v0.1.0 acceptance incorrect.

## 1.2 F-002 is not application v2.0

Keep four version concepts separate:

- Architecture Freeze: `F-002`
- Application Version: `v0.1.0`, `v0.1.1`, `v0.2.0`, ...
- Development Phase / Work Package: `F2-A`, `F2-B`, ...
- Contract Version: API, Semantic Manifest, Domain Experience, Metric definitions, etc.

Use semantic versioning for the application.

## 1.3 No v0.2 contamination

Until F2-J passes, do not implement:

- dataset/project ingestion tables;
- upload endpoints;
- canonical Parquet processing;
- profiling engines;
- semantic inference runtime;
- model training runtime;
- simulation runtime;
- Domain Experience runtime execution beyond small foundation interfaces explicitly authorized in F2-I;
- Cross-Domain execution runtime;
- learning runtime;
- new v0.2 capability APIs.

F-002 reconciliation prepares the foundation and contracts. It does not skip ahead.

## 1.4 Domain neutrality

The IPSP core must remain domain-neutral.

Never solve F-002 by scattering branches such as:

```python
if domain == "marketing":
    ...
if domain == "finance":
    ...
if domain == "product":
    ...
```

Domain knowledge belongs in registered Domain Experience definitions, metric definitions, provider/engine registries, organization configuration, benchmark fixtures, or explicit domain modules that obey generic interfaces.

## 1.5 AI authority boundary

Preserve:

```text
AI proposes.
Evidence validates.
Rules constrain.
Models compete.
Humans arbitrate exceptions.
The system remembers the outcome.
```

LLMs never become the numerical authority.

## 1.6 Simulation truth boundary

Preserve exactly three simulation bases:

- `DATA_BASED`
- `MIXED`
- `INTENT_BASED`

Do not create another canonical simulation basis.

Every simulation may become a learning experience. Not every simulation becomes empirical truth.

## 1.7 Provider neutrality

Application services request capabilities, not vendor packages.

Use provider/registry abstractions for:

- synthetic data;
- optimization;
- LLMs;
- ML/statistical engines where appropriate;
- evidence sources.

Do not make SDV, LightGBM, QuantLib, llama.cpp, CVXPY, or another implementation the architecture itself.

## 1.8 Licensing is an executable governance concern

Keep implementation/library licensing separate from algorithmic ideas.

Track dependency licenses, solver licenses, provider restrictions, model-weight licenses, commercial-use restrictions, and deployment/service restrictions independently.

## 1.9 Stop on unresolved architecture conflict

If a phase discovers a genuine contradiction not resolved by:

1. F-002 master freeze;
2. F-002 roadmap freeze;
3. `docs/00_SCOPE_FREEZE.md` after F2-A;
4. `docs/32_DECISION_LOG.md` after F2-A;

then do not invent a solution.

Report the conflict with:

- files involved;
- exact conflicting statements;
- implementation consequence;
- recommended owner decision.

Stop that phase.

## 1.10 Preserve unrelated user work

Do not reset, overwrite, delete, or reformat unrelated user-owned changes.

If the tracked worktree is unexpectedly dirty, identify the files and stop before editing shared files unless the changes are clearly part of the authorized phase.

---

# 2. F-002 frozen architecture payload

The F-002 master freeze created in F2-A must encode the following decisions.

## 2.1 Canonical IPSP identity

IPSP is a domain-adaptive, dataset-agnostic, evidence-aware platform for:

- understanding;
- analysis;
- diagnosis;
- prediction;
- forecasting;
- simulation;
- optimization where valid;
- trust/evidence assessment;
- comparison/reproducibility;
- governed learning.

IPSP is not a dashboard generator, fixed Marketing simulator, fixed Finance simulator, AutoML wrapper, chatbot, synthetic-data generator, or financial calculator.

## 2.2 Canonical product lifecycle

```text
DATA
  ↓
UNDERSTANDING
  ↓
SEMANTIC CONTRACT
  ↓
DOMAIN / CROSS-DOMAIN ACTIVATION
  ↓
CAPABILITY DISCOVERY
  ↓
ANALYSIS / DIAGNOSIS
  ↓
MODEL + ENGINE SELECTION
  ↓
SIMULATION / OPTIMIZATION
  ↓
TRUST + EVIDENCE
  ↓
RESULTS / COMPARISON
  ↓
SCENARIO & EXPERIENCE MEMORY
  ↓
GOVERNED LEARNING
  ↓
BETTER FUTURE MODELS / LOCAL AI
```

Unsupported paths may be limited, blocked, disabled, or refused with reasons.

## 2.3 Domain families

Frozen first-class families:

- Marketing
- Product
- Sales
- Customer Experience
- Finance
- Operations / Demand
- Generic / Custom
- Composite / Cross-Domain

A dataset may activate one or several domains.

## 2.4 Domain Experience Packs

Core remains domain-agnostic. Domain Experience Packs may provide:

- terminology;
- objective taxonomy;
- semantic concept catalogs;
- metric requests;
- control templates;
- UI metadata/templates;
- recommended analysis sections;
- comparison views;
- explanation vocabulary;
- optional benchmark knowledge;
- semantic/capability prerequisites.

They must not define generic numerical truth, mandatory physical columns, hardcoded model winners, or guaranteed responses.

Catalog precedence:

1. organization-configured;
2. observed/confirmed dataset values;
3. curated Domain Experience Pack;
4. custom user assumption.

## 2.5 Metric & Formula Registry

Domain Packs request semantic metric IDs. Numerical truth belongs in a versioned Metric & Formula Registry.

Each metric definition conceptually includes:

- metric ID;
- version;
- semantic inputs;
- formula;
- aggregation semantics;
- time semantics;
- unit/currency semantics;
- null behavior;
- required grain;
- validation tests;
- source/provenance.

`Domain Pack != Formula Engine`.

## 2.6 CrossDomainSemanticGraph

Cross-domain relationships must represent:

- source concept;
- target concept;
- entity relationship;
- time relationship;
- grain relationship;
- unit relationship;
- currency relationship;
- transformation;
- evidence;
- support status.

Inference remains:

```text
infer → validate → confirm if ambiguous → persist
```

No arbitrary joins.

## 2.7 ScenarioIntentManifest

Conceptually records:

- domain(s);
- objective;
- outcome;
- horizon;
- geography;
- population/entity;
- resources;
- goals;
- controls;
- constraints;
- assumptions;
- comparison basis;
- uncertainty preference;
- evidence access;
- consent snapshot.

## 2.8 CompositeSimulationGraph

Universal execution abstraction.

Node families may include:

- deterministic formula;
- statistical model;
- ML model;
- time-series model;
- causal model;
- Monte Carlo;
- optimizer;
- synthetic support/generator;
- benchmark;
- analog;
- external evidence transform;
- user assumption;
- constraint.

Edges must explicitly distinguish:

- deterministic relation;
- observed association;
- predictive relation;
- causal estimate;
- assumption;
- external prior;
- analog prior;
- constraint.

No defensible relation = constrain or refuse.

## 2.9 Cross-Domain Composite

Representative examples only:

```text
Marketing spend → response → leads → opportunities → orders → revenue → margin → cash
Product launch/price → demand → inventory → fulfilment → cost → margin → working capital
CX/service → satisfaction/sentiment → retention/churn → renewal → revenue/customer value
```

These are not guaranteed or hardcoded paths.

## 2.10 Engine / License architecture

Introduce:

- `EngineRegistry`
- `LicenseRegistry`
- `EngineResolver`

Organization modes:

- `OPEN_SOURCE_ONLY`
- `OPEN_SOURCE_PREFERRED` — default
- `COMMERCIAL_ALLOWED`

License classes:

- `PERMISSIVE_OPEN_SOURCE`
- `PUBLIC_DOMAIN`
- `COPYLEFT_OPEN_SOURCE`
- `SOURCE_AVAILABLE`
- `COMMERCIAL`
- `CUSTOM_MODEL_LICENSE`
- `UNKNOWN/BLOCKED`

Resolver priority:

1. capability validity;
2. license policy;
3. Trust/validation;
4. data suitability;
5. performance;
6. resources;
7. organization preference.

## 2.11 Open-source-first architecture candidates

Do not imply installation unless a milestone actually installs them.

Application/data:
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Polars
- Arrow/PyArrow
- Pandas where needed
- Plotly.js

ML:
- scikit-learn
- LightGBM
- XGBoost
- CatBoost

Statistics/econometrics:
- Statsmodels
- arch
- PyMC where justified

Causal:
- DoWhy
- EconML
- optional causal-learn

Explainability/tuning:
- SHAP
- Optuna

Synthetic:
- Synthcity preferred permissive candidate
- SDV optional subject to current license policy

Optimization:
- CVXPY abstraction
- OSQP
- SCS
- optional commercial solvers

Finance:
- QuantLib only for optional instrument/quant subpack
- arch where justified

Incremental:
- River only where true streaming semantics justify it

Local AI:
- llama.cpp
- Transformers
- PEFT/LoRA
- optional MLflow

Model-weight licenses are independently gated.

## 2.12 Model selection

No universal best model.

Meaningful baselines are mandatory.

Selection depends on semantic fit, data, sample size, horizon, temporal structure, explainability, uncertainty, compute, license policy, and comparative validation.

Preserve:

```text
correlation != prediction != attribution != causation
```

## 2.13 Finance family

Finance is dynamically activated, not a mandatory schema.

Core families:

- Corporate Performance / FP&A;
- forecasting;
- Treasury & Liquidity;
- three-statement relationships;
- Risk & Stress;
- Credit / Collections;
- Valuation / Capital Investment;
- optional Quant Finance / Instruments.

Optimization is separated from prediction and simulation.

## 2.14 Trust and Evidence Profile

Trust remains separate from Evidence Profile.

Expanded Trust dimensions include:

- data;
- semantic;
- relationships;
- model;
- temporal leakage;
- extrapolation;
- constraints;
- accounting reconciliation;
- unit/currency/time consistency;
- simulation support;
- optimization feasibility;
- privacy;
- outbound policy;
- license;
- reproducibility.

Evidence Profile describes dependence on observed data, actual outcomes, assumptions, synthetic data, analogs, external evidence, extrapolation, freshness, and coverage.

## 2.15 Provenance

Conceptual classes:

- `OBSERVED_DATA`
- `DERIVED_DATA`
- `ORGANIZATION_CONFIG`
- `DOMAIN_CATALOG`
- `USER_ASSUMPTION`
- `PRIOR_IPSP_RUN`
- `OBSERVED_OUTCOME`
- `CURATED_BENCHMARK`
- `EXTERNAL_EVIDENCE`
- `LOCAL_KNOWLEDGE_BASE`
- `LLM_PROPOSAL`
- `SYNTHETIC_DATA`

Synthetic provenance must retain generator/provider/version/seed/configuration/quality/privacy metadata.

## 2.16 Governed learning

Core rule:

```text
Every simulation becomes a learning experience;
not every simulation becomes empirical truth.
```

Introduce conceptually:

- `SimulationLearningStore`
- `OutcomeReconciliation`
- `LearningEligibilityGate`
- governed Training Dataset Builder
- champion/challenger promotion

Lifecycle:

```text
Simulation T0
  ↓
Actual outcome T1
  ↓
Prediction vs actual
  ↓
Error attribution
  ↓
Model / assumption / evidence evaluation
  ↓
Learning candidate
```

Do not directly retrain from one simulation.

## 2.17 LLM architecture

Preserve exact modes:

- `ML_ONLY`
- `LOCAL_LLM`
- `REMOTE_LLM`
- `HYBRID_LLM`

Evidence access modes:

- `OFF`
- `INTERNAL_ONLY`
- `PUBLIC_WEB`
- `APPROVED_CONNECTORS`

Effective outbound permission:

```text
Admin policy ∩ project/dataset policy ∩ runtime user consent
```

Continuous retrieval/memory is preferred before weight adaptation.

Optional PEFT/LoRA adaptation must use curated, governed learning events.

## 2.18 UI architecture

Top-level target navigation:

- Home / Overview
- Projects / Workspaces
- Data
- Analysis & Simulation
  - Marketing
  - Product
  - Sales
  - Customer Experience
  - Finance
  - Operations
  - Generic / Custom
  - Composite / Cross-Domain
- Scenario Library
- Compare
- Models & Learning
- Jobs
- Administration
- Profile

Five-step simulation workflow remains exactly:

1. Define
2. Configure
3. Enrich & Validate
4. Run
5. Results & Compare

CampaignSim remains a historical visual-design reference, not the product identity.

## 2.19 Backend architecture

Conceptual direction:

```text
Adaptive Frontend
  ↓
FastAPI / API
  ↓
Auth / RBAC / Policy / Consent
  ↓
Ingestion / Storage
  ↓
Data Understanding
  ↓
Semantic + Metric Layer
  ↓
Domain Experience Activation
  ↓
Cross-Domain Composition
  ↓
Capability Discovery
  ↓
Scenario + Evidence
  ↓
Engine & License Resolver
  ↓
Composite Simulation Graph
  ↓
Trust + Evidence Profile
  ↓
Results / Compare / History / Export
  ↓
Learning / Reconciliation
  ↓
Model + Local-AI Improvement
```

Storage remains two-plane:

- SQLite = control/governance/knowledge metadata;
- Source/Parquet = analytical data.

## 2.20 v1.0 boundary

v1.0 means the first complete, production-usable expression of IPSP, not every future capability.

Advanced causal production workflows, advanced optimization, automatic LLM fine-tuning, Remote/Hybrid LLM, PUBLIC_WEB evidence, enterprise connectors, enterprise distributed scale, and advanced Quant Finance do not have to block v1.0 if their architecture contracts are preserved.

---

# 3. Frozen application roadmap

F2-A must make the following roadmap authoritative:

| Version | Scope |
|---|---|
| v0.1.0 | Accepted foundation/security/repository shell |
| v0.1.1 | F-002 architecture reconciliation |
| v0.2.0 | Data ingestion, storage & provenance |
| v0.3.0 | Deterministic data understanding & relationships |
| v0.4.0 | Semantic intelligence & Dataset Semantic Manifest |
| v0.5.0 | Metric & Formula Registry + Domain Experience foundation |
| v0.6.0 | Capability Discovery + Engine/License Registry |
| v0.7.0 | Core modelling + model lifecycle |
| v0.8.0 | Simulation core + ScenarioIntentManifest + CompositeSimulationGraph foundation |
| v0.9.0 | Trust + Evidence + history + comparison |
| v0.10.0 | Cross-Domain Composite intelligence |
| v0.11.0 | Domain intelligence completion |
| v0.12.0 | Learning + Outcome Reconciliation foundation |
| v0.13.0 | Local AI |
| v0.14.0 | Full dynamic product UI |
| v0.15.0 | v1.0 release candidate / hardening |
| v1.0.0 | First General Availability release |

Tentative post-v1.0 direction:

- v1.1 — Advanced Learning & Decision Intelligence
- v1.2 — Causal & Optimization Intelligence
- v1.3 — External Intelligence
- v1.4 — Enterprise Integrations
- v1.5 — Enterprise Scale

Do not pre-assign v2.0.

---

# PHASE F2-A PROMPT
# Architecture Authority + Version / Development Roadmap Freeze

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting SHA:** `7fdfd1d97bc5d34ea29f2cb52e5c22bf2a7d5cfd`

This task is **F2-A only**.

Its purpose is to establish F-002 as formal repository architecture authority and freeze the revised product-version/development roadmap before any broader specification reconciliation or production changes.

Do not begin F2-B.
Do not modify production code.
Do not begin v0.2.
Do not create a Git tag or GitHub release.

## A1. Preflight

Read completely:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `FILE_INDEX.md`
- `README.md`
- `docs/00_SCOPE_FREEZE.md`
- `docs/01_PROJECT_SPEC.md`
- `docs/02_PRODUCT_REQUIREMENTS.md`
- `docs/03_ARCHITECTURE.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/33_OPEN_QUESTIONS.md`
- `docs/40_ANTI_CONTAMINATION.md`
- `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`
- `prompts/PHASED_COPILOT_PROMPTS.md`
- every file under `flows/`

Then inspect the full Markdown index for conflicting roadmap/architecture authority.

Before editing:

```text
git status --short
git rev-parse HEAD
git log -1 --oneline
```

Required SHA:

```text
7fdfd1d97bc5d34ea29f2cb52e5c22bf2a7d5cfd
```

If HEAD differs, stop and report the SHA and changed commits before proceeding.

## A2. Create F-002 master freeze

Create:

```text
docs/44_F002_ARCHITECTURE_FREEZE.md
```

This becomes the authoritative architecture extension/reconciliation document.

It must contain, in durable specification form, every frozen item in section **2. F-002 frozen architecture payload** of this prompt pack.

It must explicitly state:

- F-002 extends/supersedes conflicting prior architecture wording;
- v0.1.0 implementation history remains accepted;
- F-002 is planned architecture until relevant milestones implement it;
- no future capability may be advertised as implemented merely because it is frozen;
- all generic core behavior remains dataset/domain agnostic;
- Domain Experience Packs extend the core rather than fork it;
- three simulation bases remain exact;
- provider/license boundaries are mandatory;
- learning evidence tiers prevent circular contamination;
- Cross-Domain relationships require evidence and reconciliation;
- v1.0 scope is bounded.

Include a compact decision-ID table for the major F-002 decisions.

Suggested IDs may use a consistent `F002-Dxxx` scheme.

Do not reuse old decision IDs in a way that changes their historical meaning.

## A3. Create product-version and roadmap freeze

Create:

```text
docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md
```

Freeze:

- Architecture Freeze vs Application Version vs Development Phase vs Contract Version;
- semantic-versioning rules;
- v0.1.1 reconciliation meaning;
- complete v0.2.0 → v1.0.0 roadmap from section 3;
- what v1.0 means;
- what is explicitly deferred post-v1.0;
- tentative v1.1 → v1.5 direction;
- major-version rule;
- future independent Domain Experience versioning compatibility;
- development flow:

```text
Architecture Authority
  ↓
Milestone Scope
  ↓
Contract Freeze
  ↓
Dependency / License Review
  ↓
Workstream Split
  ↓
Feature Branches
  ↓
Unit / Security / Contract Tests
  ↓
Integration Branch
  ↓
Integration Tests
  ↓
Architecture Conformance
  ↓
Independent Review
  ↓
Release Candidate
  ↓
Acceptance Gate
  ↓
main
  ↓
Version Tag
```

Before implementation of every milestone, require freezes for:

1. functional contract;
2. data/schema contract;
3. API/interface contract;
4. acceptance contract;
5. dependency/license contract.

## A4. Make authority unambiguous

Update:

```text
docs/00_SCOPE_FREEZE.md
docs/32_DECISION_LOG.md
```

Do not rewrite their history.

Add an explicit authority statement equivalent to:

```text
For architecture/product-development decisions approved after the v0.1.0
foundation, F-002 and the Product Version & Development Roadmap Freeze are
authoritative. Where older target-architecture wording conflicts, F-002 wins.
Historical v0.1.0 implementation/acceptance facts remain unchanged.
```

Update the source-priority wording only as much as necessary to remove ambiguity.

## A5. Update agent authority pointers

Update only the authority/source-of-truth sections of:

```text
AGENTS.md
.github/copilot-instructions.md
```

At this phase do not perform the full F-002 instruction rewrite; that occurs in F2-H.

The immediate requirement is that future agents cannot legally follow a superseded old architecture over F-002.

Add F-002 and the roadmap freeze to required-reading/source-priority rules.

Preserve all existing security, anti-contamination, coding, branch, migration, and stop-on-conflict rules.

## A6. Index and progress

Update:

```text
FILE_INDEX.md
docs/31_IMPLEMENTATION_PROGRESS.md
```

Add both new F-002 documents to the index.

In progress, preserve v0.1.0 accepted history and add a new section/row:

```text
v0.1.1 — F-002 Architecture Reconciliation
Status: IN PROGRESS — F2-A authority/roadmap freeze
```

State explicitly:

```text
v0.2.0 — NOT STARTED
```

Do not mark v0.1.1 accepted.

## A7. Conflict inventory

Create a temporary internal checklist while reviewing all current specs/flows. Do not create dozens of speculative documents.

In the final report list files that are known to contain superseded target wording, including at least where found:

- old roadmap milestones;
- CampaignSim-as-product identity;
- SDV-specific synthetic architecture;
- old KPI-only metric architecture;
- old simulation-engine classification;
- missing Domain Experience architecture;
- missing Engine/License Registry;
- missing Cross-Domain graph;
- missing governed-learning architecture;
- missing Finance scope;
- old LLM milestone schedule.

Do not fix all of them in F2-A.

## A8. F2-A stop rule

Expected production changes:

```text
NONE
```

Do not change:

- `backend/ipsp/**`
- `frontend/**`
- `database/migrations/**`
- `pyproject.toml`
- `requirements.lock`

If establishing F-002 authority appears to require production changes, stop. That work belongs to F2-I.

## A9. Validation

Run at minimum:

```text
git diff --check
```

Validate:

- all new relative Markdown links;
- Markdown tables;
- Mermaid blocks if added;
- no conflicting authority statement remains in the files changed in this phase;
- no production code changed;
- v0.1.0 history remains intact;
- v0.2 remains not started.

Run the architecture conformance test subset if it can execute without requiring unrelated production changes.

## A10. Expected diff boundary

Expected changed/created files should be limited to:

```text
docs/44_F002_ARCHITECTURE_FREEZE.md
docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md
docs/00_SCOPE_FREEZE.md
docs/32_DECISION_LOG.md
AGENTS.md
.github/copilot-instructions.md
FILE_INDEX.md
docs/31_IMPLEMENTATION_PROGRESS.md
```

If another file must change, justify it explicitly before editing it.

## A11. Mandatory final report

Return:

### A. Starting state
SHA, branch, git status.

### B. Files created
Every created file.

### C. Files modified
Every modified file.

### D. F-002 authority
Explain the new source-of-truth chain.

### E. Architecture decisions frozen
Summarize all major F-002 decision groups.

### F. Versioning / roadmap frozen
Report complete pre-v1.0 sequence and v1.0 boundary.

### G. Historical preservation
Confirm v0.1.0 acceptance was not rewritten.

### H. Known reconciliation inventory
List stale files/areas left for F2-B onward.

### I. Production changes
Expected: `None`.

### J. v0.2 state
Expected: `NOT STARTED`.

### K. Validation
Report diff/link/Markdown/conformance results.

### L. Deviations
If none: `None`.

### M. Gate result

End exactly with one:

`F2-A: PASS — F-002 architecture authority and development roadmap frozen; proceed only after independent review`

or

`F2-A: FAIL — F-002 authority/roadmap freeze incomplete; do not proceed`

Do not begin F2-B.

---

# PHASE F2-B PROMPT
# Product / Core Architecture / Project Structure Reconciliation

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-B only**.

F2-A must already be accepted.

Read first:

- `docs/44_F002_ARCHITECTURE_FREEZE.md`
- `docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md`
- `docs/00_SCOPE_FREEZE.md`
- `docs/32_DECISION_LOG.md`
- `README.md`
- `docs/01_PROJECT_SPEC.md`
- `docs/02_PRODUCT_REQUIREMENTS.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`
- `docs/38_GLOSSARY.md`
- `docs/33_OPEN_QUESTIONS.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Expected SHA must exactly match the accepted F2-A SHA.

## B1. Reconcile project definition

Update:

```text
docs/01_PROJECT_SPEC.md
docs/02_PRODUCT_REQUIREMENTS.md
```

Ensure they now reflect:

- domain-adaptive product identity;
- structured/tabular core scope;
- Domain Experience Packs;
- Composite/Cross-Domain as first-class;
- provider-neutral engines;
- Trust + Evidence distinction;
- governed learning;
- Finance as a domain family;
- v1.0 bounded definition;
- current implementation vs target state.

Do not turn these documents into implementation plans.

## B2. Reconcile architecture

Update:

```text
docs/03_ARCHITECTURE.md
```

Make the target architecture explicitly show:

```text
Frontend
→ API/Auth/Policy/Consent
→ Ingestion/Storage
→ Data Understanding
→ Semantic + Metric
→ Domain Experience
→ Cross-Domain Composition
→ Capability Discovery
→ Scenario/Evidence
→ Engine/License Resolver
→ Composite Simulation Graph
→ Trust + Evidence Profile
→ Results/History/Export
→ Learning/Reconciliation
```

Keep cross-cutting:

- security;
- privacy;
- provenance;
- licensing;
- observability;
- jobs;
- reproducibility;
- configuration/secrets/outbound.

Preserve two-plane storage.

## B3. Reconcile project structure

Update:

```text
docs/04_PROJECT_STRUCTURE.md
```

Do not claim target directories already exist.

Remove vendor-specific target structure such as `artifacts/sdv`.

Prefer provider-neutral conceptual targets such as:

```text
artifacts/models
artifacts/manifests
artifacts/reports
artifacts/simulations
artifacts/synthetic
artifacts/evidence
```

Future engine/provider structure may conceptually include:

```text
engines/
  ml/
  statistics/
  synthetic/
  optimization/
  finance/
```

but only as planned structure.

Preserve canonical ORM/API/repository ownership.

## B4. Reconcile glossary and open questions

Update:

```text
docs/38_GLOSSARY.md
docs/33_OPEN_QUESTIONS.md
```

Add/clarify terms:

- F-002;
- Domain Experience Pack;
- Domain Experience Manifest;
- CrossDomainSemanticGraph;
- Metric & Formula Registry;
- EngineRegistry;
- LicenseRegistry;
- EngineResolver;
- ScenarioIntentManifest;
- CompositeSimulationGraph;
- Evidence Profile;
- SimulationLearningStore;
- OutcomeReconciliation;
- observed outcome;
- synthetic provenance;
- evidence access mode.

Remove questions already resolved by F-002 from the unresolved list, while preserving genuinely unresolved milestone-timing/implementation-detail questions.

Do not invent implementation details merely to close an open question.

## B5. Architecture-ready future schema/API wording

Review `docs/27_SQLITE_SCHEMA_SPEC.md` and `docs/28_REST_API_CONTRACT.md` for direct contradictions with the newly reconciled architecture.

In F2-B, make only high-level vocabulary/ownership corrections needed to prevent contradiction.

Detailed schema/API reconciliation is F2-G.

## B6. Progress

Update `docs/31_IMPLEMENTATION_PROGRESS.md` with F2-B status and evidence.

Do not advance v0.1.1 to accepted.

## B7. Tests / gates

Run:

```text
git diff --check
```

Validate all changed Markdown links and Mermaid syntax.

Run architecture-conformance tests.

Expected production changes: none.

## B8. Final report

Report:

- starting SHA;
- files changed;
- product-definition changes;
- architecture-layer changes;
- project-structure changes;
- glossary/open-question reconciliation;
- deferred schema/API work;
- production changes: `None`;
- v0.2: `NOT STARTED`;
- validation;
- deviations.

End exactly:

`F2-B: PASS — core product and architecture specifications reconciled to F-002; proceed only after independent review`

or

`F2-B: FAIL — core product/architecture reconciliation incomplete; do not proceed`

Do not begin F2-C.

---

# PHASE F2-C PROMPT
# Data / Semantics / Metric & Formula / Domain Experience Contract Freeze

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-C only**.

Read the accepted F-002 authority documents first, then:

- `docs/07_DATA_UNDERSTANDING_SPEC.md`
- `docs/08_SEMANTIC_MODEL_SPEC.md`
- `docs/09_RELATIONSHIPS_HIERARCHY_LINEAGE_SPEC.md`
- `docs/10_KPI_METRIC_DEPENDENCY_SPEC.md`
- `docs/11_CAPABILITY_DISCOVERY_SPEC.md`
- `docs/39_BENCHMARK_CATALOG.md`
- `docs/40_ANTI_CONTAMINATION.md`
- relevant data/semantic flows.

## C1. Preserve deterministic understanding boundary

Reconcile `docs/07_DATA_UNDERSTANDING_SPEC.md` without adding runtime code.

Ensure the Data Intelligence Packet and profiling contracts can support:

- entities;
- grain;
- identifiers;
- measures/dimensions;
- time/business calendars;
- units/currencies;
- plan/actual/forecast semantics;
- sensitivity;
- provenance;
- observation maturity;
- availability time;
- relationship evidence;
- future Domain Experience activation.

Do not require domain-specific columns.

## C2. Reconcile Semantic Manifest

Update `docs/08_SEMANTIC_MODEL_SPEC.md` so the Semantic Manifest is capable of feeding:

- Metric & Formula Registry;
- Domain Experience activation;
- CrossDomainSemanticGraph;
- Capability Discovery;
- Scenario Intent;
- Trust/Evidence;
- learning eligibility.

Preserve ambiguity → clarification → confirmation → new version behavior.

## C3. Reconcile relationships/lineage

Update `docs/09_RELATIONSHIPS_HIERARCHY_LINEAGE_SPEC.md`.

Preserve existing structural/identity/temporal/lifecycle/hierarchy/plan-vs-actual/commercial-flow concepts.

Add architecture requirements for cross-domain reconciliation of:

- entity grain;
- aggregation grain;
- time zone;
- calendar/fiscal periods;
- currency;
- units.

Do not implement arbitrary joins.

## C4. Create Metric & Formula Registry specification

Create:

```text
docs/46_METRIC_FORMULA_REGISTRY_SPEC.md
```

Specify:

- metric definition identity/versioning;
- semantic inputs;
- formula representation;
- dependency graph;
- aggregation semantics;
- time semantics;
- grain;
- currency/unit behavior;
- null/safe-division behavior;
- validation tests;
- lineage/provenance;
- domain requests vs generic calculation;
- organization overrides/configuration precedence;
- conflict/version behavior;
- reproducibility references.

Reconcile `docs/10_KPI_METRIC_DEPENDENCY_SPEC.md` as the dependency/evaluation subset of the broader registry rather than deleting its useful prior logic.

## C5. Create Domain Experience specification

Create:

```text
docs/47_DOMAIN_EXPERIENCE_PACK_SPEC.md
```

Specify a provider/registry-style architecture for:

- DomainExperience;
- DomainExperienceManifest;
- DomainExperienceRegistry;
- activation evidence;
- semantic concept catalogs;
- objective taxonomy;
- UI metadata;
- metric IDs requested;
- capability hints;
- constraint templates;
- terminology/explanation vocabulary;
- optional benchmark catalogs;
- required semantic prerequisites;
- versioning;
- organization override precedence.

Freeze domain families:

- Marketing;
- Product;
- Sales;
- Customer Experience;
- Finance;
- Operations / Demand;
- Generic / Custom;
- Composite / Cross-Domain.

Include a baseline catalog table showing representative concepts for each domain, clearly as examples rather than mandatory schema.

## C6. Create Cross-Domain semantic contract

Within the Domain Experience spec or a dedicated section, define `CrossDomainSemanticGraph` fully.

Do not yet create simulation execution rules; that is F2-E.

## C7. Anti-contamination update

Update `docs/40_ANTI_CONTAMINATION.md` so it explicitly allows domain-specific knowledge in registered Domain Experience definitions while prohibiting it from generic core logic.

Benchmark examples remain fixtures/reference knowledge, not runtime truth.

## C8. Index / progress

Update:

- `FILE_INDEX.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`

## C9. Stop rule

Production code changes: none.

No new database migration.
No new dependency.
No v0.2 implementation.

## C10. Validation

Run Markdown/link/diff checks and architecture-conformance tests.

Perform a static search showing that the newly written contracts do not require fixed physical column names for any domain.

## C11. Final report

Report:

- files created/modified;
- Semantic Manifest changes;
- relationship changes;
- Metric Registry contract;
- Domain Experience contract;
- Cross-Domain semantic contract;
- anti-contamination result;
- production/schema/dependency changes: `None`;
- v0.2 state;
- validation.

End exactly:

`F2-C: PASS — semantic, metric, and Domain Experience contracts frozen under F-002; proceed only after independent review`

or

`F2-C: FAIL — semantic/domain contract freeze incomplete; do not proceed`

Do not begin F2-D.

---

# PHASE F2-D PROMPT
# Capability / Engine / License / Modeling Architecture Reconciliation

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-D only**.

Read:

- F-002 authority/roadmap;
- `docs/11_CAPABILITY_DISCOVERY_SPEC.md`;
- `docs/12_MODELING_ENGINE_SPEC.md`;
- `docs/13_MODEL_REGISTRY_LIFECYCLE_SPEC.md`;
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`;
- `docs/35_CONFIGURATION_SPEC.md`;
- new Metric/Domain Experience specs from F2-C.

## D1. Reconcile Capability Discovery

Update `docs/11_CAPABILITY_DISCOVERY_SPEC.md`.

Separate clearly:

```text
What is semantically/data-valid?
        ↓
What engine families can perform it?
        ↓
Which installed/allowed provider is eligible?
```

Capability Discovery must not select a vendor simply because it is installed.

Add/clarify capability families for:

- descriptive/diagnostic;
- regression/classification/count;
- forecasting;
- similarity/look-alike;
- clustering/segmentation;
- deterministic what-if;
- sensitivity;
- Monte Carlo;
- synthetic-assisted workflows;
- risk/stress;
- optimization where supported;
- causal where supported;
- Composite/Cross-Domain where supported.

Preserve reasoned refusal.

## D2. Create Engine + License Registry spec

Create:

```text
docs/48_ENGINE_LICENSE_REGISTRY_SPEC.md
```

Define:

- EngineRegistry;
- LicenseRegistry;
- EngineResolver;
- provider interfaces;
- engine capability metadata;
- installed/available status;
- hardware requirements;
- security restrictions;
- dependency license;
- model-weight license;
- solver/commercial license;
- commercial-use status;
- redistribution/service restrictions;
- organization policy modes;
- ALLOW/WARN/BLOCK license gate;
- resolver priority.

Include provider examples without making them mandatory runtime dependencies.

Synthetic provider examples must use Synthcity as preferred permissive candidate and SDV as optional subject to licensing policy.

## D3. Reconcile modeling engine

Update `docs/12_MODELING_ENGINE_SPEC.md`.

Freeze baseline-first candidate competition.

Include candidate families without declaring universal winners.

Require:

- time-aware validation for temporal problems;
- leakage checks;
- calibration where probability is surfaced;
- explainability where required;
- license/provider eligibility before training;
- resource suitability;
- Trust validation.

Preserve distinction among score, probability, ranking, business rule, predictive association, causal estimate.

## D4. Reconcile model registry lifecycle

Update `docs/13_MODEL_REGISTRY_LIFECYCLE_SPEC.md`.

Retain:

- TRAINING;
- CANDIDATE;
- CHALLENGER;
- CHAMPION;
- REJECTED;
- ARCHIVED.

Expand metadata conceptually for:

- engine/provider;
- library version;
- dependency license;
- model-weight license where relevant;
- dataset/semantic/metric versions;
- feature lineage;
- horizon;
- calibration;
- explainability;
- Trust;
- promotion evidence.

Do not implement model runtime.

## D5. Causal boundary

Explicitly freeze:

```text
correlation != prediction != attribution != causal effect
```

Causal activation requires treatment/outcome/confounders/identification assumptions and validation/refutation support.

DoWhy/EconML are architecture candidates, not v0.1.1 dependencies.

## D6. Optimization boundary

Optimization is not prediction.

Freeze CVXPY abstraction + OSQP/SCS preferred open-source providers conceptually.

Commercial solvers remain optional and license-gated.

Do not implement optimization runtime.

## D7. Technical-stack/license documentation

Update relevant target-stack wording in product/config docs without adding dependencies.

Create or reserve a later runtime inventory contract, but do not fabricate installed packages.

## D8. Progress/index

Update `FILE_INDEX.md` and implementation progress.

## D9. Validation

No production/schema/dependency changes.

Run docs/link/diff and architecture tests.

Search for target documentation that still treats SDV as the generic synthetic architecture; report remaining occurrences assigned to later phases.

## D10. Final report

End exactly:

`F2-D: PASS — capability, engine, license, and modeling contracts reconciled to F-002; proceed only after independent review`

or

`F2-D: FAIL — capability/engine/model contract reconciliation incomplete; do not proceed`

Do not begin F2-E.

---

# PHASE F2-E PROMPT
# Simulation / Composite / Finance / Trust / Evidence Contract Freeze

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-E only**.

Read:

- F-002 master freeze;
- roadmap freeze;
- new Domain/Metric/Engine specs;
- `docs/14_SIMULATION_ENGINE_SPEC.md`;
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`;
- `docs/25_REPORTING_EXPORT_SPEC.md`;
- `docs/26_SIMULATION_HISTORY_REPRODUCIBILITY.md`;
- relevant flows.

## E1. Reconcile simulation basis

Update `docs/14_SIMULATION_ENGINE_SPEC.md`.

Make exact canonical bases:

- DATA_BASED
- MIXED
- INTENT_BASED

Old predictive/deterministic/benchmark/Monte-Carlo/synthetic concepts become engine/node patterns or evidence mechanisms, not competing top-level bases.

## E2. Freeze ScenarioIntentManifest

Specify the versioned ScenarioIntentManifest fields and lifecycle.

Include consent/evidence-access snapshot and assumptions.

Do not over-specify persistence tables yet.

## E3. Create Composite / Cross-Domain simulation spec

Create:

```text
docs/49_COMPOSITE_CROSS_DOMAIN_SIMULATION_SPEC.md
```

Freeze:

- CompositeSimulationGraph;
- node types;
- edge semantics;
- execution ordering/dependencies;
- graph validation;
- domain crossing;
- unit/currency/time/entity reconciliation;
- constraint nodes;
- assumption nodes;
- evidence references;
- failure/refusal behavior;
- deterministic/accounting reconciliation;
- reproducibility/versioning;
- support/extrapolation behavior.

No arbitrary graph edge may be invented to satisfy user intent.

## E4. Finance Domain Experience specification

Create:

```text
docs/50_FINANCE_DOMAIN_EXPERIENCE_SPEC.md
```

Finance is a Domain Experience family, not a separate hardcoded platform.

Cover dynamic activation for:

- Corporate Performance / FP&A;
- Actual/Budget/Forecast;
- variance;
- profitability/margin/contribution;
- rolling/scenario forecasts;
- Treasury & Liquidity;
- AR/AP and working capital;
- debt/interest/FX where data supports;
- three-statement relationships;
- Risk & Stress;
- Credit / Collections;
- Valuation / Capital Investment;
- optional Quant Finance subpack.

Define semantic prerequisites and examples, not mandatory physical columns.

Separate prediction, deterministic accounting logic, simulation, stress testing, and optimization.

## E5. Trust reconciliation

Update `docs/15_TRUST_AND_VALIDATION_SPEC.md`.

Add expanded F-002 dimensions and keep Green/Amber/Red conceptually.

Require accounting, unit, currency, time/calendar, license and reproducibility checks where applicable.

## E6. Evidence Profile

Define Evidence Profile separately from Trust.

It should describe composition/dependence of evidence, not produce a duplicate Trust score.

## E7. Provenance and synthetic boundary

Reconcile provenance definitions across relevant specs.

Add `SYNTHETIC_DATA` with generator/provider/version/seed/config/quality/privacy metadata.

Synthetic data never silently becomes observed truth.

## E8. Reproducibility

Update `docs/26_SIMULATION_HISTORY_REPRODUCIBILITY.md`.

Preserve:

- re-run = same intent using current eligible state;
- reproduce = original frozen versions/state.

Expand reproduction to include original evidence snapshot, metric definitions, engine/provider versions, graph version, assumptions, policy context where relevant.

## E9. Reporting/export

Update `docs/25_REPORTING_EXPORT_SPEC.md` only where necessary to represent Evidence Profile, Cross-Domain results, scenario basis, graph lineage, and Trust.

Do not implement exports.

## E10. Index/progress/validation

Update `FILE_INDEX.md` and progress.

No production code, migration or dependency changes.

Run docs/link/diff/conformance checks.

## E11. Final report

End exactly:

`F2-E: PASS — simulation, Composite/Cross-Domain, Finance, Trust, Evidence and reproducibility contracts frozen; proceed only after independent review`

or

`F2-E: FAIL — simulation/composite/trust contract freeze incomplete; do not proceed`

Do not begin F2-F.

---

# PHASE F2-F PROMPT
# Governed Learning / Outcome Reconciliation / LLM / Evidence Access Contract Freeze

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-F only**.

Read:

- F-002 authority documents;
- simulation/composite/trust specs;
- model registry;
- `docs/16_LLM_ARCHITECTURE.md`;
- `docs/17_PRIVACY_REMOTE_LLM_POLICY.md`;
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`;
- history/reproducibility specs.

## F1. Create governed learning specification

Create:

```text
docs/51_SIMULATION_LEARNING_OUTCOME_RECONCILIATION_SPEC.md
```

Freeze:

- SimulationLearningStore;
- separation from empirical analytical data;
- evidence-authority tiers;
- OutcomeReconciliation;
- LearningEligibilityGate;
- Training Dataset Builder;
- leakage/provenance validation;
- challenger evaluation;
- champion comparison;
- promotion/rejection;
- drift/stability/calibration/robustness considerations;
- user correction capture;
- actual-outcome matching;
- batch retraining as default;
- River only when streaming semantics justify it.

Explicitly forbid direct truth promotion of:

- intent-based outputs;
- mixed assumptions;
- synthetic records;
- LLM-proposed numbers;
- unverified external evidence.

## F2. Reconcile LLM architecture

Update `docs/16_LLM_ARCHITECTURE.md`.

Preserve exact modes:

- ML_ONLY
- LOCAL_LLM
- REMOTE_LLM
- HYBRID_LLM

Preserve LLM non-numerical authority.

Add:

- Domain Experience reasoning;
- intent parsing;
- analog ranking;
- evidence planning;
- scenario explanation;
- memory/retrieval;
- optional governed PEFT/LoRA adaptation;
- Local LLM registry metadata and model-weight license gate.

Do not require Remote LLM for v1.0.

## F3. Evidence access modes

Freeze exact modes:

- OFF
- INTERNAL_ONLY
- PUBLIC_WEB
- APPROVED_CONNECTORS

Effective permission:

```text
Admin policy ∩ project/dataset policy ∩ runtime user consent
```

Update privacy/outbound specs accordingly.

Do not imply web/connectors are implemented in v0.1.1.

## F4. Local AI learning boundary

Preferred order:

1. retrieval/memory;
2. curated training-event preparation;
3. optional PEFT/LoRA challenger;
4. evaluation;
5. promotion/rejection.

Fine-tuning never grants numerical authority.

## F5. Privacy and provenance

Ensure LLM training/retrieval artifacts preserve:

- source provenance;
- privacy classification;
- consent/policy;
- model-weight license;
- training snapshot/version;
- evaluation.

## F6. Progress/index

Update index and progress.

## F7. Stop rule / validation

No LLM package installation.
No runtime provider implementation.
No model download.
No Internet requirement.
No production/schema changes.

Run docs/link/diff/conformance gates.

## F8. Final report

End exactly:

`F2-F: PASS — governed learning, outcome reconciliation, LLM and evidence-access contracts frozen; proceed only after independent review`

or

`F2-F: FAIL — learning/LLM/evidence contract freeze incomplete; do not proceed`

Do not begin F2-G.

---

# PHASE F2-G PROMPT
# UI / API / Storage / Jobs / Security / Configuration / Operations Reconciliation

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-G only**.

This phase reconciles platform contracts around F-002. It still does not implement v0.2 or later engines.

Read F-002 authority plus:

- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `docs/20_INGESTION_STORAGE_SPEC.md`
- `docs/21_SAMPLING_PROVENANCE_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/24_JOB_PROCESSING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/36_BACKUP_RETENTION_RECOVERY.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`

## G1. UI/UX target reconciliation

Update UI specs so the target product identity is IPSP.

CampaignSim remains visual reference only.

Freeze target navigation from F-002.

Keep five-step simulation UX exactly:

1. Define
2. Configure
3. Enrich & Validate
4. Run
5. Results & Compare

UI composition must be driven by:

```text
Semantic Manifest
+ Capability Manifest
+ Domain Experience Manifest
+ Scenario Intent
+ Organization Config
+ Permissions / Consent
```

Domain pages are capability-driven, not guaranteed static screens.

## G2. Storage/schema architecture-ready contract

Update `docs/27_SQLITE_SCHEMA_SPEC.md` so future migrations have clean conceptual homes for:

- metric/formula definitions;
- engine/license registry metadata;
- Domain activation metadata;
- Scenario Intent;
- assumptions;
- Evidence Profiles/snapshots;
- CompositeSimulationGraph metadata;
- CrossDomainSemanticGraph metadata;
- SimulationLearningStore;
- OutcomeReconciliation;
- model/library/license metadata;
- Local AI model/adapter/evaluation metadata.

Do NOT add actual tables in this phase.

Explicitly state migrations arrive only in their owning milestones.

## G3. REST API contract reconciliation

Update `docs/28_REST_API_CONTRACT.md` conceptually for future resource families, without claiming routes are implemented.

Avoid premature endpoint over-design.

Preserve `/api/v1` compatibility.

## G4. Job architecture

Update `docs/24_JOB_PROCESSING_SPEC.md` only as needed for provider-neutral future work.

Keep `JobBackend` abstraction and current LocalJobBackend single-process constraint.

Do not replace the generic durable job vocabulary with domain-specific job types.

`SYNTHETIC_FITTING` may remain generic.

## G5. Configuration

Update `docs/35_CONFIGURATION_SPEC.md` target contracts for:

- provider-neutral synthetic capability;
- Engine/License policies;
- evidence access;
- consent/policy composition;
- organization license mode;
- model-weight gates.

Do not edit production feature flags yet; that belongs to F2-I.

## G6. Security/privacy/outbound

Reconcile security/outbound specs for:

- license gate;
- evidence policy;
- runtime consent;
- project/dataset policies;
- learning eligibility;
- Local/Remote provider governance.

Preserve deny-by-default outbound behavior.

## G7. Observability/health/backup

Extend target contracts so future health/audit can represent:

- engines/providers;
- license status;
- evidence providers;
- learning runs;
- model/adapter state;
- Cross-Domain execution.

Do not make unimplemented services current readiness requirements.

## G8. Ingestion/sampling compatibility

Review v0.2 ingestion and provenance specs only for compatibility with F-002.

Do not implement v0.2.

Make sure future dataset-version provenance can support the F-002 provenance classes without forcing all of them into v0.2 persistence prematurely.

## G9. Progress / validation

Update progress.

Expected production changes: none.

Run docs/link/diff/conformance checks.

## G10. Final report

End exactly:

`F2-G: PASS — UI, API, storage, jobs, security, configuration and operations contracts reconciled to F-002; proceed only after independent review`

or

`F2-G: FAIL — platform-contract reconciliation incomplete; do not proceed`

Do not begin F2-H.

---

# PHASE F2-H PROMPT
# Flows / Testing / Acceptance / Benchmark / Governance / Agent-Instruction Reconciliation

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-H only**.

This is the final documentation/governance reconciliation before production v0.1.1 changes.

Read every current F-002-updated spec, every `flows/*.md`, and:

- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/39_BENCHMARK_CATALOG.md`
- `docs/40_ANTI_CONTAMINATION.md`
- `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`
- `docs/42_ACTIVE_WORKSTREAMS.md`
- `docs/43_WORKSTREAM_CONTRACT_TEMPLATE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.github/instructions/*.md`
- `prompts/PHASED_COPILOT_PROMPTS.md`
- `FILE_INDEX.md`

## H1. Create/update canonical flows

Reconcile existing flows and add new flows where necessary.

At minimum ensure there are authoritative Mermaid flows for:

1. F-002 canonical end-to-end lifecycle;
2. Domain Experience activation;
3. Metric & Formula resolution;
4. Engine + License resolution;
5. Scenario Intent + three simulation bases;
6. CompositeSimulationGraph execution;
7. Cross-Domain semantic reconciliation;
8. Finance three-statement/stress conceptual flow where appropriate;
9. Trust + Evidence Profile;
10. SimulationLearningStore + Outcome Reconciliation;
11. evidence access / consent routing;
12. model champion/challenger learning;
13. Local LLM memory/fine-tune governance.

Prefer adding numbered flows after the current sequence rather than renumbering historical files.

Update `flows/README.md` and `FILE_INDEX.md`.

## H2. Test strategy

Update `docs/29_TEST_STRATEGY.md` so future milestone tests cover:

- Domain neutrality;
- Metric Registry validation;
- Engine/license resolution;
- provider fallback/refusal;
- synthetic provenance;
- accounting/unit/currency/time constraints;
- Cross-Domain graph safety;
- simulation-basis provenance;
- evidence profile separation;
- learning eligibility;
- outcome reconciliation;
- Local AI authority boundaries;
- reproducibility/evidence snapshots.

Do not add all future tests now.

## H3. Acceptance criteria

Update `docs/30_ACCEPTANCE_CRITERIA.md` to match the revised v1.0 definition.

Separate:

- v1.0 mandatory acceptance criteria;
- capabilities intentionally deferred post-v1.0.

Do not treat Remote LLM, PUBLIC_WEB, enterprise connectors, distributed scale, advanced causal/optimization or specialized Quant Finance as mandatory blockers unless F-002 explicitly requires a foundation contract.

## H4. Benchmark strategy

Update benchmark/anti-contamination docs so the test set exercises multiple domain families and Composite/Cross-Domain semantics without becoming hardcoded production truth.

Preserve prior benchmark knowledge/history.

## H5. Parallel development workflow

Reconcile workstream templates for the revised milestone sequence.

Require each future milestone contract to state:

- exact base SHA;
- owner;
- owned/shared/forbidden paths;
- functional contract;
- data/schema contract;
- API/interface contract;
- acceptance contract;
- dependency/license contract;
- migration owner;
- dependency owner;
- stop conditions;
- branch gate;
- post-merge gate;
- milestone acceptance gate.

## H6. Agent/Copilot instructions full reconciliation

Now fully update:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- relevant scoped instruction files.

Remove/replace superseded instructions such as:

- CampaignSim as top-level shell identity;
- SDV as generic/core synthetic architecture;
- old v0.2–v0.9 roadmap;
- old simulation milestone bundling;
- any instruction that conflicts with Domain Experience/Engine Registry architecture.

Preserve security and coding hardening.

## H7. Phased implementation prompt map

Rewrite `prompts/PHASED_COPILOT_PROMPTS.md` to reflect the new roadmap.

Keep prompts high-level enough that each future milestone still receives a dedicated detailed prompt before coding.

Do not begin v0.2.

## H8. Current workstream state

Update `docs/42_ACTIVE_WORKSTREAMS.md` so it does not imply old v0.2 workstreams are active before F-002/v0.1.1 acceptance.

## H9. Documentation completeness audit

Search all Markdown for stale architecture/roadmap terms.

Classify every occurrence of:

- CampaignSim identity;
- SDV core/synthetic wording;
- old roadmap;
- old simulation basis;
- KPI-only architecture;
- missing F-002 authority references.

Historical acceptance reports and historical prompt artifacts may retain old wording when clearly historical.

Do not rewrite historical evidence simply to eliminate a search string.

## H10. Validation

Run:

```text
git diff --check
```

Validate all Markdown relative links and Mermaid blocks.

Run architecture-conformance tests.

Expected production/schema/dependency changes: none.

## H11. Final report

End exactly:

`F2-H: PASS — F-002 flows, tests, acceptance, governance and agent instructions reconciled; v0.1.1 production reconciliation may begin only after independent review`

or

`F2-H: FAIL — documentation/governance reconciliation incomplete; do not begin production reconciliation`

Do not begin F2-I.

---

# PHASE F2-I PROMPT
# IPSP v0.1.1 Production Reconciliation
## Minimal foundation-code changes required by F-002

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-I only**.

All F2-A through F2-H documentation/governance phases must be accepted first.

Purpose:

> Make the already-accepted v0.1 foundation compatible with F-002 where current production code or repository enforcement directly contradicts the new freeze, without implementing v0.2 or later analytical capabilities.

## I1. Read before editing

Read completely:

- F-002 master freeze;
- roadmap freeze;
- all newly created F-002 specs;
- updated AGENTS/Copilot instructions;
- current config/feature flags;
- frontend shell;
- architecture conformance tests;
- pyproject/lock;
- current license state;
- current `.github/` contents.

Before editing:

```text
git status --short
git rev-parse HEAD
```

## I2. Production change boundary

Authorized categories only:

1. neutral IPSP branding reconciliation;
2. provider-neutral synthetic capability flag/config naming;
3. anti-contamination/conformance enforcement;
4. version bump to `0.1.1` where application metadata requires it;
5. explicit project/dependency licensing governance artifacts;
6. CI/repository checks that enforce the existing quality gates, if they can be added without changing product behavior.

Not authorized:

- ingestion;
- dataset models/tables;
- Parquet runtime;
- Semantic Manifest runtime;
- Domain Experience execution engine;
- Metric Registry runtime;
- Engine Registry runtime;
- model training;
- simulation;
- Finance runtime;
- learning runtime;
- Local LLM runtime.

## I3. Neutral IPSP branding

Update the generic frontend/application shell so top-level identity is IPSP.

Remove CampaignSim from generic production branding such as:

- page title;
- meta description;
- application brand header;
- generic ARIA labels;
- noscript message;
- router-generated document title.

Do not remove historical/reference CampaignSim material from `reference/`.

Preserve the visual design language.

## I4. Provider-neutral synthetic feature flag

Current vendor-specific architecture must become capability-specific.

Replace production/config naming equivalent to:

```text
sdv_enabled
IPSP_FEATURES__SDV_ENABLED
```

with a generic form such as:

```text
synthetic_data_enabled
IPSP_FEATURES__SYNTHETIC_DATA_ENABLED
```

Use the exact final name frozen in the updated configuration spec.

If backward compatibility for an existing environment variable is intentionally required by the spec, implement a narrow deprecated alias with deterministic precedence and tests.

Do not install Synthcity or SDV.

Keep `JobType.SYNTHETIC_FITTING` unless the frozen F-002 job spec explicitly changes it.

## I5. Anti-contamination tests

Strengthen architecture/conformance tests so domain/prototype/vendor-specific terms are rejected from generic surfaces where inappropriate.

At minimum inspect:

- backend core;
- generic frontend shell;
- config;
- generic database/migrations.

Allow domain terminology in:

- registered domain-spec documentation/reference;
- benchmark fixtures/tests;
- historical prompt/acceptance evidence;
- `reference/`.

Tests must distinguish intentional domain knowledge from generic-core contamination rather than naïvely banning words repository-wide.

## I6. Version bump

If the authoritative roadmap/implementation contract now defines the reconciliation application version as `0.1.1`, update the canonical application/package version surfaces consistently.

Do not modify `/api/v1` just because application version becomes 0.1.1.

Contract/API major version and application package version are separate.

## I7. Project/dependency licensing artifacts

The project currently declares proprietary licensing direction.

Add an explicit top-level project license/proprietary notice if the frozen license governance spec requires it.

Add a human-readable third-party license inventory/policy file such as:

```text
THIRD_PARTY_LICENSES.md
```

or the exact name frozen by F2-D/F2-G.

Do not claim target libraries are installed.

The current inventory must reflect actual current dependencies only, plus clearly separated approved future candidates if the spec allows that section.

Do not redistribute license text inaccurately.

## I8. CI workflow

If no CI exists, add a minimal GitHub Actions workflow only if consistent with the frozen repository-governance spec.

It should run the established foundation gates, for example:

- supported Python setup;
- locked/project install strategy;
- compileall;
- pytest;
- Ruff check;
- Ruff format check;
- strict mypy;
- pip check;
- architecture-conformance tests;
- Alembic consistency where safe.

Do not introduce npm/Node simply for CI.

Do not configure remote branch protection through code. Report branch protection as an owner/GitHub-setting action if still required.

## I9. Tests

Update/add focused tests for:

- neutral branding;
- provider-neutral synthetic flag;
- deprecated alias behavior if any;
- anti-contamination scope;
- application version consistency;
- license/governance file sanity where useful.

Do not add tests for unimplemented F-002 engines.

## I10. Documentation status

Update `docs/31_IMPLEMENTATION_PROGRESS.md` so F2-I is recorded as implemented/tested but v0.1.1 is not yet finally accepted until F2-J.

README current-state wording may be updated only where current code genuinely changed.

Do not describe F-002 analytical capabilities as implemented.

## I11. Mandatory quality gates

Run:

```text
python -m compileall -q backend tests
pytest
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
```

Run Alembic verification against an isolated database:

```text
alembic heads
alembic current
alembic check
```

Expected schema remains exactly the accepted foundation schema unless a prior F-002 specification explicitly authorized a non-v0.2 metadata-only migration—which this prompt does not authorize by default.

Preferred expected result:

```text
No migration changes
Seven application ORM tables
```

## I12. Browser/shell QA

Recheck:

- login;
- Overview;
- Jobs;
- Profile;
- System Health;
- System/Dark/Light themes;
- required-password flow;
- permission-denial flow;
- desktop/mobile;
- no external runtime asset request;
- no console application error;
- neutral IPSP generic branding.

## I13. Expected diff boundary

Likely changes may include:

```text
frontend/**
backend/ipsp/config/feature_flags.py
.env.example and config documentation if current config contract requires
backend/application metadata version surfaces
pyproject.toml only for the 0.1.1 version or license metadata if frozen
tests/architecture/**
focused config/frontend/version tests
LICENSE or proprietary notice
THIRD_PARTY_LICENSES.md
.github/workflows/** if authorized by frozen governance
docs/31_IMPLEMENTATION_PROGRESS.md
README.md only for verified current-state wording
```

No ingestion/model/simulation/learning implementation.

## I14. Final report

Report:

### A. Starting SHA

### B. Files created

### C. Files modified

### D. Branding reconciliation

### E. Synthetic capability/config reconciliation

### F. Anti-contamination enforcement

### G. Version consistency

### H. Licensing artifacts

### I. CI/governance

### J. Tests
Exact pass/fail/skipped/warnings/duration.

### K. Quality gates

### L. Browser QA

### M. Database/migration state

### N. Dependencies installed/changed
Expected: no new analytical/AI dependencies.

### O. F-002 capabilities implemented
Expected: only foundation reconciliation; no analytical F-002 engine implementation.

### P. v0.2 state
Expected: NOT STARTED.

### Q. Deviations

### R. Gate result

End exactly:

`F2-I: PASS — v0.1.1 production reconciliation implemented and ready for independent F2-J acceptance audit; v0.2 remains blocked`

or

`F2-I: FAIL — v0.1.1 reconciliation incomplete; v0.2 remains blocked`

Do not begin F2-J automatically.

---

# PHASE F2-J PROMPT
# Independent F-002 + IPSP v0.1.1 Final Acceptance Audit

**Required starting SHA:** `<<PREVIOUS_ACCEPTED_SHA>>`

This task is **F2-J only**.

It is a final audit, not a feature phase.

Expected production implementation changes during F2-J:

```text
NONE
```

If a real defect is found, document it and FAIL. Do not patch production inside the final audit.

## J1. Audit scope

Audit the repository for two separate questions:

### A. F-002 documentation/governance acceptance

Is the latest architecture now coherent, authoritative, cross-referenced, non-contradictory, and usable by future Codex/Copilot work?

### B. v0.1.1 foundation compatibility

Does the accepted v0.1 foundation remain healthy after the minimal F-002 reconciliation changes?

Do NOT audit as though v0.2–v1.0 features were already required to exist.

## J2. Read everything authoritative

Read:

- `AGENTS.md`;
- `.github/copilot-instructions.md`;
- all scoped agent instructions;
- README;
- every numbered spec;
- every F-002 new spec;
- every flow;
- acceptance criteria;
- progress;
- decision log;
- open questions;
- benchmark/anti-contamination;
- parallel workflow;
- current source/tests/config/migrations/dependencies.

## J3. Create final acceptance report

Create:

```text
docs/F002_V0_1_1_ACCEPTANCE_REPORT.md
```

Do not overwrite the historical Phase 1 acceptance report.

The new report must contain:

- audited SHA;
- audit date;
- F-002 scope;
- v0.1.1 reconciliation scope;
- source-of-truth hierarchy;
- architecture coherence matrix;
- roadmap/versioning matrix;
- current-vs-future status matrix;
- production reconciliation matrix;
- anti-contamination matrix;
- license/provider governance matrix;
- test/quality evidence;
- schema/dependency evidence;
- browser QA;
- repository hygiene;
- deferred v0.2+ capabilities;
- blockers;
- final recommendation.

## J4. F-002 architecture matrix

Audit at least:

1. product identity;
2. canonical lifecycle;
3. Domain Experience architecture;
4. domain families;
5. Metric & Formula Registry;
6. CrossDomainSemanticGraph;
7. ScenarioIntentManifest;
8. exact simulation bases;
9. CompositeSimulationGraph;
10. EngineRegistry;
11. LicenseRegistry;
12. EngineResolver;
13. provider neutrality;
14. open-source-preferred policy;
15. model selection/baselines;
16. causal boundary;
17. optimization boundary;
18. Finance architecture;
19. Trust;
20. Evidence Profile;
21. provenance including SYNTHETIC_DATA;
22. SimulationLearningStore;
23. OutcomeReconciliation;
24. champion/challenger learning;
25. LLM modes;
26. evidence access modes;
27. UI/navigation;
28. backend layering;
29. two-plane storage;
30. revised roadmap/v1.0 boundary.

Use exactly:

- PASS
- BLOCKED
- DEFERRED_BY_ROADMAP
- NOT_APPLICABLE

A future capability being unimplemented is normally `DEFERRED_BY_ROADMAP`, not a blocker, if its F-002 contract is correctly frozen.

## J5. Contradiction sweep

Search all current non-historical documentation/instructions for contradictory stale wording.

Historical prompt/acceptance files may retain prior wording if clearly historical.

Block acceptance if active authority/instructions still direct future agents to:

- treat CampaignSim as primary product identity;
- treat SDV as generic synthetic architecture;
- use the old roadmap;
- use the old simulation basis;
- bypass Domain Experience/Metric/Engine registries;
- treat simulated data as empirical truth;
- give LLM numerical authority.

## J6. v0.1.1 production reconciliation audit

Verify:

- generic IPSP branding;
- provider-neutral synthetic capability flag;
- version 0.1.1 consistency where frozen;
- no v0.2 implementation;
- seven-table foundation schema unchanged;
- JobBackend/LocalJobBackend behavior unchanged except authorized nonfunctional reconciliation;
- security/RBAC/session/CSRF/outbound/observability unchanged or improved;
- architecture-conformance tests cover generic frontend/config/core;
- license artifacts are accurate;
- no target dependency silently installed.

## J7. Full test reproducibility

Run the full suite twice as two planned independent invocations:

```text
pytest
pytest
```

Both must pass with:

- 0 failed;
- 0 skipped unless a pre-existing explicitly accepted skip is documented by current strategy;
- no unexpected warnings.

Do not rerun until green.

Also run focused:

```text
pytest tests/architecture
```

and the high-value Phase 1 foundation/security/job suites identified by current acceptance documentation.

## J8. Quality gates

Run:

```text
python -m compileall -q backend tests
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
```

Verify Alembic:

```text
alembic heads
alembic current
alembic check
```

Confirm:

- one Alembic tree;
- synchronous SQLAlchemy foundation;
- seven application tables;
- no v0.2 dataset tables;
- no migration drift.

## J9. Browser QA

Use isolated state.

Recheck:

- Login;
- required-password flow;
- Overview;
- Jobs;
- Profile;
- System Health;
- permission denial;
- logout;
- System/Dark/Light;
- desktop and ~390px mobile;
- no horizontal overflow;
- no app-origin console error;
- no public CDN/remote runtime asset;
- neutral IPSP branding;
- cleanup of QA processes/files.

## J10. License/dependency audit

Verify actual installed/project dependencies against:

- `pyproject.toml`;
- lock file;
- third-party inventory;
- project license notice.

Do not audit future candidate libraries as though installed.

Any inaccurately claimed current license is a blocker until corrected in a later narrow hardening phase.

## J11. Roadmap gate

Confirm progress says:

```text
v0.1.0 — historical accepted foundation
v0.1.1 — F-002 reconciliation pending/under final acceptance during audit
v0.2.0 — NOT STARTED
```

Only after every F2-J gate passes may documentation be updated to:

```text
v0.1.1 — F-002 FOUNDATION RECONCILED / ACCEPTED
v0.2.0 — AUTHORIZED FOR CONTRACT-FREEZE PREPARATION, NOT IMPLEMENTATION
```

Do not begin v0.2 implementation.

## J12. README/progress update on PASS

Only after all technical/documentation gates pass, update current-state wording in:

- `README.md`;
- `docs/31_IMPLEMENTATION_PROGRESS.md`;

so v0.1.1 is accepted.

Do not describe any v0.2+ capability as implemented.

## J13. Repository residue

Confirm no:

- orphan processes;
- QA databases/WAL/SHM;
- runtime test logs;
- browser profiles;
- temp venvs;
- credentials/cookies;
- generated archives;
- untracked prompt/test debris.

## J14. Final report

Return:

### A. Starting state

### B. Files created
Expected final audit report only unless PASS status docs require update.

### C. Files modified

### D. F-002 architecture matrix
Give counts and blockers.

### E. Active-document contradiction sweep

### F. v0.1.1 reconciliation matrix

### G. Version/roadmap consistency

### H. Security/privacy regression

### I. Database/migration

### J. Dependencies/licenses

### K. Full-suite run 1
Exact result/duration.

### L. Full-suite run 2
Exact result/duration.

### M. Architecture/focused tests

### N. Quality gates

### O. Browser QA

### P. Repository/runtime hygiene

### Q. Production defects found
Expected on PASS: `None`.

### R. Production source changes during F2-J
Expected: `None`.

### S. v0.2 state
Expected: `NOT STARTED`.

### T. Deviations/unresolved issues
If none: `None`.

### U. Gate result

End exactly with one:

`F2-J: PASS — IPSP v0.1.1 F-002 foundation reconciliation accepted; v0.2 may proceed to contract-freeze preparation only`

or

`F2-J: FAIL — IPSP v0.1.1 F-002 reconciliation not accepted; v0.2 remains blocked`

Do not begin v0.2.

---

# 4. F-002 phase acceptance ledger

Use this table outside Codex or in `docs/31_IMPLEMENTATION_PROGRESS.md` as phases are accepted.

| Phase | Purpose | Required input | Gate status | Accepted SHA |
|---|---|---|---|---|
| F2-A | Architecture authority + roadmap freeze | `7fdfd1d...` | NOT STARTED | — |
| F2-B | Product/core architecture reconciliation | F2-A accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-C | Data/semantics/metrics/domain contracts | F2-B accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-D | Capability/engine/license/model contracts | F2-C accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-E | Simulation/composite/Finance/trust/evidence | F2-D accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-F | Learning/outcome/LLM/evidence access | F2-E accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-G | UI/API/storage/jobs/security/ops contracts | F2-F accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-H | Flows/tests/acceptance/governance/instructions | F2-G accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-I | v0.1.1 production reconciliation | F2-H accepted SHA | BLOCKED BY PRIOR PHASE | — |
| F2-J | Final independent acceptance audit | F2-I accepted SHA | BLOCKED BY PRIOR PHASE | — |

---

# 5. Final program boundary

Successful completion of this prompt pack means only:

```text
F-002 is authoritative and internally reconciled.
IPSP v0.1.1 foundation is compatible with F-002.
The accepted v0.1.0 history remains preserved.
No v0.2 analytical capability has been implemented.
```

Only after F2-J PASS should the project prepare the dedicated **v0.2 contract-freeze and implementation prompt pack**.

Do not let Codex automatically continue from F2-J into v0.2.
