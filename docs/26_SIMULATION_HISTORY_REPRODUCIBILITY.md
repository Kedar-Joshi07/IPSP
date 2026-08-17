# Simulation History & Reproducibility

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

This specification freezes scenario-history identity and the distinction between re-run and
reproduce. It does not create persistence tables, APIs, jobs, or replay services.

## Run identity and history

Use a stable opaque run ID with an optional friendly display ID such as `SIM-YYYYMMDD-NNNNNN`.
History preserves immutable run/result versions, actor and timestamps, lifecycle/audit references,
parent/comparison/supersession relationships, partial/refused state, and artifacts.

User actions include open, compare, re-run, reproduce, export PDF, and export Excel, subject to
current authorization and policy. Viewing history never grants access to an upstream source,
evidence item, provider, or artifact that the current actor is not permitted to access.

## Exact definitions

- **Re-run:** the same frozen scenario intent is submitted against **current eligible state**. Current
  semantic/metric/model/engine/evidence/policy versions may be resolved, and the resulting run records
  every change from the prior run.
- **Reproduce:** the system attempts to execute using the **original frozen versions and state** that
  produced the historical result.

Re-run is not evidence that a historical result can be reproduced. Reproduce never silently selects
a newer model, provider, formula, graph, evidence item, assumption, policy, or configuration. If an
original component is unavailable or current safety/authorization prohibits access, the attempt
reports a structured limitation/refusal rather than claiming exact reproduction.

## Reproduction manifest

Each run/result retains an immutable reproduction manifest or references sufficient immutable records
to resolve:

- run/result, application, contract/schema, and code/build versions;
- project/workspace, dataset/table/source artifact, sampling, and Dataset Semantic Manifest versions;
- Domain Experience manifests/activations and CrossDomainSemanticGraph version;
- ScenarioIntentManifest, canonical simulation basis, and CompositeSimulationGraph version/hash;
- Metric & Formula Registry definitions, dependency graph, source mappings, transformations,
  aggregation, unit/currency conversions, and validation versions;
- capability decision, model/artifact/baseline/explainability versions and validation evidence;
- engine/provider/adapter/library/runtime versions, Runtime Engine Inventory snapshot,
  EngineResolver result, resources, and dependency/model-weight/solver/data/evidence license decisions;
- original evidence snapshot/cutoff and all provenance references, including synthetic generator,
  provider, version, seed, configuration, quality, and privacy metadata where applicable;
- baseline/comparison basis, controls, constraints, assumptions, uncertainty/distributions,
  reconciliation rules/tolerances, and random seeds/determinism behavior;
- effective permission, privacy, outbound, organization, consent/evidence-access, license, feature,
  and other policy context relevant to execution;
- effective non-secret numerical/runtime configuration or immutable retrievable snapshot/hash;
- Trust rule/check versions and decomposition, separate Evidence Profile, warnings, limitations,
  refusals, audit/trace, result artifacts, and checksums.

Credential values, auth cookies, API keys, and other secrets are never retained in the reproduction
manifest. It stores governed references and availability facts only.

## Re-run comparison

A re-run begins from the same immutable intent version unless the user explicitly creates a new
intent version. Before execution, it resolves current eligible dependencies and presents or records a
change set covering at least evidence/data, semantics, Domain Experiences, metrics, graph, assumptions,
models/providers, licenses, policy/consent, configuration, and Trust rules.

Material changes may alter basis, capability, support, or output eligibility. If the current state
cannot honor the original intent, the re-run is limited or refused with reasons; it does not quietly
change the objective or controls.

## Reproduce behavior and equivalence

Reproduction validates current authorization and safety while resolving original frozen state. It
records exact, numerically equivalent within a declared tolerance, artifact-equivalent, partially
reproduced, or not reproducible as distinct outcomes. The applicable equivalence definition,
tolerances, deterministic/nondeterministic provider behavior, platform/resource differences, and
comparison diagnostics are explicit.

Historical provider/library unavailability, revoked licenses, inaccessible evidence, expired consent,
removed data, nondeterministic hardware/runtime behavior, or integrity mismatch may prevent execution.
These facts remain auditable. A substitute can be used only in a new re-run, never in a result labeled
as reproduction of the original execution.

## Comparison and evidence meaning

History comparison aligns result versions, semantic/metric definitions, population/entity/grain,
period/calendar, units/currencies, basis, assumptions, evidence cutoff/composition, graph paths,
model/provider, and Trust rules before presenting deltas. Non-comparable differences are labeled and
not coerced into a numeric comparison.

A prior run remains `PRIOR_IPSP_RUN`; simulated output never becomes observed data. A later actual
may be stored separately as `OBSERVED_OUTCOME` and linked through governed outcome reconciliation in
a later F-002 contract. Reproduction does not promote evidence class.

## Retention, integrity, and safe failure

History and artifacts follow retention, backup, privacy, permission, and license policy. Immutable
checksums and audit/trace references support integrity. Missing, corrupted, unauthorized, blocked, or
expired dependencies produce safe structured reasons without secrets or raw stack traces.

## Deferred implementation detail

Exact persistence schemas, APIs, identifiers, comparison algorithms, tolerance catalogs, archival
formats, dependency capture, replay isolation, and UI controls are deferred to later contract freezes
and accepted milestones.
