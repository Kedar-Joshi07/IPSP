# F-002 Architecture Freeze

## Status and authority

**Architecture freeze:** F-002  
**Approval state:** FROZEN  
**Application implementation state:** PLANNED unless a later accepted milestone explicitly records implementation  
**Current accepted application:** IPSP v0.1.0 foundation  
**Accepted foundation SHA:** cd0dca48ded8d68f18e861f2427dfeb746d52ea7

F-002 is the authoritative architecture extension and reconciliation baseline for product and development decisions approved after acceptance of the v0.1.0 foundation. It extends, and where necessary supersedes, conflicting prior target-architecture wording. The companion [Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md) is authoritative for application sequencing and release boundaries.

Historical implementation and acceptance facts are not retroactively rewritten. The Phase 1/v0.1.0 foundation remains formally accepted, and the independent Phase 1L.1 final review remains PASS. F-002 does not claim that any newly frozen analytical, domain, engine, simulation, evidence, or learning capability is currently implemented.

If an older active specification conflicts with this document or the roadmap freeze, this document governs architecture and the roadmap freeze governs sequencing. Historical reports and prompts may retain the wording that accurately records their original context.

## Interpretation rules

- **F-002** is an architecture-freeze identifier, not application v2.0.
- **v0.1.0, v0.1.1, v0.2.0, and v1.0.0** are application versions.
- **F2-A through F2-J** are development work packages.
- **API, manifest, registry, and experience versions** are contract versions.
- A frozen capability is not an implemented capability.
- A planned provider is not an installed dependency.
- Provider and license boundaries are mandatory architecture gates.
- No v0.2 functionality is authorized by this architecture freeze.
- Generic core behavior remains dataset- and domain-agnostic.
- Unsupported capability paths are limited, disabled, blocked, or refused with reasons.

## Decision index

| Decision ID | Frozen decision |
|---|---|
| F002-D001 | IPSP is the neutral, domain-adaptive product identity; CampaignSim is historical visual reference only |
| F002-D002 | The canonical lifecycle runs from data understanding through governed learning and permits responsible refusal |
| F002-D003 | IPSP Core composes with registered Domain Experience Packs rather than separate hardcoded domain engines |
| F002-D004 | Organization configuration, observed/confirmed values, curated packs, and user assumptions have explicit precedence |
| F002-D005 | Numerical metric truth belongs to a versioned Metric & Formula Registry |
| F002-D006 | Cross-domain semantics use a validated CrossDomainSemanticGraph; arbitrary joins are prohibited |
| F002-D007 | Capability Discovery is evidence-first and separate from provider selection |
| F002-D008 | EngineRegistry, LicenseRegistry, and EngineResolver make provider and license governance executable |
| F002-D009 | OPEN_SOURCE_PREFERRED is the default organization mode; dependency and model-weight licenses are separate gates |
| F002-D010 | Model selection is baseline-first with no universal winner and strict prediction/causality separation |
| F002-D011 | The exact simulation bases are DATA_BASED, MIXED, and INTENT_BASED |
| F002-D012 | ScenarioIntentManifest and CompositeSimulationGraph are the universal scenario and execution contracts |
| F002-D013 | Composite/Cross-Domain and Finance are first-class, dynamically activated capabilities |
| F002-D014 | Trust and Evidence Profile are separate authorities |
| F002-D015 | Provenance includes SYNTHETIC_DATA; synthetic records never silently become observed truth |
| F002-D016 | SimulationLearningStore and OutcomeReconciliation support governed learning without circular contamination |
| F002-D017 | LLM modes and evidence-access modes remain governed; LLMs never gain numerical authority |
| F002-D018 | IPSP is the target UI identity and all domain pages are capability-driven |
| F002-D019 | The backend remains layered, provider-neutral, and split between SQLite control and source/Parquet analytical planes |
| F002-D020 | v1.0 is bounded to the first complete production-usable expression, not every future capability |

## Canonical product identity and non-goals

IPSP is a domain-adaptive, dataset-agnostic, evidence-aware platform for:

- understanding;
- analysis and diagnosis;
- prediction and forecasting;
- simulation;
- optimization where valid;
- Trust and evidence assessment;
- comparison and reproducibility;
- governed learning.

The generic product identity is **Intelligent Predictive Simulation Platform (IPSP)**. CampaignSim is a historical prototype and visual-design reference. It may inform cards, badges, navigation, steppers, themes, responsiveness, and interaction style, but it is not the platform identity or architecture authority.

