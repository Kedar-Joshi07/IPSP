# Engine & License Registry Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.6.0 — Capability Discovery + Engine/License Registry

This specification freezes the provider-neutral `EngineRegistry`, `LicenseRegistry`, and
`EngineResolver` contracts. It does not install packages, inspect the current environment, create
runtime tables/APIs, train models, or implement optimization/causal execution.

## Governing separation

```text
Semantic and data-valid capability
  → valid engine families
  → installed and available providers
  → license/security/resource eligibility
  → deterministic resolution or refusal
```

Capability Discovery owns the first two decisions. Engine/License services cannot turn an invalid
semantic/data path into a valid capability. Installation alone never establishes validity or
approval.

## Provider interfaces

Application services depend on typed IPSP provider interfaces rather than vendor libraries. Planned
families may include:

- deterministic formula/metric evaluator;
- statistical and econometric engine;
- machine-learning training/scoring provider;
- forecasting/time-series provider;
- causal-analysis provider;
- Monte Carlo provider;
- synthetic-data/support provider;
- optimizer/solver provider;
- Finance-specific optional provider;
- explainability/tuning provider;
- local, remote, or hybrid LLM provider.

An implementation may combine compatible families behind one adapter or expose multiple adapters.
Provider design must preserve capability, policy, license, security, resource, and reproducibility
metadata.

## EngineRegistry

`EngineRegistry` is the versioned catalog of provider declarations. An engine record conceptually
contains:

| Area | Metadata |
|---|---|
| Identity | Engine/provider ID, adapter version, provider interface/family, display name, provenance |
| Capability | Supported task/capability IDs, input/output types, uncertainty/calibration/explainability support |
| Runtime | Library/runtime name and version, artifact compatibility, determinism/seed behavior |
| Availability | Declared, installed, loadable, healthy, enabled, and last-verified facts kept distinct |
| Resources | CPU architecture, memory, disk, GPU/accelerator, operating-system, concurrency, and latency constraints |
| Security | Isolation, local/remote execution, data-transmission behavior, known restrictions, and approval state |
| Licensing | Dependency, model-weight, solver/commercial, and other LicenseRegistry references |
| Governance | Organization eligibility, configuration source, feature flag, owner, audit, and reason metadata |

Registry declarations are schema-validated. They do not prove that a package is currently installed,
healthy, licensed for use, suitable for a dataset, or allowed by organization policy.

## Runtime Engine Inventory contract

A later runtime implementation must produce a factual, timestamped inventory separate from target
architecture and static registry declarations. Each verification snapshot conceptually records:

- engine/provider ID and declared adapter version;
- installed/loadable/available status and safe failure reason;
- discovered library/runtime version and artifact compatibility;
- hardware/resource facts and capacity limits;
- security/configuration readiness without exposing secrets;
- referenced license-decision versions and expiry/verification state;
- health verification method/time and provenance.

Unknown, never-checked, not-installed, unavailable, and blocked are distinct. Documentation candidate
lists never populate runtime inventory automatically. Exact discovery mechanisms, persistence, APIs,
and refresh behavior are deferred to later freezes.

## LicenseRegistry

`LicenseRegistry` is the versioned authority for legal/policy metadata and decisions. It keeps
separate records for:

- direct/transitive dependency license;
- model-weight or model-bundle license;
- solver or commercial-provider license;
- dataset, benchmark, or external-evidence license where applicable;
- adapter/application compatibility and redistribution/service constraints.

License metadata conceptually includes:

- subject identity, type, version, source, checksum/reference, and license identifier/class;
- commercial-use status;
- redistribution, modification, hosted-service, and network/service restrictions;
- geographic, organizational, user-count, hardware, expiry, or purpose restrictions where present;
- model-weight terms independently from code terms;
- approved/prohibited uses, review owner, evidence, decision version, and expiry/review date;
- unresolved or conflicting terms and safe reason codes.

Legal/policy review evidence is versioned and auditable. Absence of known restrictions is not proof
of permission.

## Frozen license classes

- `PERMISSIVE_OPEN_SOURCE`
- `PUBLIC_DOMAIN`
- `COPYLEFT_OPEN_SOURCE`
- `SOURCE_AVAILABLE`
- `COMMERCIAL`
- `CUSTOM_MODEL_LICENSE`
- `UNKNOWN/BLOCKED`

Classification does not itself decide use. Organization policy and specific terms still apply.

## Organization policy modes

- `OPEN_SOURCE_ONLY`
- `OPEN_SOURCE_PREFERRED` — default
- `COMMERCIAL_ALLOWED`

`OPEN_SOURCE_ONLY` excludes commercial/source-available/custom subjects unless an explicit policy
defines them as eligible. `OPEN_SOURCE_PREFERRED` selects an eligible open-source provider when one
meets capability, Trust, suitability, performance, and resource requirements; it does not choose an
invalid provider simply because its license is preferred. `COMMERCIAL_ALLOWED` permits reviewed
commercial providers but never bypasses other gates.

## License gate

For a specific provider/capability/organization/use context, LicenseRegistry returns:

- `ALLOW` — required license subjects and intended use are approved;
- `WARN` — use may proceed only under recorded conditions/review requirements that do not violate
  a hard policy;
- `BLOCK` — use is prohibited, unknown, expired, conflicting, or missing mandatory approval.

The decision includes exact subject versions, organization mode, intended use, reasons, conditions,
review evidence, and expiry. A warning cannot override a mandatory block. Dependency approval never
silently approves model weights, solver rights, or hosted-service use.

