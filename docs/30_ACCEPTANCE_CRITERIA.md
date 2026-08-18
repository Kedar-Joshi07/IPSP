# V1.0 Acceptance Criteria

## Acceptance boundary

IPSP v1.0 is the first complete, production-usable expression of the frozen
[F-002 architecture](44_F002_ARCHITECTURE_FREEZE.md). It is ready only when every mandatory
criterion below has accepted evidence. A frozen contract is not proof of implementation, and a
provider being installed is not proof of capability.

## Governance
- Admin/User login and permissions enforced server-side.
- Role-to-permission mapping is the sole authorization authority; no persisted admin Boolean is used.
- Dataset permissions work.
- Passwords securely hashed.
- Session tokens rotate on login, expire, invalidate on logout/password/role changes, are not logged raw, and state-changing browser requests enforce CSRF.
- Failed logins are throttled/temporarily locked and required production secrets fail closed.
- Remote/internet policy blocks disallowed calls.
- Secrets are not stored/logged in plaintext.

## Data
- All supported structured formats ingest safely.
- Multi-sheet/multi-table metadata supported.
- Candidate grain, roles, relationships, hierarchies, lineage, sampling provenance produced.
- Unsafe joins are detected.
- Semantic conflicts produce questions instead of silent assumptions.
- Dataset Semantic Manifest versions provide the evidence needed for domain, metric, capability, scenario, Trust/Evidence, and learning decisions.

## Capability
- Unsupported capabilities are visibly disabled with reasons.
- At least one regression/classification/forecast or other predictive path can be validated on suitable data.
- Metric & Formula Registry definitions are versioned, deterministic, grain/time/unit/currency safe, and reproducible.
- Registered Domain Experiences activate only when semantic prerequisites pass; generic core remains domain neutral.
- EngineRegistry, Runtime Engine Inventory, LicenseRegistry, and EngineResolver distinguish validity, availability, eligibility, and refusal.
- Deterministic what-if works without ML where formula semantics are confirmed.
- Similarity/look-alike path is available only when appropriate.

## Trust
- Predictive models beat or meaningfully justify themselves over baselines before enablement.
- Leakage checks run.
- Constraint classes are respected.
- P10/P50/P90 ordering and coverage checks exist where uncertainty is shown.
- Causal language is blocked/downgraded without causal support.
- Cross-domain paths reconcile entity/grain/cardinality, time/calendar, unit/currency, transformation, evidence, and support; unsupported edges are refused.
- Accounting relationships reconcile where applicable; a material unexplained imbalance is not hidden.
- Trust and Evidence Profile are separate, visible authorities.

## Simulation and learning

- ScenarioIntentManifest supports exactly `DATA_BASED`, `MIXED`, and `INTENT_BASED` with explicit assumptions, evidence access, and consent snapshots.
- CompositeSimulationGraph executes only validated typed nodes and edges; blocked or partial paths remain explicit.
- Synthetic support retains `SYNTHETIC_DATA` provenance and never silently becomes observed truth.
- SimulationLearningStore remains separated from empirical analytical data.
- OutcomeReconciliation matches mature actuals without rewriting the original run or observed outcome.
- Learning candidates pass eligibility, governed dataset construction, leakage/provenance, challenger, Trust, and authorized promotion gates; one simulation never directly retrains a champion.
- Optional Local LLM assistance remains structured, validated, privacy-governed, license-governed, and without numerical authority. IPSP remains useful when it is disabled.

## UI
- Entire app presents IPSP as the product identity and uses the historical visual reference only as design input.
- Dark and light themes complete.
- Shared dark/light tokens, switching, and preference persistence exist in the v0.1.0 foundation.
- Browser dependencies are pinned and vendored; production has no public-CDN runtime dependency.
- Dataset workflow and the exact simulation flow `Define → Configure → Enrich & Validate → Run → Results & Compare` function.
- Dynamic controls and results are metadata-driven.
- Domain and Composite/Cross-Domain entries are capability-driven, not guaranteed static pages.

## Operations
- Trace IDs propagate.
- Audit events use a non-secret `session_correlation_id` and high-volume runtime logs use an appropriate structured sink.
- Foundation job interfaces/schema cover status, progress, cancellation, retry, and safe errors without requiring Redis/Celery.
- Liveness, readiness, and authorized Admin diagnostics are separate and safe.
- Audit/security/ML/LLM/simulation/export errors are logged safely.
- Run history supports re-run/reproduce.
- Completed runs reference exact immutable dataset/semantic/capability/model versions, seed, and effective non-secret configuration snapshot/hash.
- PDF and Excel export from persisted Run Result Object.
- Basic health and backup/restore are functional.

## Explicit post-v1.0 deferrals

The following do not block v1.0 when their foundation boundaries remain preserved and the product does not claim they are operational:

- advanced production causal workflows;
- full solver-backed optimization;
- automatic Local LLM PEFT/LoRA lifecycle;
- Remote and Hybrid LLM execution;
- `PUBLIC_WEB` evidence access;
- `APPROVED_CONNECTORS` and enterprise business/warehouse connectors;
- enterprise identity, PostgreSQL, distributed workers, Redis, Celery, Kubernetes, object storage, and multi-node scale;
- specialized Quant Finance and instrument pricing.

Deferral never waives mandatory security, privacy, provenance, licensing, Trust, Evidence Profile, reproducibility, responsible refusal, or the provider-neutral foundation contract.
