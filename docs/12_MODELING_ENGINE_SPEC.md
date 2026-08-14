# Modelling Engine Specification

## Status and boundary

This is a planned, provider-neutral modelling contract under F-002. It does not implement model
training or install candidate libraries in v0.1.1. Capability Discovery establishes semantic/data
validity first; EngineResolver establishes provider/license eligibility before training begins.

There is no universal best model.

## Baseline-first competition

Every candidate set includes a meaningful baseline appropriate to the outcome and validation design.
A complex model that does not improve materially and robustly over the baseline does not justify
enabling or promoting the predictive capability.

Representative baselines include:

- mean, median, robust location, or simple rule for numeric outcomes where meaningful;
- class frequency, majority, or logistic baseline for classification;
- naive, seasonal-naive, drift, or simple rolling/statistical baseline for temporal outcomes;
- simple distance/similarity baseline for look-alike evaluation;
- deterministic formula/business-rule result when that is the actual requested authority.

Baselines are selected from semantics and design, not from one benchmark.

## Candidate families

Candidate families may include, when justified:

- linear, logistic, regularized, generalized-linear, count, duration, or distribution-aware models;
- trees, Random Forest, ExtraTrees, and gradient-boosted tree families;
- naive/seasonal-naive, rolling, ETS/state-space, ARIMA/SARIMAX, lag-feature ML, or multivariate
  temporal methods where assumptions and data support them;
- Bayesian or probabilistic methods where uncertainty requirements justify them;
- clustering, representation, nearest-neighbor, and similarity methods;
- volatility methods only when volatility semantics and data support them;
- causal estimators only after the independent causal activation contract passes.

Library names documented elsewhere are provider candidates behind registry interfaces. They are not
mandatory dependencies or universal winners.

## Candidate routing inputs

Routing depends on:

- exact outcome semantics and whether the output is a value, score, probability, ranking, count,
  duration, forecast, interval, or causal estimate;
- dataset/entity grain, sample size, variation, balance, censoring, and observation maturity;
- horizon, event/availability time, temporal structure, seasonality, hierarchy, and grouping;
- feature lineage, sensitive-feature policy, missingness, units, and support;
- explainability, uncertainty, calibration, latency, compute, memory, and artifact constraints;
- provider availability, dependency/model-weight license, security status, and organization policy;
- comparative validation and Trust requirements.

An LLM may explain or propose candidates but never selects a winner.

## Validation design

Validation matches the prediction/use design:

- chronological holdout, rolling-origin evaluation, or backtesting for temporal problems;
- entity/group/geographic holdout where leakage across related observations is possible;
- nested or standard cross-validation/holdout where appropriate;
- out-of-time and segment evaluation where stability/generalization matter;
- uncertainty and interval coverage where such outputs are surfaced;
- meaningful baseline comparison with predefined acceptance criteria.

Temporal problems never use inappropriate random splits merely for a better score.

## Leakage and contamination protection

Exclude or constrain:

- target, future, or post-outcome fields unavailable at the prediction horizon;
- same-period personas, clusters, aggregates, or features derived from the outcome being predicted;
- transformations fitted using future/test data;
- identifiers and high-cardinality fields that enable memorization without defensible semantics;
- duplicated derived concepts and unsafe multi-table aggregations;
- benchmark-specific feature sets or domain assumptions embedded in generic routing.

Training data references exact feature lineage and availability-time evidence.

## Calibration, explainability, and uncertainty

When a probability is surfaced, calibration is evaluated with an appropriate held-out design and the
output is labeled as probability only when supported. Scores and rankings are not silently presented
as calibrated probabilities.

Explainability requirements depend on user impact, model family, policy, and capability. Global and
local explanations retain model/data/version context and never convert association into causation.

Intervals and quantiles are displayed only when their construction and empirical coverage are
validated and limitations are explicit.

## Provider, license, resource, and Trust gates

Before training:

1. EngineRegistry confirms a candidate provider implements the required engine-family capabilities;
2. Runtime Engine Inventory confirms installed/available version and required hardware/resources;
3. LicenseRegistry returns an eligible dependency, model-weight, and commercial-use decision;
4. security and data-transmission policy permit the provider;
5. EngineResolver records deterministic selection reasons;
6. Trust validates the design and, after training, the resulting model evidence.

Model quality cannot waive license, security, resource, or semantic invalidity.

## Output-semantics separation

- **Score:** arbitrary or model-specific scale unless separately calibrated.
- **Probability:** calibrated estimate with declared event, horizon, and validation evidence.
- **Ranking:** ordering objective; not automatically a probability or expected effect.
- **Business rule:** deterministic declared logic; not a learned association.
- **Predictive association:** out-of-sample relationship useful for prediction, not causal impact.
- **Causal estimate:** effect estimate requiring causal identification and refutation evidence.

```text
correlation != prediction != attribution != causal effect
```

## Causal boundary

Causal activation requires a defensible treatment, outcome, confounder set, identification
assumptions, overlap/support, temporal ordering, sensitivity/refutation tests, and validation.
DoWhy and EconML are architecture candidates, not v0.1.1 dependencies or automatic authorities.

Observational predictive performance alone never licenses causal wording.

## Optimization boundary

Optimization is not prediction. It requires an explicit objective, decision variables, constraints,
feasibility checks, uncertainty handling, solver eligibility, and validation of downstream effects.

The planned boundary uses a CVXPY abstraction with OSQP and SCS as preferred open-source provider
candidates where valid. Commercial solvers remain optional and license-gated. No optimization
runtime is implemented by this specification.