## EngineResolver inputs

Resolution is deterministic for an exact request snapshot containing:

- validated capability and eligible engine families;
- Dataset Semantic Manifest, metric, relationship/graph, and scenario requirements;
- required outputs, uncertainty, calibration, explainability, causal/optimization features;
- data size/shape/support and privacy/transmission constraints;
- Runtime Engine Inventory facts;
- LicenseRegistry decisions and organization policy mode;
- Trust requirements, validation evidence, performance/latency needs, and available resources;
- organization preferences, feature flags, and non-secret configuration version.

## Frozen resolver priority

1. capability validity;
2. license policy;
3. Trust and validation;
4. data suitability;
5. performance;
6. available resources;
7. organization preference.

Priority is lexicographic governance, not a weighted score that permits a lower criterion to waive a
higher failure.

## Resolution result

The result conceptually records:

- selected provider ID/version or no-selection outcome;
- considered candidates and exclusion reasons;
- exact capability, registry, inventory, license, policy, and Trust references;
- resource allocation/limits and fallback policy;
- deterministic tie-break reason;
- warnings, conditions, reproducibility snapshot/hash, and audit/trace reference.

If no eligible provider exists, the capability is limited, disabled, blocked, or refused with safe
reasons. Silent fallback to an unlicensed, unvalidated, remote, or semantically different provider is
prohibited.

## Representative provider candidates

The following are architecture candidates only. Their presence here does not mean installed,
approved, secure, compatible, or operational.

| Family | Representative candidates and boundary |
|---|---|
| Application/data | FastAPI, Uvicorn, SQLAlchemy, SQLite, Polars, Arrow/PyArrow, Pandas where needed |
| ML | scikit-learn, LightGBM, XGBoost, CatBoost behind modelling/provider contracts |
| Statistics/econometrics | Statsmodels, arch, and PyMC where justified |
| Causal | DoWhy, EconML, and optional causal-learn after causal activation |
| Explainability/tuning | SHAP and Optuna where compatible and licensed |
| Synthetic | Synthcity as preferred permissive candidate; SDV optional subject to current license policy |
| Optimization | CVXPY abstraction with OSQP/SCS preferred open-source solver candidates; optional commercial solvers |
| Finance | arch where valid; QuantLib only for an optional specialized instrument/quant subpack |
| Incremental | River only when genuine streaming semantics justify it |
| Local AI | llama.cpp, Transformers, PEFT/LoRA, and optional MLflow subject to code/model licenses |

Provider examples never become mandatory dependencies or generic routing constants.

## Synthetic-provider boundary

Synthetic capability uses a generic provider interface. Synthcity is the preferred permissive
candidate. SDV remains optional and may be used only when its current license, intended use,
security, data suitability, quality/privacy validation, and organization policy pass.

Synthetic records retain generator, provider, version, seed, configuration, quality, privacy, and
lineage metadata. Provider selection never lets synthetic data silently become observed truth.

## Causal boundary

```text
correlation != prediction != attribution != causal effect
```

Causal capability activates only when treatment, outcome, confounders, identification assumptions,
temporal ordering, overlap/support, sensitivity/refutation, and validation evidence are defensible.
DoWhy and EconML are provider candidates, not v0.1.1 dependencies and not proof that causality is
identified.

## Optimization boundary

Optimization is not prediction. Activation requires a declared objective, decision variables,
constraints, feasibility, uncertainty treatment, validated response/accounting relationships,
solver capability, and license/resource eligibility.

The target uses a CVXPY abstraction with OSQP and SCS preferred where valid. Commercial solvers are
optional, explicitly licensed, and never required for the bounded v1.0 foundation. F2-D does not
implement optimization runtime.

## Security, privacy, and outbound behavior

Provider metadata declares local/remote behavior and raw/derived data needs. Effective outbound use
remains the intersection of Admin policy, project/dataset policy, and runtime consent. Secrets are
references resolved through SecretProvider and are never stored in registry/inventory records.

An unavailable credential, prohibited transmission, unsafe provider, or unknown security state
blocks use rather than triggering an ungoverned fallback.

## Reproducibility and audit

Runs/models reference exact engine/provider/adapter/library versions, Runtime Engine Inventory
snapshot, dependency/model-weight/solver license decisions, resolver input/result, resources,
non-secret configuration, and policy/Trust evidence. Reproduce reports unavailable historical
providers honestly; it does not silently substitute a current provider.

## Deferred implementation detail

F2-D freezes ownership, metadata, gates, and policy only. Exact registry/inventory persistence,
discovery probes, health checks, APIs, plugin loading, dependency installation, solver adapters,
security isolation, and runtime execution require later contract freezes and accepted milestones.

## Related contracts

- [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md)
- [Capability Discovery](11_CAPABILITY_DISCOVERY_SPEC.md)
- [Modelling Engine](12_MODELING_ENGINE_SPEC.md)
- [Model Registry & Lifecycle](13_MODEL_REGISTRY_LIFECYCLE_SPEC.md)
- [Trust & Validation](15_TRUST_AND_VALIDATION_SPEC.md)
- [Metric & Formula Registry](46_METRIC_FORMULA_REGISTRY_SPEC.md)
- [Domain Experience Pack](47_DOMAIN_EXPERIENCE_PACK_SPEC.md)
- [Configuration](35_CONFIGURATION_SPEC.md)
