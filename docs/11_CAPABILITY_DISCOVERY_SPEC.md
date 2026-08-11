# Capability Discovery Specification

## Principle
The platform asks: **What can responsibly be calculated, diagnosed, predicted, simulated, explained, or refused from this data?**

## Candidate capability families
- Descriptive analytics
- Diagnostic/opportunity analysis
- Regression
- Binary/multiclass classification
- Count prediction
- Forecasting
- Similarity/look-alike
- Propensity (only with valid labels/design)
- Clustering/segment profiling
- Deterministic what-if
- Benchmark scenario
- Sensitivity analysis
- Monte Carlo uncertainty
- Synthetic-context simulation
- Journey/funnel simulation
- Risk/anomaly analysis

## Four gates
1. **Semantic gate** — concept is meaningful and temporal roles are valid.
2. **Data gate** — required fields, variation, labels, support, and grain exist.
3. **Model/engine gate** — out-of-sample/baseline or deterministic validation is acceptable.
4. **Trust gate** — constraints, drift/support, extrapolation, privacy, and lineage checks pass.

## Status lifecycle
`DISCOVERED → VALIDATING → VALIDATED → ENABLED` or `LIMITED/DISABLED/BLOCKED` with reason codes.

## Responsible refusal
Unsupported ROI, profit, causal lift, optimization, individual propensity, or other capabilities must be shown as unavailable when required data/design is missing.
