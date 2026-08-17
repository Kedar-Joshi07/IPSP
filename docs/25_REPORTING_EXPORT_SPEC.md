# Reporting & Export Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

This specification freezes result/report content and governance only. It does not implement PDF,
Excel, or another export path.

## Principle

Reports are generated from a persisted **Run Result Object**, never by screenshotting the browser.
An export is a governed representation of an immutable result version; it does not recompute a
scenario, change evidence meaning, or suppress a failed path.

## Run Result Object

The result conceptually includes:

- run/user/time, project/workspace, dataset/table and Dataset Semantic Manifest versions;
- exact ScenarioIntentManifest version and canonical basis (`DATA_BASED`, `MIXED`, or
  `INTENT_BASED`);
- activated Domain Experience versions and any Composite/Cross-Domain scope;
- CompositeSimulationGraph and CrossDomainSemanticGraph versions plus node/edge/path lineage;
- capability, metric/formula/dependency, model/artifact, engine/provider/inventory/resolver, license,
  and non-secret configuration versions;
- baseline/comparison basis, controls, constraints, assumptions, conversions, random seeds, and
  consent/evidence-access and policy snapshots;
- predictions, deterministic values, simulations, intervals/distributions, optimizer outputs where
  applicable, reconciliations, and requested comparisons;
- separate Trust decomposition and Evidence Profile, support/extrapolation, warnings, limitations,
  partial/blocked/refused paths, explanations, provenance, audit/trace, and result artifacts.

Cross-Domain output retains domain boundaries and reconciliation lineage. A combined view does not
hide entity/grain, time/calendar, unit/currency, accounting, evidence, or unsupported-path details.

## Required presentation boundary

Every report identifies the scenario basis and distinguishes observed values/outcomes, derived
values, predictions/forecasts, deterministic calculations, simulated output, optimization output,
assumptions, synthetic data, benchmarks/analogs, external evidence, and LLM proposals where present.

Trust and Evidence Profile are presented as separate sections/authorities. Green/Amber/Red and
dimension-level reasons remain visible; an Evidence Profile describes dependence and composition,
not another Trust score. Predictive associations are not labeled causal, extrapolation is not labeled
observed support, and intent-based output is not presented as empirical truth.

## PDF content

Representative sections are executive summary, scenario intent/basis, baseline and comparisons,
results/KPIs/charts, Composite/Cross-Domain path summary where applicable, uncertainty, assumptions
and constraints, drivers/explanations, Trust, Evidence Profile, warnings/refusals, methodology,
reconciliation, and dataset/semantic/metric/model/engine/graph/evidence lineage.

## Excel content

Representative worksheets are Summary, Scenario Intent, Inputs, Assumptions & Constraints, Results,
Scenario Comparison, Metric Details, Chart Data, Uncertainty/Monte Carlo, Composite Graph Lineage,
Cross-Domain Reconciliation, Trust, Evidence Profile, Historical Support, Model & Engine Information,
Warnings & Refusals, and Audit Metadata. Detailed samples are optional and included only when policy
permits.

Exact templates, worksheet names, field layouts, and rendering libraries are deferred.

## Permission, privacy, license, and audit enforcement

Exports re-evaluate export authorization and honor dataset, table, column, row, sensitivity,
purpose, retention, outbound, evidence-access, license, and consent policy. Access to a result does not
automatically grant access to every upstream raw value or external/synthetic artifact. Sensitive or
raw data is not included merely because a user may export summarized results.

Each artifact records result/version, format, generator/version, requester, authorization/policy
snapshot, included/redacted/omitted sections, checksum, creation/expiry, audit/trace, and safe failure
reasons. Secret values and raw stack traces are never exported.

## Reproducibility boundary

The export references the immutable result and original reproduction manifest. Generating a later
artifact from the same result is not a re-run. If a template or renderer version changes, the new
artifact records that version while preserving the result's original analytical lineage.

## Deferred implementation detail

F2-E adds only the contract needed to represent Evidence Profile, scenario basis,
Composite/Cross-Domain results, graph lineage, and Trust. Export APIs, jobs, templates, storage,
rendering dependencies, and UI controls require later accepted phases and milestones.
