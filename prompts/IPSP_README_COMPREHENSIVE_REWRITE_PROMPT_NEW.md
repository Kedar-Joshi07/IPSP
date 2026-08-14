TASK
====

Update the root `README.md` of the IPSP repository so that it accurately represents:

1. the currently accepted implementation state;
2. the latest owner-approved F-002 architecture freeze;
3. the newly frozen domain architecture;
4. the newly frozen simulation architecture;
5. the newly frozen Engine/License architecture;
6. the newly frozen continual-learning architecture;
7. the newly frozen Cross-Domain Composite architecture;
8. the newly frozen Finance architecture;
9. the revised pre-v1.0 development roadmap;
10. the intended IPSP v1.0 scope and explicitly deferred post-v1.0 capabilities.

This is a DOCUMENTATION-ONLY task.

DO NOT implement production functionality.

DO NOT start v0.2.

DO NOT create migrations.

DO NOT install dependencies.

DO NOT change application code.

DO NOT change tests unless explicitly instructed in a later task.

DO NOT change any file other than `README.md`.

The purpose of this task is to make README.md accurately describe the latest frozen product direction while preserving a very clear distinction between:

- functionality implemented today;
- architecture that is frozen but not yet implemented;
- planned milestone scope;
- post-v1.0 capabilities.

This prompt represents an explicit owner-authorized architecture reconciliation.

For README content, the F-002 decisions contained in this prompt supersede older architectural wording in repository documentation where the two conflict.

Do NOT silently edit the conflicting specification files during this task.

Instead, use the latest architecture defined here when updating README.

The rest of the specification reconciliation will happen in subsequent tasks.


======================================================================
PHASE 0 — READ AND UNDERSTAND THE REPOSITORY BEFORE EDITING
======================================================================

Before modifying README.md, inspect the repository comprehensively.

First read:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `FILE_INDEX.md`
- existing `README.md`

Then read ALL Markdown documentation listed in `FILE_INDEX.md`, including:

- all `docs/*.md`
- all `flows/*.md`
- all applicable `.github/instructions/*.md`
- `config/README.md`
- `reference/README.md`
- relevant files under `prompts/`

At minimum, pay especially close attention to:

Product and architecture
------------------------
- `docs/00_SCOPE_FREEZE.md`
- `docs/01_PROJECT_SPEC.md`
- `docs/02_PRODUCT_REQUIREMENTS.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`

UI
--
- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`

Data and semantics
------------------
- `docs/07_DATA_UNDERSTANDING_SPEC.md`
- `docs/08_SEMANTIC_MODEL_SPEC.md`
- `docs/09_RELATIONSHIPS_HIERARCHY_LINEAGE_SPEC.md`
- `docs/10_KPI_METRIC_DEPENDENCY_SPEC.md`

Capabilities, models and simulation
-----------------------------------
- `docs/11_CAPABILITY_DISCOVERY_SPEC.md`
- `docs/12_MODELING_ENGINE_SPEC.md`
- `docs/13_MODEL_REGISTRY_LIFECYCLE_SPEC.md`
- `docs/14_SIMULATION_ENGINE_SPEC.md`
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`

LLM / AI / privacy
------------------
- `docs/16_LLM_ARCHITECTURE.md`
- `docs/17_PRIVACY_REMOTE_LLM_POLICY.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`

Data lifecycle
--------------
- `docs/20_INGESTION_STORAGE_SPEC.md`
- `docs/21_SAMPLING_PROVENANCE_SPEC.md`

Platform/operations
-------------------
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/24_JOB_PROCESSING_SPEC.md`
- `docs/25_REPORTING_EXPORT_SPEC.md`
- `docs/26_SIMULATION_HISTORY_REPRODUCIBILITY.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`

Quality/release
---------------
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/33_OPEN_QUESTIONS.md`

