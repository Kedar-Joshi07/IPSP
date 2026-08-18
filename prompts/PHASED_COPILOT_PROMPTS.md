# Phased GitHub Copilot Implementation Prompt Map

## Authority and use

This is a high-level map of the frozen application sequence. It is not an implementation prompt and
does not authorize any milestone. Before coding, read `AGENTS.md`, scoped instructions, the F-002
architecture and roadmap freezes, active-workstream governance, relevant specifications, and the
previous accepted milestone evidence.

Every milestone requires a dedicated detailed prompt and accepted contract freeze that identifies:

- exact base SHA, branch, owner, merge target, and other active workstreams;
- owned, shared/integration-sensitive, and forbidden paths;
- functional, data/schema, API/interface, acceptance, and dependency/license contracts;
- migration owner, dependency owner, and stop conditions;
- branch gate, post-merge integration gate, and milestone acceptance gate.

Do not infer missing ownership, install a planned provider, or begin a milestone because it appears
below. A branch PASS is not a milestone PASS. Kedar owns integration and promotion.

## Current gate — v0.1.1 F-002 architecture reconciliation

F2-A through F2-H reconcile architecture and governance. F2-I is the minimal production
compatibility reconciliation and may start only after independent F2-H PASS. F2-J is the independent
v0.1.1 final acceptance audit. No v0.2 implementation begins within this sequence.

Gate: accepted F2-J evidence is required before any separately authorized v0.2 contract-freeze
preparation.

## v0.2.0 — Data ingestion, storage, and provenance

Freeze and implement secure structured ingestion, immutable originals, canonical analytical
references, dataset/table/version identities, staging/quarantine, validation, and sampling/source
provenance. Preserve the SQLite control plane and source/Parquet analytical plane. Do not begin
business-semantic inference beyond this milestone's accepted structural contract.

Gate direction: safe supported formats, immutable/reproducible versions, traversal/archive defenses,
provenance, and accepted persistence/API contracts.

## v0.3.0 — Deterministic Data Understanding and relationships

Freeze and implement deterministic profiling, physical/semantic evidence candidates, grain, keys,
entities, measures/dimensions/time/units, lineage, hierarchies, relationship/cardinality proposals,
join-safety analysis, sensitivity candidates, and sampling-aware evidence. No LLM dependency and no
benchmark special cases.

Gate direction: renamed and multi-domain fixtures produce generic evidence, unsafe joins refuse, and
sample metadata is not mistaken for full-population sufficiency.

## v0.4.0 — Semantic intelligence and Dataset Semantic Manifest

Freeze and implement versioned semantic proposals, evidence/confidence, ambiguity/conflict,
clarification and confirmation, relationship resolution, horizon/availability, units/currency/time,
constraints, and Dataset Semantic Manifest persistence/API contracts. LLMs, if not yet implemented,
remain replaceable proposal sources rather than requirements.

Gate direction: dependent capabilities remain blocked until material ambiguity is resolved and exact
manifest versions are reproducible.

## v0.5.0 — Metric & Formula Registry and Domain Experience foundation

Freeze and implement provider-neutral Domain Experience manifests/registry/activation and the
versioned Metric & Formula Registry, safe expression/dependency evaluation, precedence/conflicts,
grain/time/unit/currency/null rules, lineage, and compatibility. Domain packs request semantic metric
IDs; they never become formula engines or impose source columns.

Gate direction: multi-domain activation is evidence-driven, formulas are deterministic and validated,
and generic core contains no domain/benchmark branching.

## v0.6.0 — Capability Discovery and Engine/License Registry

Freeze and implement evidence-first capability decisions, EngineRegistry, factual Runtime Engine
Inventory, LicenseRegistry, organization modes, deterministic EngineResolver, explicit fallback,
resource/security checks, and reasoned limitation/refusal. Do not install candidate libraries without
the milestone dependency/license contract.

Gate direction: capability validity precedes provider choice; unavailable, unlicensed, unsafe, or
unsuitable providers cannot be selected or silently substituted.

## v0.7.0 — Core modelling and model lifecycle

Freeze and implement meaningful baselines, eligible statistical/ML/forecast candidates, leakage-safe
split strategy, calibration/uncertainty where valid, explainability, immutable artifacts, registry
states, challenger/champion evaluation, monitoring, rollback, and refusal. Preserve prediction,
attribution, and causal distinctions.