IPSP is not:

- a dashboard generator;
- a fixed Marketing or Finance simulator;
- an AutoML wrapper;
- an LLM chatbot;
- a synthetic-data generator;
- a financial calculator;
- a fixed-schema product;
- a system that fabricates unsupported relationships;
- a system where prediction is presented as causation;
- a system where an LLM has numerical authority;
- a system where simulated output automatically becomes empirical truth.

## Canonical lifecycle

```text
DATA
  → UNDERSTANDING
  → SEMANTIC CONTRACT
  → DOMAIN / CROSS-DOMAIN ACTIVATION
  → CAPABILITY DISCOVERY
  → ANALYSIS / DIAGNOSIS
  → MODEL + ENGINE SELECTION
  → SIMULATION / OPTIMIZATION
  → TRUST + EVIDENCE
  → RESULTS / COMPARISON
  → SCENARIO & EXPERIENCE MEMORY
  → GOVERNED LEARNING
  → BETTER FUTURE MODELS / LOCAL AI
```

Not every dataset traverses every branch. Capability Discovery may limit, disable, block, or refuse an unsupported path and must preserve the reason.

## Domain Experience architecture

### Frozen domain families

- Marketing
- Product
- Sales
- Customer Experience
- Finance
- Operations / Demand
- Generic / Custom
- Composite / Cross-Domain

A dataset may activate one domain, several domains, or Composite/Cross-Domain capability.

### Core and packs

IPSP Core remains domain-neutral. Registered Domain Experience Packs extend the core; they do not fork it into independent Marketing, Product, Sales, or Finance engines.

A pack may provide:

- terminology and explanation vocabulary;
- objective taxonomy;
- semantic concept catalogs;
- semantic and capability prerequisites;
- metric requests;
- control and constraint templates;
- UI metadata/templates;
- recommended analysis sections and comparison views;
- optional benchmark knowledge.

A pack must not own:

- generic numerical truth;
- mandatory physical source columns;
- a hardcoded model winner;
- a guaranteed response;
- arbitrary business-domain branches in generic core;
- permission to bypass evidence, Trust, or licensing.

Catalog precedence is:

1. organization-configured;
2. observed or confirmed dataset values;
3. curated Domain Experience Pack;
4. explicit custom user assumption.

Future Domain Experience contracts may be versioned independently from the IPSP application. This compatibility direction does not claim that independent packaging exists in v0.1.0 or v0.1.1.

## Semantic and cross-domain intelligence

The Dataset Semantic Manifest remains the versioned semantic authority for a dataset version. It must be capable of supplying grain, entities, fields, roles, time, units, currencies, relationships, lineage, constraints, metrics, provenance, capability prerequisites, ambiguity, and confirmation state.

The **CrossDomainSemanticGraph** represents validated relationships between concepts. Each relationship records:

- source and target concepts;
- entity relationship;
- time relationship;
- grain relationship;
- unit relationship;
- currency relationship;
- transformation;
- evidence;
- support status.

Cross-domain inference follows:

```text
infer → validate → confirm if ambiguous → persist
```

Composition reconciles entity grain, aggregation grain, time zones, calendar and fiscal periods, currencies, and units where relevant. IPSP never creates an arbitrary join merely to satisfy composite intent.

## Metric & Formula Registry

Domain Experiences request semantic metric IDs. Numerical truth belongs in a versioned **Metric & Formula Registry** evaluated by generic compute services.

A metric definition conceptually includes:

- metric ID and version;
- semantic inputs;
- formula;
- aggregation semantics;
- time semantics;
- unit and currency semantics;
- null and safe-division behavior;
- required grain;
- validation tests;
- source and provenance.

The existing Metric Dependency Graph remains a useful dependency and evaluation representation inside the broader registry. Domain and organization catalogs may request or override definitions only through explicit versioned policy and precedence.

**Domain Pack does not equal Formula Engine.**

## Capability Discovery

Capability Discovery asks what can responsibly be calculated, analyzed, diagnosed, predicted, forecast, simulated, optimized, explained, compared, or refused. It evaluates at least:

- descriptive and diagnostic analysis;
- regression, classification, and count prediction;
- forecasting;
- similarity/look-alike;
- clustering and segmentation;
- deterministic what-if;
- sensitivity analysis;
- Monte Carlo;
- risk and stress analysis;
- synthetic-assisted analysis;
- optimization where supported;
- causal analysis where supported;
- Composite/Cross-Domain simulation where supported.