Engineering/governance
----------------------
- `docs/34_CODING_STANDARDS.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/36_BACKUP_RETENTION_RECOVERY.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `docs/38_GLOSSARY.md`
- `docs/39_BENCHMARK_CATALOG.md`
- `docs/40_ANTI_CONTAMINATION.md`
- `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`
- `docs/42_ACTIVE_WORKSTREAMS.md`
- `docs/43_WORKSTREAM_CONTRACT_TEMPLATE.md`

Read every flow, especially:

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
- `flows/12_STORAGE_PLANES.md`
- `flows/17_PREDICTION_HORIZON_LEAKAGE.md`
- `flows/18_JOURNEY_STAGE_METRIC_GRAPH.md`
- `flows/19_WORKSPACE_HIERARCHY.md`
- `flows/20_END_TO_END_LIFECYCLE.md`
- `flows/21_PARALLEL_DEVELOPMENT.md`

Also inspect actual implemented code sufficiently to confirm that README's
"implemented today" statements remain truthful.

Do not infer implementation merely because something is described in a spec.


======================================================================
SOURCE-OF-TRUTH AND STATUS RULES
======================================================================

Preserve the historical Phase-1 acceptance record.

The accepted implementation remains:

    IPSP application v0.1.0
    Phase 1 foundation
    FORMALLY ACCEPTED
    Independent Phase 1L.1 final review: PASS

Do NOT rewrite history.

Do NOT claim that F-002 functionality has already been implemented.

Do NOT claim v0.1.1 is already complete.

The newly agreed roadmap changes the NEXT planned step:

    v0.1.0
        accepted foundation
            ↓
    v0.1.1
        F-002 Architecture Reconciliation
            ↓
    v0.2.0
        Ingestion / Storage / Provenance

Therefore:

- v0.1.0 remains the currently accepted production foundation.
- v0.1.1 becomes the next planned reconciliation milestone.
- v0.2.0 remains NOT STARTED and must not begin until reconciliation is complete.
- old statements that v0.2 is the immediate next implementation milestone are superseded.
- old acceptance evidence must remain accurately represented.

Do NOT say v1.0 is the current product version.

Clearly distinguish:

    Current implementation = v0.1.0

from:

    Target first General Availability release = v1.0.0


======================================================================
ARCHITECTURE FREEZE TERMINOLOGY
======================================================================

Explain the distinction between:

1. Architecture Freeze
   Example: F-002

2. Application Version
   Example: v0.1.0, v0.5.0, v1.0.0

3. Development Phase / work package
   Example: Phase 1, later milestone workstreams

4. Contract Version
   Example:
   - `/api/v1`
   - Semantic Manifest contract version
   - Domain Experience contract version

F-002 DOES NOT mean application v2.0.

Application versioning follows semantic versioning:

    MAJOR.MINOR.PATCH

Before GA:

    v0.x.0 = accepted capability milestone
    v0.x.y = compatibility/bug/reconciliation patch

After GA:

    v1.x = backward-compatible capability growth

Reserve v2.0 for an actual major compatibility break.


======================================================================
UPDATED IPSP PRODUCT IDENTITY
======================================================================

The top-level product identity is now:

    Intelligent Predictive Simulation Platform
    IPSP

DO NOT present CampaignSim as the primary application identity.

The CampaignSim prototype/reference remains important ONLY as:

- historical origin/reference;
- visual design language;
- inspiration for cards, badges, navigation patterns, stepper,
  dark/light visual treatment, responsive behavior and interaction style.

Do NOT describe the application shell as:

    CampaignSim — Powered by IPSP

The generic application shell should be described as IPSP.

A future Marketing Domain Experience may use suitable Marketing terminology,
but CampaignSim does not own the platform architecture.

IPSP is:

    a domain-adaptive,
    dataset-agnostic,
    evidence-aware,
    analysis,
    prediction,
    simulation,
    optimization,
    trust,
    and governed-learning platform.

Its purpose is to determine:

    what data means,
    what can responsibly be analyzed,
    predicted,
    simulated,
    optimized,
    explained,
    compared,
    learned from,
    or refused.


======================================================================
UPDATED PRODUCT NON-GOALS
======================================================================

The README must make clear that IPSP is NOT:

- a dashboard generator;
- a fixed Marketing simulator;
- a fixed Finance simulator;
- an AutoML wrapper;
- an LLM chatbot;
- a synthetic-data generator;
- a financial calculator;
- a tool that assumes every dataset belongs to a predefined schema;
- a system that fabricates unsupported relationships;
- a system where prediction is presented as causation;
- a system where an LLM has numerical authority;
- a system where simulated outcomes automatically become empirical truth.


======================================================================
NEW CANONICAL END-TO-END PRODUCT LIFECYCLE
======================================================================

Replace the old simplified lifecycle with the F-002 lifecycle.

Use a readable Mermaid diagram and/or compact text flow representing:

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

Do not imply every dataset proceeds through every branch.

Capability discovery may refuse unsupported capabilities.


======================================================================
DOMAIN ARCHITECTURE
======================================================================

README must introduce Domain Experience architecture.

Frozen domain families:

- Marketing
- Product
- Sales
- Customer Experience
- Finance
- Operations / Demand
- Generic / Custom
- Composite / Cross-Domain

A dataset may activate:

- one domain;
- several domains;
- Composite/Cross-Domain capability.

The IPSP core remains domain-neutral.

Do NOT describe the architecture as separate independent engines such as:

    Marketing Engine
    Product Engine
    Sales Engine
    Finance Engine

Instead explain:

    IPSP Core
        +
    Domain Experience Packs

Domain Experience Packs may supply:

- terminology;
- objective taxonomy;
- semantic concepts;
- metric requests;
- control templates;
- UI metadata/templates;
- recommended analysis sections;
- comparison views;
- explanation vocabulary;
- optional benchmark knowledge;
- semantic/capability prerequisites.

They MUST NOT own:

- generic numerical truth;
- mandatory physical columns;
- hardcoded model choice;
- guaranteed response;
- arbitrary domain-specific production branching.

Catalog precedence:

1. organization-configured
2. observed/confirmed dataset values
3. curated Domain Experience Pack
4. custom user assumption


======================================================================
SEMANTICS AND CROSS-DOMAIN INTELLIGENCE
======================================================================

Retain the Dataset Semantic Manifest concept.

Expand README architecture to also introduce:

    CrossDomainSemanticGraph

This graph will describe validated relationships across domain concepts.

It must capture:

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

Cross-domain inference remains:

    infer
        ↓
    validate
        ↓
    confirm if ambiguous
        ↓
    persist

IPSP must NEVER create arbitrary joins merely to make a composite scenario work.

Cross-domain composition must reconcile where relevant:

- entity grain;
- aggregation grain;
- time zones;
- calendar periods;
- fiscal periods;
- currencies;
- units.


======================================================================
METRIC & FORMULA REGISTRY
======================================================================

The README currently discusses KPI dependency logic.

Update this to the F-002 model:

    Metric & Formula Registry

The existing Metric Dependency Graph remains a useful architectural precursor
and dependency representation.

The new registry separates domain knowledge from numerical truth.

Conceptual flow:

    Domain Experience
        ↓ requests semantic metric ID
    Metric & Formula Registry
        ↓ validates prerequisites
    Generic Compute Engine
        ↓
    Result + lineage

Metric definitions conceptually include:

- metric_id;
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

Make explicit:

    Domain Pack != Formula Engine


======================================================================
CAPABILITY DISCOVERY
======================================================================

Preserve the evidence-first capability philosophy.

IPSP should determine whether it can responsibly perform:

- descriptive analysis;
- diagnostic analysis;
- forecasting;
- regression;
- classification;
- count prediction;
- similarity/look-alike;
- clustering/segmentation;
- deterministic what-if;
- sensitivity analysis;
- Monte Carlo simulation;
- risk/stress analysis;
- synthetic-assisted analysis;
- optimization where supported;
- causal analysis where supported;
- Cross-Domain Composite simulation where supported.

Unsupported capabilities must be:

- limited;
- disabled;
- blocked;
- or refused

with reasons.

Do not imply the presence of a target column alone enables a predictive model.


======================================================================
ENGINE AND LICENSE ARCHITECTURE
======================================================================

Introduce the F-002 provider-neutral architecture:

    EngineRegistry
        +
    LicenseRegistry
        +
    EngineResolver

Production application services must depend on IPSP interfaces rather than
vendor implementations.

Examples:

    SyntheticDataProvider
        → SynthcityProvider
        → optional SDVProvider

    OptimizerProvider
        → OSQPProvider
        → SCSProvider
        → optional CommercialSolverProvider

    LLMProvider
        → LlamaCppProvider
        → RemoteProvider
        → HybridProvider

Do NOT make vendor libraries the architecture.

Replace SDV-specific architecture wording.

Specifically:

- SDV is not the generic synthetic-data architecture.
- Synthetic capability is provider-neutral.
- Synthcity is the preferred permissive default candidate.
- SDV may remain an optional provider subject to current licensing policy.
- Do not describe SDV as automatically open-source.

License metadata conceptually includes:

- engine ID;
- library;
- version;
- provider;
- license identifier/class;
- commercial-use status;
- redistribution/service restrictions;
- model-weight license;
- approved use;
- installed status;
- capabilities;
- hardware;
- security status.

License classes:

- PERMISSIVE_OPEN_SOURCE
- PUBLIC_DOMAIN
- COPYLEFT_OPEN_SOURCE
- SOURCE_AVAILABLE
- COMMERCIAL
- CUSTOM_MODEL_LICENSE
- UNKNOWN/BLOCKED

Organization modes:

- OPEN_SOURCE_ONLY
- OPEN_SOURCE_PREFERRED
- COMMERCIAL_ALLOWED

Default:

    OPEN_SOURCE_PREFERRED

Engine selection priority:

1. capability validity
2. license policy
3. trust/validation
4. data suitability
5. performance
6. available resources
7. organization preference


======================================================================
UPDATED OPEN-SOURCE-FIRST TECHNOLOGY DIRECTION
======================================================================

README should distinguish:

A. dependencies actually active in v0.1.0;
B. frozen/approved architecture candidates;
C. optional later providers.

Do not imply target dependencies are installed today.

Architecture candidates include:

Application/data
----------------
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Polars
- Apache Arrow / PyArrow
- Pandas where required
- Plotly.js

ML
--
- scikit-learn
- LightGBM
- XGBoost
- CatBoost

Statistics/econometrics
-----------------------
- Statsmodels
- arch
- PyMC where Bayesian modelling is justified

Causal
------
- DoWhy
- EconML
- optional causal-learn

Explainability
--------------
- SHAP

Tuning
------
- Optuna

Synthetic
---------
- Synthcity as preferred permissive provider candidate
- SDV optional subject to licensing policy

Optimization
------------
- CVXPY abstraction
- OSQP
- SCS
- optional commercial solvers

Finance
-------
- QuantLib only for optional instrument/quant use cases
- arch where appropriate

Incremental learning
--------------------
- River only where true incremental/streaming learning is justified

Local AI
--------
- llama.cpp
- Transformers
- PEFT/LoRA
- optional MLflow

Model weights have independent licenses.

README must state that:

    dependency license
    and
    model-weight license

are separate governance decisions.


======================================================================
MODEL SELECTION PHILOSOPHY
======================================================================

Do not present one model as universally preferred.

README should explain:

    no universal best model

Selection depends on:

- target semantics;
- data size;
- data grain;
- horizon;
- class balance;
- temporal structure;
- explainability requirement;
- uncertainty requirement;
- compute availability;
- license policy;
- benchmark performance;
- Trust gates.

Mandatory principle:

    always include a meaningful baseline.

Candidate families should be described compactly rather than exhaustively.

Tabular:
- linear/logistic;
- regularized models;
- trees;
- Random Forest;
- ExtraTrees;
- gradient boosting;
- LightGBM;
- XGBoost;
- CatBoost.

Time series:
- naive;
- seasonal naive;
- rolling/statistical;
- ETS/state-space;
- ARIMA/SARIMAX;
- VAR/VECM where justified;
- lag-feature ML;
- Bayesian where justified;
- ARCH/GARCH where finance volatility semantics justify it.

Temporal validation must not use inappropriate random splits.


======================================================================
CAUSAL BOUNDARY
======================================================================

Make this distinction prominent:

    correlation != prediction != attribution != causation

Causal capability activates only when IPSP has sufficient semantics,
assumptions and evidence for:

- treatment;
- outcome;
- confounders;
- identification;
- validation/refutation.

Do not claim causal functionality is already implemented.


======================================================================
NEW SIMULATION ARCHITECTURE
======================================================================

Replace the old engine list as the main simulation classification.

The frozen simulation basis is EXACTLY:

- DATA_BASED
- MIXED
- INTENT_BASED

Do not create a fourth basis.

Explain:

DATA_BASED
----------
Primarily supported by observed/derived first-party data and validated
models/formulas.

MIXED
-----
Combines empirical evidence with explicit assumptions, analogs,
benchmarks, synthetic support and/or external evidence.

INTENT_BASED
------------
Starts from user objective/intent where empirical support may be incomplete;
assumptions and evidence limitations must remain explicit.

Intent-based simulation must never silently masquerade as observed truth.


======================================================================
SCENARIO INTENT MANIFEST
======================================================================

Introduce:

    ScenarioIntentManifest

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


======================================================================
COMPOSITE SIMULATION GRAPH
======================================================================

Introduce:

    CompositeSimulationGraph

as the universal simulation/execution abstraction.

Graph nodes may represent:

- deterministic formula;
- statistical model;
- ML model;
- time-series model;
- causal model;
- Monte Carlo;
- optimizer;
- synthetic generator/support;
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

If there is no defensible relationship:

    IPSP must constrain or refuse the path.

It must not fabricate an edge.


======================================================================
CROSS-DOMAIN COMPOSITE
======================================================================

Composite/Cross-Domain is a first-class capability.

Provide representative examples, clearly labeled as examples rather than
hardcoded product flows:

Marketing example:

    Marketing spend
        → response
        → leads
        → opportunities
        → orders
        → revenue
        → margin
        → cash

Product/Operations example:

    Product price or launch
        → demand
        → inventory
        → fulfilment
        → cost
        → margin
        → working capital

CX example:

    service / experience
        → satisfaction / sentiment
        → retention / churn
        → renewal
        → revenue / customer value

Do not imply those paths always exist.


======================================================================
FINANCE DOMAIN
======================================================================

Add Finance as a first-class Domain Experience family.

Finance should be described as a dynamically activated capability family,
not one giant mandatory schema.

Core Finance areas:

Corporate Performance / FP&A
----------------------------
- Actual / Budget / Forecast;
- variance;
- revenue;
- cost;
- margin;
- profitability;
- contribution;
- operating leverage;
- unit economics;
- scenario budgeting;
- rolling forecasting;
- target analysis.

Forecasting
-----------
- revenue;
- expense;
- gross margin;
- opex;
- cash;
- AR/AP;
- inventory/working capital;
- liquidity;
- business-unit/ratio forecasting.

Treasury & Liquidity
--------------------
- cash;
- runway;
- receivable/payable timing;
- working capital;
- funding;
- debt schedules;
- interest;
- FX;
- cash conversion cycle.

Three-statement relationships
-----------------------------
Where sufficient semantics exist:

    Income Statement
        ↔ Balance Sheet
        ↔ Cash Flow

Outputs must respect accounting constraints.

Risk & Stress
-------------
- deterministic stress;
- historical replay;
- Monte Carlo;
- volatility;
- sensitivity;
- revenue/cost/rate/FX/liquidity shocks;
- appropriate VaR-style analysis.

Credit / Collections
--------------------
Where supported:

- payment;
- lateness;
- delinquency;
- default;
- collection;
- delay.

Valuation / Capital Investment
------------------------------
- NPV;
- IRR;
- DCF;
- payback;
- project comparison;
- discount-rate sensitivity;
- terminal-value sensitivity.

Optional Quant Finance
----------------------
QuantLib/instrument pricing must be positioned as an optional future
Finance subpack.

It must NOT contaminate normal FP&A architecture.


======================================================================
OPERATIONS, PRODUCT, SALES, CX AND GENERIC DOMAIN COVERAGE
======================================================================

README should make the breadth of Domain Experience architecture clear.

Product
-------
Examples:
- product lifecycle;
- launch performance;
- adoption;
- demand;
- price;
- orders;
- returns;
- inventory;
- product performance.

Sales
-----
Examples:
- account;
- opportunity;
- pipeline;
- stage;
- territory;
- target;
- quota;
- forecast;
- won/lost;
- orders/revenue.

Customer Experience
-------------------
Examples:
- customer;
- service interaction;
- CSAT;
- NPS;
- CES;
- issue;
- resolution;
- complaint;
- churn;
- retention;
- structured sentiment-derived signals.

Do not imply IPSP v1.0 is a universal raw unstructured-text platform.

Operations / Demand
-------------------
Examples:
- demand;
- inventory;
- capacity;
- backlog;
- lead time;
- fulfilment;
- supplier;
- production;
- service level;
- stockout.

Generic / Custom
----------------
Must work even when no curated Domain Experience fits.

This is essential evidence that IPSP core remains domain-neutral.


======================================================================
SYNTHETIC DATA PROVENANCE
======================================================================

Add:

    SYNTHETIC_DATA

to the architecture/provenance discussion.

Synthetic datasets must carry metadata such as:

- generator;
- provider;
- version;
- seed;
- configuration;
- quality evaluation;
- privacy evaluation.

Synthetic data may support:

- privacy-safe development;
- simulation;
- augmentation;
- sparse-region exploration;
- stress testing;
- robustness analysis.

Synthetic records must NEVER automatically become empirical truth.


======================================================================
TRUST AND EVIDENCE PROFILE
======================================================================

Preserve Trust as independent from model/LLM confidence.

Expand Trust dimensions conceptually to include:

- data quality;
- semantic confidence;
- relationship validity;
- model validation;
- temporal leakage;
- extrapolation;
- constraints;
- accounting reconciliation;
- unit consistency;
- currency consistency;
- time/calendar consistency;
- simulation support;
- optimization feasibility;
- privacy;
- outbound policy;
- licensing;
- reproducibility.

Keep Green / Amber / Red conceptually.

Introduce a separate:

    Evidence Profile

Do NOT combine Evidence Profile and Trust into one score.

Evidence Profile can describe dependence on:

- first-party historical data;
- observed outcomes;
- assumptions;
- synthetic data;
- analogs;
- external evidence;
- extrapolation;
- evidence freshness;
- evidence coverage.


======================================================================
PROVENANCE CLASSES
======================================================================

Document the frozen conceptual provenance families:

- OBSERVED_DATA
- DERIVED_DATA
- ORGANIZATION_CONFIG
- DOMAIN_CATALOG
- USER_ASSUMPTION
- PRIOR_IPSP_RUN
- OBSERVED_OUTCOME
- CURATED_BENCHMARK
- EXTERNAL_EVIDENCE
- LOCAL_KNOWLEDGE_BASE
- LLM_PROPOSAL
- SYNTHETIC_DATA


======================================================================
RESULT HISTORY AND REPRODUCIBILITY
======================================================================

Preserve the important existing distinction:

RE-RUN
------
Same scenario intent using currently eligible models/evidence.

REPRODUCE
---------
Reconstruct original run using original frozen versions/configuration.

Extend `REPRODUCE` to include:

- original evidence snapshot;
- dataset version;
- semantic version;
- metric version;
- model version;
- engine/provider version;
- assumptions;
- seed;
- configuration;
- graph/version;
- applicable policy context.

A future rerun may use newer evidence.

A reproduction must represent the historical original.


======================================================================
CONTINUAL / GOVERNED LEARNING
======================================================================

Add this as a major architecture section.

Core principle:

    Every simulation becomes a learning experience;
    not every simulation becomes empirical truth.

Describe evidence authority tiers conceptually:

Highest:
- observed actual outcomes

High:
- derived observed data with lineage

Lower/non-empirical:
- data-based simulations
- mixed simulations
- intent-based simulations
- LLM proposals

Introduce:

    SimulationLearningStore

It retains scenario-level experience such as:

- scenario intent;
- simulation basis;
- domains;
- inputs;
- controls;
- constraints;
- assumptions;
- evidence;
- models;
- simulation graph;
- outputs;
- uncertainty;
- Trust;
- Evidence Profile;
- user actions/corrections;
- later observed outcomes.

Make clear this learning store is conceptually separate from empirical
analytical data so simulations cannot contaminate observed truth.


======================================================================
OUTCOME RECONCILIATION
======================================================================

Add the lifecycle:

Simulation at T0
    ↓
Real-world execution
    ↓
Observed actual at T1
    ↓
Prediction vs actual
    ↓
Error attribution
    ↓
Model / assumption / evidence evaluation
    ↓
Learning candidate

Do NOT describe IPSP as immediately retraining a model after every run.


======================================================================
CHAMPION / CHALLENGER LEARNING
======================================================================

Preserve and expand the existing model lifecycle.

Governed training path:

New Data / Reconciled Outcomes
    ↓
Learning Eligibility Gate
    ↓
Training Dataset Builder
    ↓
Leakage + provenance validation
    ↓
Challenger
    ↓
Validation
    ↓
Trust evaluation
    ↓
Champion comparison
    ↓
Promote or reject

Promotion may consider:

- predictive metrics;
- calibration;
- temporal holdout;
- stability;
- robustness;
- drift;
- explainability;
- constraint compliance;
- compute/resources.

River/incremental learning must NOT be described as default.

Default remains governed batch retraining unless streaming semantics
genuinely justify incremental learning.


======================================================================
LOCAL LLM LEARNING
======================================================================

Preserve exact LLM modes:

- ML_ONLY
- LOCAL_LLM
- REMOTE_LLM
- HYBRID_LLM

Numerical authority remains with:

    ML / statistics / deterministic engines

LLMs may assist with:

- semantics;
- intent interpretation;
- clarification;
- domain reasoning;
- capability explanation;
- analog ranking;
- evidence planning;
- result explanation;
- organization terminology.

Preferred learning approach:

1. continuous retrieval/memory;
2. optional periodic governed PEFT/LoRA adaptation.

Useful local-AI learning material:

- confirmed semantic mappings;
- user corrections;
- domain interpretations;
- clarification outcomes;
- intent parsing;
- validated control selections;
- capability reasoning;
- analog ranking;
- evidence query planning;
- approved explanations;
- organization vocabulary.

Never teach as empirical facts:

- intent-based simulation results;
- mixed assumptions;
- synthetic records;
- unverified external claims;
- LLM-proposed numbers;
- failed predictions without context/provenance.

Fine-tuning does not grant numerical authority to an LLM.


======================================================================
EVIDENCE ACCESS
======================================================================

Document frozen conceptual access modes:

- OFF
- INTERNAL_ONLY
- PUBLIC_WEB
- APPROVED_CONNECTORS

Effective permission conceptually equals:

    Admin policy
        ∩
    project/dataset policy
        ∩
    runtime user consent

Do not claim PUBLIC_WEB or APPROVED_CONNECTORS are currently implemented.


======================================================================
UPDATED BACKEND ARCHITECTURE
======================================================================

Replace/expand the current architecture Mermaid so it conceptually represents:

Adaptive Frontend
    ↓
FastAPI / API
    ↓
Authentication / RBAC / Policy / Consent
    ↓
Ingestion + Storage
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
Model & Local-AI improvement

Cross-cutting concerns:

- security;
- privacy;
- outbound controls;
- secrets;
- jobs;
- observability;
- provenance;
- licensing;
- reproducibility.

Storage remains two-plane:

SQLite
------
Control / governance / knowledge metadata.

Source + Parquet
----------------
Analytical data.

Do not suggest SQLite is the large analytical warehouse.


======================================================================
UPDATED UI ARCHITECTURE
======================================================================

Keep the CampaignSim visual design language where useful,
but brand the product as IPSP.

Frozen top-level navigation target:

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

Domain pages must be capability-driven.

They must NOT be guaranteed static pages.

Standard domain experience may expose:

- Overview
- Data Fit
- Analyze
- Diagnose / Drivers
- Simulate
- Compare
- History

only when supported.

Finance may dynamically expose:

- Overview
- Data Fit
- Performance
- Forecast
- Drivers
- Cash & Liquidity
- Risk & Stress
- Valuation
- Optimize
- Simulate
- Compare
- History

only when supported.

Composite workspace may expose:

- Scope
- Domain Graph
- Data Fit
- Analyze
- Drivers
- Simulate
- Cascade Results
- Optimize
- Compare
- History


======================================================================
FIVE-STEP SIMULATION EXPERIENCE
======================================================================

Preserve EXACTLY:

1. Define
2. Configure
3. Enrich & Validate
4. Run
5. Results & Compare

Do not invent a sixth canonical step.


======================================================================
UPDATED DEVELOPMENT AND VERSION ROADMAP
======================================================================

Replace the old roadmap entirely.

Use the following currently frozen roadmap:

v0.1.0
------
Foundation / Security / Repository Shell
STATUS:
FORMALLY ACCEPTED

v0.1.1
------
F-002 Architecture Reconciliation

Purpose:
Align accepted Phase-1 foundation documentation/contracts with F-002.

Includes conceptually:
- F-002 repo authority;
- neutral IPSP branding;
- provider-neutral synthetic naming;
- Domain Experience contracts;
- Metric Registry contracts;
- Engine/License contracts;
- Composite/Cross-Domain contracts;
- learning contracts;
- anti-contamination updates;
- documentation/flows;
- license governance;
- regression validation.

Do NOT describe this as already implemented.

v0.2.0
------
Data Ingestion, Storage & Provenance

v0.3.0
------
Deterministic Data Understanding & Relationships

v0.4.0
------
Semantic Intelligence & Dataset Semantic Manifest

v0.5.0
------
Metric / Formula Registry + Domain Experience Foundation

v0.6.0
------
Capability Discovery + Engine/License Registry

v0.7.0
------
Core Modelling + Model Lifecycle

v0.8.0
------
Simulation Core
including:
- DATA_BASED
- MIXED
- INTENT_BASED
- ScenarioIntentManifest
- CompositeSimulationGraph foundation

v0.9.0
------
Trust + Evidence + History + Comparison

v0.10.0
-------
Cross-Domain Composite Intelligence

v0.11.0
-------
Domain Intelligence Completion

v0.12.0
-------
Learning + Outcome Reconciliation Foundation

v0.13.0
-------
Local AI

v0.14.0
-------
Full Dynamic Product UI

v0.15.0
-------
v1.0 Release Candidate / Hardening

v1.0.0
------
First General Availability release

Do NOT compress v0.10 into v1.0 because of decimal-number assumptions.

Semantic versions are not decimal fractions.

v0.10.0 is perfectly valid and comes after v0.9.0.


======================================================================
IPSP v1.0 DEFINITION
======================================================================

README must explain that v1.0 means:

    the first complete, production-usable expression
    of the IPSP architecture

NOT:

    every capability that IPSP may ever support.

Core expected v1.0 product capability includes:

- secure local-first platform;
- projects/workspaces;
- structured ingestion;
- dataset versioning/provenance;
- deterministic data understanding;
- Dataset Semantic Manifest;
- relationship/grain validation;
- Metric & Formula Registry;
- Domain Experience framework;
- baseline experiences for:
    - Marketing
    - Product
    - Sales
    - Customer Experience
    - Finance
    - Operations / Demand
    - Generic / Custom
- capability discovery;
- responsible refusal;
- core statistical/ML modelling;
- forecasting;
- explainability;
- Engine Registry;
- License Registry;
- open-source-preferred resolution;
- DATA_BASED simulation;
- MIXED simulation;
- INTENT_BASED simulation;
- CompositeSimulationGraph;
- basic defensible Cross-Domain simulation;
- Monte Carlo where valid;
- Trust;
- Evidence Profiles;
- Scenario Library;
- Compare;
- Re-run;
- Reproduce;
- SimulationLearningStore;
- Outcome Reconciliation foundation;
- governed champion/challenger learning;
- local LLM assistance as optional;
- PDF/Excel export;
- full capability-driven UI.


======================================================================
CAPABILITIES EXPLICITLY NOT REQUIRED TO BLOCK v1.0
======================================================================

README should include a concise "post-v1.0 / advanced capability"
section.

Do not require the following to declare v1.0 complete:

Advanced causal production capability
-------------------------------------
DoWhy/EconML production workflows may mature in v1.x.

Advanced optimization
---------------------
Full CVXPY/solver-backed decision optimization may mature in v1.x.

Automatic Local LLM fine-tuning
--------------------------------
v1.0 should gather governed learning events.
Full automated PEFT/LoRA lifecycle may mature later.

Remote / Hybrid LLM
-------------------
Architecture remains supported.

Remote LLM is NOT mandatory for v1.0.

Public web evidence
-------------------
Architecture-supported but not mandatory for v1.0.

Enterprise connectors
---------------------
Examples such as Salesforce, HubSpot, SAP, Oracle, BigQuery, Snowflake, etc.
must not block v1.0.

Enterprise distributed infrastructure
-------------------------------------
Do not make these mandatory for v1.0:

- PostgreSQL;
- Redis;
- Celery;
- Kubernetes;
- object storage;
- multi-node workers.

Advanced Quant Finance
----------------------
QuantLib-based specialized instrument pricing does not block normal
Finance v1.0.


======================================================================
POST-v1.0 ROADMAP
======================================================================

Add a clearly labelled tentative strategic roadmap.

Do NOT present these as immutable implementation commitments.

Suggested direction:

v1.1
----
Advanced Learning & Decision Intelligence

Examples:
- stronger reconciliation;
- drift;
- governed retraining;
- local semantic memory;
- optional LoRA/PEFT evaluation.

v1.2
----
Causal & Optimization Intelligence

Examples:
- DoWhy;
- EconML;
- CVXPY;
- OSQP/SCS;
- budget/resource/capacity optimization.

v1.3
----
External Intelligence

Examples:
- PUBLIC_WEB evidence;
- approved external evidence providers;
- Remote LLM;
- Hybrid LLM;
- stronger evidence research flows.

v1.4
----
Enterprise Integrations

Examples:
- warehouse/business-system connectors;
- enterprise identity;
- stronger organizational policy.

v1.5
----
Enterprise Scale

Examples:
- optional PostgreSQL control plane;
- distributed workers;
- object/object-like storage;
- horizontal scaling;
- advanced operational deployment.

State explicitly:

    v2.0 is NOT pre-assigned to a feature set.

A major version should be reserved for a meaningful breaking compatibility
change.


======================================================================
DOMAIN PACK VERSIONING
======================================================================

Mention that the architecture should permit Domain Experience Packs to
eventually carry versions independently from the IPSP application.

Conceptual future example:

    IPSP Core                 1.x
    Marketing Experience      x.y
    Product Experience        x.y
    Sales Experience          x.y
    CX Experience             x.y
    Finance Experience        x.y
    Operations Experience     x.y

Do NOT claim this independent packaging/versioning is already implemented.


======================================================================
DEVELOPMENT FLOW
======================================================================

Replace/expand the roadmap process to show:

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

Preserve the repository's existing disciplined integration ownership,
branch-gate and acceptance-gate philosophy.

Before implementation of a milestone, the future process should freeze:

1. functional contract;
2. data/schema contract;
3. API/interface contract;
4. acceptance contract;
5. dependency/license contract.


======================================================================
CURRENT IMPLEMENTATION SECTION
======================================================================

Keep a strong "Implemented today vs Target" section.

Do not remove the useful current v0.1.0 implementation details.

Preserve accurate descriptions of current foundation capabilities such as:

- FastAPI application factory;
- Python runtime;
- typed configuration;
- SQLAlchemy;
- SQLite;
- Alembic;
- users/roles/permissions;
- Argon2;
- opaque server-side sessions;
- CSRF;
- audit events;
- structured logging;
- error handling;
- SecretProvider;
- OutboundPolicy;
- JobBackend abstraction;
- LocalJobBackend;
- health endpoints;
- static/offline frontend;
- theme support;
- existing API surface.

But verify every such claim against current code before retaining it.

Do not imply future dataset/model/simulation functionality exists today.


======================================================================
PHASE-1 ACCEPTANCE EVIDENCE
======================================================================

Preserve the accepted Phase-1 evidence accurately.

Do NOT fabricate new test runs.

If the existing README says the accepted Phase-1 audit recorded:

- two clean 216-test full-suite runs;
- architecture/security checks;
- migration validation;
- browser QA;

you may retain that as HISTORICAL ACCEPTANCE EVIDENCE if still accurately
documented by the acceptance report.

Do NOT write:

    "all tests currently pass"

unless you actually run them during this task.

This README-only task does not require running the full suite unless necessary
to verify an edited current-state statement.


======================================================================
BACKGROUND JOBS
======================================================================

Preserve the provider abstraction.

Current:

    LocalJobBackend

Future:

    alternative/distributed JobBackend provider

Do not introduce Redis/Celery as current dependencies.

Do not make domain-specific job architecture.

The existing generic durable job vocabulary may remain where accurate.


======================================================================
SECURITY / PRIVACY / GOVERNANCE
======================================================================

Preserve the strong current security section.

Also explain conceptually that future F-002 governance adds:

- engine license gating;
- model-weight licensing;
- evidence policy;
- runtime consent;
- dataset/project policy;
- provenance;
- learning eligibility.

Do not weaken deny-by-default outbound behavior.


======================================================================
ANTI-CONTAMINATION
======================================================================

Strengthen the README's architecture principle.

Generic production core must not contain benchmark/domain/prototype
special cases.

Domain knowledge belongs in:

- Domain Experience Packs;
- Metric/Formula Registry definitions;
- explicit organization configuration;
- benchmark fixtures/tests/reference docs.

Generic core must not accumulate branches such as:

    if domain == "marketing"
    if domain == "finance"
    if domain == "product"

unless a generic registry/provider mechanism genuinely requires dispatch by
registered capability rather than hardcoded business logic.

CampaignSim terms should not appear as generic application identity.


======================================================================
REPOSITORY STRUCTURE
======================================================================

Update the conceptual target repository structure to remain provider-neutral.

Avoid:

    artifacts/sdv

Prefer conceptual structures such as:

    artifacts/models
    artifacts/manifests
    artifacts/reports
    artifacts/simulations
    artifacts/synthetic
    artifacts/evidence

Future engine/provider code may conceptually group:

    engines/
        synthetic/
        optimization/
        ml/
        statistics/
        finance/

Do NOT create these directories during this README-only task unless they
already exist.

README should distinguish actual directories from planned target layout.


======================================================================
README STRUCTURE
======================================================================

Keep the README comprehensive but navigable.

Use roughly this structure, adjusting only where necessary:

1. Title
2. Product identity
3. Current implementation status
4. Architecture/versioning status
5. Problem IPSP solves
6. Product definition
7. Non-goals
8. Current implementation vs target v1.0
9. End-to-end IPSP lifecycle
10. Architecture overview
11. Storage architecture
12. Data onboarding/versioning
13. Data Understanding
14. Semantic Model
15. Relationships / lineage
16. Metric & Formula Registry
17. Domain Experience architecture
18. Cross-Domain Semantic Graph
19. Capability Discovery
20. Engine & License architecture
21. Modelling/model lifecycle
22. Simulation architecture
23. Scenario Intent / Composite Simulation Graph
24. Cross-Domain Composite simulation
25. Finance domain
26. Other Domain Experiences
27. Trust & Evidence Profiles
28. Provenance
29. Results/history/reproducibility
30. Governed learning / SimulationLearningStore
31. Outcome reconciliation
32. ML vs LLM authority
33. Local AI
34. Security/RBAC/privacy/outbound
35. Background jobs
36. Observability/errors/health
37. UI/UX
38. Anti-contamination
39. Technical stack
40. Repository structure
41. Current API surface
42. Local development
43. Quality/testing
44. Versioning philosophy
45. Revised development roadmap
46. v1.0 scope
47. Post-v1.0 direction
48. Parallel development workflow
49. Documentation map
50. Current release/status summary

You may consolidate closely related sections to keep the README readable.

Do not blindly create 50 headings if some are better grouped.


======================================================================
README STYLE REQUIREMENTS
======================================================================

The README must be:

- technically precise;
- professional;
- readable by engineers;
- understandable by technical/product stakeholders;
- sufficiently comprehensive;
- less repetitive than the current document where possible;
- explicit about implemented vs planned functionality;
- free of marketing exaggeration;
- free of architecture ambiguity.

Use:

- concise paragraphs;
- tables where comparison helps;
- Mermaid diagrams;
- small code/text diagrams;
- bullets for capability lists;
- links to authoritative deeper specifications.

Do not turn README into a 100-page architecture specification.

README is the ENTRY POINT.

Detailed contracts belong in docs.


======================================================================
LINKING RULE
======================================================================

Prefer linking every major architecture area to its corresponding
repository specification.

When a new F-002 specification file does not yet exist:

- do not invent a broken link;
- describe the concept in README;
- retain links to relevant predecessor specs where useful;
- do not falsely imply old specs already contain the F-002 revision.

Subsequent tasks will reconcile those specs.


======================================================================
CRITICAL WORDING RULE
======================================================================

Use explicit status labels throughout:

- IMPLEMENTED
- ACCEPTED
- FROZEN ARCHITECTURE / PLANNED
- NOT IMPLEMENTED
- DEFERRED
- TENTATIVE POST-v1.0

Never use language that makes planned functionality appear operational.


======================================================================
DO NOT DO THESE THINGS
======================================================================

Do NOT:

- implement F-002;
- edit specs;
- edit flows;
- edit AGENTS.md;
- edit Copilot instructions;
- edit source code;
- edit migrations;
- install libraries;
- create database tables;
- begin v0.2;
- say v0.1.1 is complete;
- say v1.0 is released;
- rewrite historical Phase-1 acceptance;
- make CampaignSim the product name;
- hardcode Finance or Marketing into the generic core;
- call SDV the synthetic architecture;
- describe simulations as automatically causal;
- make LLMs numerical authorities;
- treat synthetic outputs as actual observations;
- train models from simulation outputs without evidence-tier governance;
- imply remote LLM/web access is enabled today;
- imply enterprise distributed execution exists today;
- invent future API endpoints as implemented routes;
- invent license conclusions not present in the frozen policy.


======================================================================
FINAL SELF-AUDIT
======================================================================

After editing README.md, perform a documentation self-audit.

Check for stale strings/concepts including:

- "CampaignSim — Powered by IPSP" as top-level product branding
- old direct `SDV` architecture wording
- `SDV` presented as generic synthetic engine
- old v0.2–v0.9 roadmap
- "v0.7 dynamic frontend" as old roadmap authority
- "v0.8 Local LLM / v0.9 Remote LLM" as old milestone schedule
- old v0.6 simulation/trust/history bundle
- KPI Dependency presented as the full final metric architecture
- absence of Domain Experience architecture
- absence of Finance
- absence of Composite/Cross-Domain
- absence of Engine Registry
- absence of License Registry
- absence of Engine Resolver
- absence of Metric & Formula Registry
- absence of ScenarioIntentManifest
- absence of CompositeSimulationGraph
- absence of CrossDomainSemanticGraph
- absence of Evidence Profile
- absence of SimulationLearningStore
- absence of Outcome Reconciliation
- absence of governed learning
- planned functionality described as implemented

Also search for contradictions between:

- current implementation;
- F-002 target architecture;
- revised roadmap;
- v1.0 scope;
- post-v1.0 scope.


======================================================================
LINK VALIDATION
======================================================================

Check that all relative Markdown links in README resolve to real repository
paths.

Do not introduce broken links.


======================================================================
DIFF REVIEW
======================================================================

Before finishing:

1. inspect `git diff -- README.md`;
2. confirm only README.md changed;
3. check Markdown structure;
4. check Mermaid blocks for obvious syntax errors;
5. check tables render logically;
6. check terminology consistency;
7. confirm historical acceptance facts were preserved;
8. confirm no future capability was presented as implemented.


======================================================================
FINAL RESPONSE FORMAT
======================================================================

After completing the README modification, report:

1. `README.md updated`
2. Summary of major architecture sections changed
3. Old concepts removed/reframed
4. New F-002 concepts added
5. Current-vs-target status checks performed
6. Roadmap/versioning update performed
7. Links checked
8. Files changed

The files-changed section MUST say:

    README.md

and nothing else.

If any other file was modified accidentally, restore it before completing.

Do not start another task.

STOP after README.md is updated and audited.