Gate direction: no universal model winner, target/horizon/availability semantics are enforced, and
promotion requires accepted comparative evidence.

## v0.8.0 — Simulation core and universal scenario/execution contracts

Freeze and implement exactly `DATA_BASED`, `MIXED`, and `INTENT_BASED`, versioned
ScenarioIntentManifest, typed CompositeSimulationGraph foundation, deterministic/model/Monte Carlo/
assumption/constraint nodes where eligible, jobs, safe partial/refusal behavior, and result lineage.
Synthetic and optimizer nodes remain provider/license gated.

Gate direction: graph execution cannot create semantic authority; intent and synthetic support never
masquerade as observation.

## v0.9.0 — Trust, Evidence, history, and comparison

Freeze and implement expanded Trust dimensions, separate Evidence Profile, result persistence,
Scenario Library, compare, re-run, exact reproduce, and authorized PDF/Excel export. Preserve basis,
evidence, consent, provider/license, seed, code, and non-secret configuration snapshots.

Gate direction: no result bypasses Trust, Evidence Profile is not a duplicate score, and unavailable
historical components are reported rather than silently replaced.

## v0.10.0 — Cross-Domain Composite intelligence

Freeze and implement validated CrossDomainSemanticGraph composition and CompositeSimulationGraph
execution across activated Domain Experiences. Reconcile entity/grain/cardinality, time/calendar,
units/currencies, transformations, evidence, support, and provenance; refuse unsupported edges.

Gate direction: defensible multi-domain fixture paths work generically and incompatible or fabricated
relations fail safely.

## v0.11.0 — Domain intelligence completion

Freeze and complete the baseline Domain Experience families and capability-driven metadata, including
Finance accounting, planning, three-statement, risk/stress, and other supported families without
fixed schemas. Numerical truth remains in registries and generic compute services.

Gate direction: domains activate dynamically, accounting/unit/currency/time relations reconcile, and
specialized Quant Finance remains optional/deferred.

## v0.12.0 — Learning and Outcome Reconciliation foundation

Freeze and implement SimulationLearningStore separation, observed-actual matching,
OutcomeReconciliation, LearningEligibilityGate, governed Training Dataset Builder, leakage/provenance
validation, mature-outcome evaluation, and governed challenger/champion learning. Batch retraining is
the default.

Gate direction: no simulation, assumption, synthetic, benchmark, external, correction, or LLM
proposal directly becomes observed truth or an empirical training row.

## v0.13.0 — Local AI

Freeze and implement optional Local LLM structured semantic assistance, governed local knowledge/
retrieval memory, provider/model-weight licenses, privacy/consent, evaluation, and only then optional
adaptation challengers if justified. The product remains fully functional without Local AI.

Gate direction: deterministic/evidence validators retain authority; fine-tuning never grants
numerical authority.

## v0.14.0 — Full dynamic product UI

Freeze and implement the IPSP product identity, capability-driven navigation and domain experiences,
dataset workflows, the exact five-step simulation flow, Trust/Evidence, history/compare, models/
learning, jobs, administration, themes, accessibility, responsive behavior, and safe errors. Historical
prototype material is design reference only.

Gate direction: no domain-specific hardcoded pages/controls/results, no public-CDN runtime dependency,
and UI cannot imply an unavailable capability.

## v0.15.0 — v1.0 release candidate and hardening

Integrate and harden all mandatory bounded-v1.0 behavior: security, privacy, licensing, provenance,
performance, reliability, recovery, observability, accessibility, exports, scale appropriate to the
accepted contract, architecture conformance, multi-domain benchmarks, and release documentation.

Gate direction: a complete evidence map to `docs/30_ACCEPTANCE_CRITERIA.md`, independent review, and a
formal v1.0.0 acceptance decision.

## v1.0.0 — First General Availability

Create a release/tag only after the accepted v0.15.0 candidate passes the independent milestone
acceptance gate and Kedar authorizes promotion. Advanced production causal workflows, full
solver-backed optimization, automatic LLM adaptation, Remote/Hybrid LLM, public-web evidence,
enterprise connectors/distributed scale, and specialized Quant Finance are post-v1.0 deferrals when
their foundation boundaries remain preserved.
