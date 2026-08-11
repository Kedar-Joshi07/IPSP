# Simulation Engine Specification

## Simulation types

### Predictive scenario
Change validated controllable/context variables and score with a validated model. Label as predictive association, not causal effect.

### Deterministic what-if
Use confirmed KPI identities/business formulas. No ML required.

### Benchmark scenario
Estimate a scenario if a weak segment reaches a selected/approved benchmark. Clearly label as scenario assumption.

### Monte Carlo
Propagate uncertainty through validated distributions/model residuals; output intervals only when calibrated/meaningful.

### Synthetic context (SDV)
Generate plausible contextual populations. SDV never decides the outcome; validated response models/logic score outcomes.

## Control eligibility
A field can be a scenario control only if the semantic manifest identifies it as controllable or explicitly allows assumption mode. Do not expose IDs, outcomes, post-outcome variables, or unsafe sensitive features as ordinary controls.

## Support checks
- Historical range/support
- Combination support
- Extrapolation distance
- Observation maturity
- Missing required context
- Business/semantic constraints

## Reproducibility
Persist random seeds and exact engine/model/config versions.