The architecture separates three questions:

```text
What is semantically and data-valid?
  → What engine families can perform it?
  → Which installed and allowed provider is eligible?
```

Installed software alone never establishes capability validity. A target-like column alone never enables prediction.

## Engine and license architecture

F-002 introduces:

- **EngineRegistry** for provider capabilities, versions, availability, resource needs, and security metadata;
- **LicenseRegistry** for dependency, provider, solver, commercial-use, redistribution/service, and model-weight restrictions;
- **EngineResolver** for deterministic eligible-provider selection.

Application services depend on IPSP interfaces rather than vendor implementations. Representative adapters include:

- SyntheticDataProvider → preferred Synthcity candidate or optional SDV provider;
- OptimizerProvider → OSQP, SCS, or optional commercial solver;
- LLMProvider → llama.cpp/local, remote, or hybrid provider.

These names are examples and approved candidates, not installed-runtime claims. SDV is not the generic synthetic architecture and is optional subject to current license policy.

### License metadata

Registry metadata conceptually includes:

- engine ID, library, version, and provider;
- license identifier and class;
- commercial-use status;
- redistribution and service restrictions;
- model-weight license;
- approved use;
- installed status;
- capabilities;
- hardware requirements;
- security status.

Frozen license classes:

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

The default is **OPEN_SOURCE_PREFERRED**. Resolver priority is:

1. capability validity;
2. license policy;
3. Trust and validation;
4. data suitability;
5. performance;
6. available resources;
7. organization preference.

A dependency license and a model-weight license are independent governance decisions.

## Open-source-first candidate direction

Candidates remain subject to milestone dependency and license review. Their appearance here does not mean they are installed.

| Area | Architecture candidates |
|---|---|
| Application/data | FastAPI, Uvicorn, SQLAlchemy, SQLite, Polars, Arrow/PyArrow, Pandas where needed, Plotly.js |
| ML | scikit-learn, LightGBM, XGBoost, CatBoost |
| Statistics/econometrics | Statsmodels, arch, PyMC where justified |
| Causal | DoWhy, EconML, optional causal-learn |
| Explainability/tuning | SHAP, Optuna |
| Synthetic | Synthcity preferred permissive candidate; SDV optional subject to license policy |
| Optimization | CVXPY abstraction, OSQP, SCS, optional commercial solvers |
| Finance | arch where justified; QuantLib only for an optional instrument/quant subpack |
| Incremental | River only for genuine streaming semantics |
| Local AI | llama.cpp, Transformers, PEFT/LoRA, optional MLflow |

## Model selection and causal boundary

There is no universal best model. Meaningful baselines are mandatory. Selection depends on target semantics, data and sample size, grain, horizon, temporal structure, class balance, explainability, uncertainty, compute, license policy, resources, comparative validation, and Trust.

Candidate families may include linear/logistic and regularized models, trees and ensembles, gradient boosting, statistical/time-series methods, Bayesian methods where justified, and volatility models when semantics require them. Temporal problems require time-aware validation rather than inappropriate random splits.

The governing distinction is:

```text
correlation != prediction != attribution != causation
```

Causal activation requires defensible treatment, outcome, confounders, identification assumptions, and validation/refutation. Optimization is also distinct from prediction and simulation.

## Simulation architecture

### Exact simulation bases

The canonical simulation bases are exactly:

- DATA_BASED
- MIXED
- INTENT_BASED

No fourth canonical basis is permitted.

DATA_BASED relies primarily on observed or derived first-party data and validated formulas/models. MIXED combines empirical evidence with explicit assumptions, analogs, benchmarks, synthetic support, or external evidence. INTENT_BASED begins from a user objective where empirical support may be incomplete and must expose assumptions and limitations.

Intent-based simulation never masquerades as observed truth.

### ScenarioIntentManifest

The versioned ScenarioIntentManifest conceptually records:

- domains;
- objective and outcome;
- horizon;
- geography;
- population or entity;
- resources and goals;
- controls and constraints;
- assumptions;
- comparison basis;
- uncertainty preference;
- evidence access;
- consent snapshot.

### CompositeSimulationGraph

The CompositeSimulationGraph is the universal simulation/execution abstraction. Nodes may represent:

