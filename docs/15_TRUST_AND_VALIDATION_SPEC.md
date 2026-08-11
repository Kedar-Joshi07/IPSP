# Trust & Validation Specification

## Governing principle
**AI proposes. Evidence validates. Rules constrain. Models compete. Humans arbitrate exceptions. The system remembers the outcome.**

## Independent trust dimensions
- Data quality
- Semantic confidence
- Model/engine validation
- Historical/sample support
- Drift/extrapolation
- Constraint compliance
- Privacy/governance

## Constraint classes
1. **Intrinsic constraint** — mathematically inherent, e.g. probability in [0,1].
2. **Confirmed semantic constraint** — derived from confirmed meaning.
3. **Business constraint** — explicitly defined process rule.
4. **Empirical expectation** — historical pattern; warning only unless promoted by confirmation.

Never turn `revenue >= 0` into a universal rule.

## Outcome levels
- Green: all required checks pass.
- Amber: limited evidence, novelty, extrapolation, low cohort support, or review-worthy issue.
- Red: critical ambiguity, violation, leakage, permission/policy failure, invalid model, unsupported capability.

## ML validation
Regression: MAE/RMSE/WAPE/R² where appropriate; classification: precision/recall/F1/ROC-AUC/PR-AUC/calibration; forecasting: backtest/MAE/WAPE/coverage; interval coverage for uncertainty outputs.

## LLM validation
Strict schema, deterministic evidence consistency, conflict detection, optional local/remote agreement, and user confirmation for unresolved semantics.

## Simulation validation
Check interval ordering, support, constraints, impossible combinations, leakage, and calibrated uncertainty before display.

## Data/business anomaly separation
A negative value is invalid only when it is intrinsically impossible or violates a confirmed semantic/business rule. It is an anomaly or warning only when statistical evidence supports that classification. Otherwise it is a valid observation; negativity alone does not make it an error, exception, or anomaly.
