# Modelling Engine Specification

## Candidate routing

### Numeric targets
Linear/Ridge baseline, tree/gradient models, LightGBM/CatBoost; count/Tweedie/Gamma/Poisson families when supported by target semantics.

### Binary/multiclass
Logistic baseline plus tree/boosting candidates.

### Forecasting
Naive/seasonal baseline, lag-based ML, SARIMAX/other appropriate statistical candidates.

### Similarity/look-alike
Scaled/encoded representation and nearest-neighbor/similarity approaches, with careful sensitive-feature governance.

## Model selection
The winning model is selected from validation evidence, never LLM preference.

## Validation strategy
Choose chronological, entity/group, geographic/group, standard holdout/cross-validation, or backtesting based on grain and leakage risk.

## Leakage protection
Check target/post-outcome features, same-period personas/clusters, aggregate features built from future/test data, IDs/high-cardinality memorization, and duplicated derived concepts.

## Baseline rule
A complex model that fails to improve meaningfully over a simple/naive baseline does not justify enabling the predictive capability.