- deterministic formula;
- statistical, ML, time-series, or causal model;
- Monte Carlo;
- optimizer;
- synthetic generator/support;
- benchmark or analog;
- external-evidence transform;
- user assumption;
- constraint.

Edges explicitly distinguish:

- deterministic relation;
- observed association;
- predictive relation;
- causal estimate;
- assumption;
- external prior;
- analog prior;
- constraint.

No defensible relation means constrain or refuse; the graph must not fabricate an edge.

## Composite/Cross-Domain capability

Composite/Cross-Domain is first-class but never guaranteed. Representative paths include Marketing response through commercial and cash concepts, Product price or launch through demand/inventory/margin/working capital, and Customer Experience through satisfaction/retention/customer value.

These are examples, not hardcoded flows. Every edge remains subject to semantic, grain, time, unit, currency, evidence, support, license, model/engine, and Trust validation.

## Finance Domain Experience

Finance is dynamically activated and does not impose one mandatory schema. Its capability families include:

- Corporate Performance and FP&A;
- Actual/Budget/Forecast and variance;
- profitability, margin, contribution, and unit economics;
- forecasting;
- Treasury and Liquidity;
- AR/AP, cash, working capital, debt, interest, and FX where supported;
- three-statement relationships;
- Risk and Stress;
- Credit and Collections;
- Valuation and Capital Investment;
- optional Quant Finance and instrument capabilities.

Prediction, deterministic accounting logic, simulation, stress testing, and optimization remain distinct. Accounting relationships must reconcile. QuantLib is reserved for optional specialized instrument use and does not contaminate ordinary FP&A.

## Trust and Evidence Profile

Trust remains independent of model or LLM confidence. Its dimensions include:

- data quality;
- semantic confidence;
- relationship validity;
- model validation;
- temporal leakage;
- support and extrapolation;
- constraints;
- accounting reconciliation;
- unit, currency, time, and calendar consistency;
- simulation support;
- optimization feasibility;
- privacy;
- outbound policy;
- licensing;
- reproducibility.

Green, Amber, and Red remain the conceptual outcomes.

The **Evidence Profile** is separate from Trust. It describes dependence on:

- first-party observed data;
- observed outcomes;
- assumptions;
- synthetic data;
- analogs;
- external evidence;
- extrapolation;
- evidence freshness;
- evidence coverage.

Evidence Profile is not a duplicate Trust score.

## Provenance

Frozen conceptual provenance classes:

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

Synthetic provenance retains generator, provider, version, seed, configuration, quality evaluation, and privacy evaluation. Synthetic records never silently become observed truth.

## Governed learning and circular-contamination prevention

```text
Every simulation becomes a learning experience;
not every simulation becomes empirical truth.
```

Evidence authority tiers preserve the distinction:

1. observed actual outcomes;
2. derived observed data with lineage;
3. data-based simulation experience;
4. mixed simulation experience;
5. intent-based simulation experience;
6. LLM proposals and other unverified proposals.

The **SimulationLearningStore** retains scenario intent, basis, domains, inputs, controls, constraints, assumptions, evidence, models, graph, outputs, uncertainty, Trust, Evidence Profile, user actions/corrections, and later observed outcomes. It is logically separate from empirical analytical data.

**OutcomeReconciliation** connects:

```text
Simulation at T0
  → Real-world execution
  → Observed actual at T1
  → Prediction vs actual
  → Error attribution
  → Model / assumption / evidence evaluation
  → Learning candidate
```

Learning candidates pass a LearningEligibilityGate, governed Training Dataset Builder, leakage and provenance validation, challenger evaluation, Trust, champion comparison, and promote/reject decision. One simulation does not directly retrain a model. Governed batch retraining is the default; incremental learning is allowed only when genuine streaming semantics justify it.

Intent-based outputs, mixed assumptions, synthetic records, LLM-proposed numbers, and unverified external evidence cannot be promoted directly to empirical truth.

## LLM and evidence-access architecture

Exact LLM modes:

- ML_ONLY
- LOCAL_LLM
- REMOTE_LLM
- HYBRID_LLM

ML, statistics, and deterministic engines retain numerical authority. LLMs may assist with semantics, intent, clarification, domain reasoning, analog ranking, evidence planning, explanation, and organization vocabulary. All operational outputs remain structured and validated.

Exact evidence-access modes:

- OFF
- INTERNAL_ONLY
- PUBLIC_WEB
- APPROVED_CONNECTORS

