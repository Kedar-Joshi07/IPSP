# Capability Discovery Specification

## Status and authority

This is a planned F-002 contract. Capability Discovery, engine resolution, and analytical runtime
are not implemented in v0.1.0 or v0.1.1. The governing architecture is the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md).

## Principle

The platform asks: **What can responsibly be calculated, analyzed, diagnosed, predicted,
forecast, simulated, optimized, explained, compared, or refused from this evidence?**

Capability validity is independent of which libraries happen to be installed. A target-like field,
provider registration, Domain Experience hint, benchmark expectation, or LLM proposal never enables
a capability by itself.

## Required decision separation

```text
What is semantically and data-valid?
  → What engine families can perform it?
  → Which installed and allowed provider is eligible?
```

1. **Semantic/data validity** uses exact Dataset Semantic Manifest, Metric & Formula Registry,
   relationship, grain, time, unit/currency, provenance, maturity, support, and policy evidence.
2. **Engine-family feasibility** identifies valid deterministic, statistical, ML, time-series,
   causal, Monte Carlo, synthetic-support, optimization, or other governed execution patterns.
3. **Provider eligibility** delegates to EngineRegistry, LicenseRegistry, and EngineResolver after
   capability and engine-family validity are established.

Capability Discovery never selects a vendor merely because it is installed. EngineResolver never
turns an unsupported semantic/data path into a valid capability.

## Candidate capability families

- Descriptive analytics and summaries.
- Diagnostic, driver, opportunity, and anomaly analysis.
- Regression.
- Binary and multiclass classification.
- Count prediction.
- Forecasting and temporal projection.
- Similarity and look-alike analysis.
- Propensity only with valid labels, horizon, and design.
- Clustering and segment profiling without same-period target leakage.
- Deterministic what-if and formula evaluation.
- Sensitivity analysis.
- Monte Carlo uncertainty where distributions/support are defensible.
- Synthetic-assisted workflows with explicit synthetic provenance.
- Risk and stress analysis.
- Optimization where an objective, controllable decisions, constraints, and solver support exist.
- Causal analysis where treatment, outcome, confounders, identification assumptions, and
  validation/refutation support exist.
- Composite/Cross-Domain analysis or simulation where CrossDomainSemanticGraph relationships
  reconcile.

These are candidate families, not guaranteed features for every dataset.

## Capability evidence contract

Each capability proposal conceptually records:

- capability ID/type, objective, outcome, entity/population, horizon, and requested outputs;
- exact dataset, Semantic Manifest, metric, relationship/graph, and Domain Experience versions;
- required semantic concepts, labels, controls, constraints, grain, time, units/currencies, and
  evidence maturity;
- data sufficiency, variation, coverage, support, leakage, and extrapolation evidence;
- candidate engine families and why each is or is not semantically valid;
- required provider features, resource bounds, explainability, uncertainty, and calibration;
- provider/license eligibility result references when resolution is reached;
- Trust validation, limitations, reason codes, and reproducibility references.

Exact persistence/API representation is deferred to later contract freezes.

## Validation gates

1. **Semantic gate** — concepts, roles, relationships, time, grain, units/currencies, and objective
   meaning are valid and sufficiently confirmed.
2. **Data gate** — required variation, labels, coverage, support, observation maturity, and safe join
   plan exist; leakage and prohibited sensitivity use are absent.
3. **Engine-family gate** — at least one execution pattern can validly perform the task and has a
   meaningful baseline or deterministic validation plan.
4. **Provider/license gate** — an installed/available provider satisfies capability, dependency,
   model-weight, solver/commercial, security, hardware, resource, and organization policy.
5. **Trust gate** — model/engine validation, calibration where applicable, constraints, support,
   extrapolation, privacy, provenance, licensing, and reproducibility pass at the required level.

A later gate cannot waive an earlier failure.

## Status and reason behavior

The conceptual lifecycle preserves `DISCOVERED → VALIDATING → VALIDATED → ENABLED` and terminal or
limited outcomes such as `LIMITED`, `DISABLED`, `BLOCKED`, or `REFUSED`, always with stable safe
reason codes and evidence references. Exact persisted enums are deferred.

Unavailable providers do not erase a semantically valid capability; they may leave it disabled with
a provider/resource/license reason. Conversely, an eligible provider does not hide semantic or data
invalidity.

## Responsible refusal

Unsupported return, profit, causal-effect, optimization, individual propensity, composite, or other
requests remain unavailable when required semantics, design, relationships, data, evidence,
providers, licenses, or Trust are missing. Refusal states what is absent, what can still be done, and
what evidence or confirmation could change the result without fabricating certainty.