Effective outbound permission is:

```text
Admin policy ∩ project/dataset policy ∩ runtime user consent
```

PUBLIC_WEB and APPROVED_CONNECTORS are architecture modes, not current v0.1.0 services. Continuous governed retrieval and memory are preferred before optional PEFT/LoRA adaptation. Weight adaptation uses curated learning events and never grants numerical authority.

## UI architecture

The target product identity is IPSP. Target navigation is:

- Home / Overview;
- Projects / Workspaces;
- Data;
- Analysis & Simulation, with capability-driven Marketing, Product, Sales, Customer Experience, Finance, Operations, Generic/Custom, and Composite/Cross-Domain entries;
- Scenario Library;
- Compare;
- Models & Learning;
- Jobs;
- Administration;
- Profile.

Domain pages are capability-driven, not guaranteed static screens.

The canonical simulation workflow has exactly five steps:

1. Define
2. Configure
3. Enrich & Validate
4. Run
5. Results & Compare

CampaignSim remains historical visual reference only.

## Backend and storage architecture

```text
Adaptive Frontend
  → FastAPI / API
  → Authentication / RBAC / Policy / Consent
  → Ingestion / Storage
  → Data Understanding
  → Semantic + Metric Layer
  → Domain Experience Activation
  → Cross-Domain Composition
  → Capability Discovery
  → Scenario + Evidence
  → Engine & License Resolver
  → Composite Simulation Graph
  → Trust + Evidence Profile
  → Results / Compare / History / Export
  → Learning / Reconciliation
  → Model + Local-AI Improvement
```

Cross-cutting requirements are security, privacy, outbound policy, secrets, jobs, observability, provenance, licensing, configuration, and reproducibility.

Storage remains two-plane:

- SQLite stores control, governance, knowledge, registry, and operational metadata;
- source files and Parquet hold analytical data.

SQLite is not the mandatory large analytical warehouse. Provider and repository boundaries preserve future portability.

## Bounded v1.0 scope

v1.0 is the first complete, production-usable expression of IPSP, not every capability IPSP may ever support.

Expected v1.0 capability includes:

- secure local-first projects/workspaces;
- structured ingestion, versioning, and provenance;
- deterministic understanding and Dataset Semantic Manifest;
- relationship and grain validation;
- Metric & Formula Registry;
- Domain Experience framework and baseline domain experiences;
- Capability Discovery and responsible refusal;
- core statistical/ML modelling, forecasting, explainability, and model lifecycle;
- EngineRegistry, LicenseRegistry, and open-source-preferred resolution;
- all three simulation bases;
- ScenarioIntentManifest and CompositeSimulationGraph;
- basic defensible Cross-Domain simulation;
- Monte Carlo where valid;
- Trust and Evidence Profiles;
- scenario history, compare, re-run, and reproduce;
- SimulationLearningStore and OutcomeReconciliation foundation;
- governed champion/challenger learning;
- optional local LLM assistance;
- PDF/Excel export;
- full capability-driven UI.

The following may mature after v1.0 without blocking it:

- advanced production causal workflows;
- full solver-backed optimization;
- automatic LLM fine-tuning;
- Remote/Hybrid LLM;
- PUBLIC_WEB evidence;
- enterprise connectors;
- distributed enterprise infrastructure;
- specialized Quant Finance.

## Conformance requirements

Every later reconciliation and implementation phase must prove:

- current implementation claims match code and accepted evidence;
- frozen/planned capability is never advertised as operational;
- domain and benchmark knowledge does not contaminate generic core;
- provider choice cannot bypass capability, license, Trust, or resource gates;
- relationship composition cannot bypass grain, time, unit, currency, or evidence checks;
- simulation and synthetic experience cannot silently become observed truth;
- LLM proposals cannot become numerical authority;
- v0.1.0 acceptance history remains intact;
- v0.2 remains unimplemented until its separately accepted contract freeze and workstream authorization.

## Related authority

- [Scope Freeze](00_SCOPE_FREEZE.md)
- [Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md)
- [Decision Log](32_DECISION_LOG.md)
- [Implementation Progress](31_IMPLEMENTATION_PROGRESS.md)
- [Anti-Contamination Rules](40_ANTI_CONTAMINATION.md)
- [Parallel Development Workflow](41_PARALLEL_DEVELOPMENT_WORKFLOW.md)
