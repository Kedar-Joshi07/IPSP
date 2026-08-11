# Model Registry & Lifecycle

## Registry fields
Model ID, dataset/version, semantic manifest version, capability, algorithm/version, feature set, target, split strategy, metrics, artifact path, training timestamp, seed, status, parent/challenger relationship.

## Statuses
`TRAINING`, `CANDIDATE`, `CHALLENGER`, `CHAMPION`, `REJECTED`, `ARCHIVED`.

## Champion/challenger
Production uses the champion. New candidates compete on defined metrics, calibration, stability, latency, segment performance, and constraints.

## Shadow evaluation
A challenger may receive the same requests without serving results. Compare outcomes once actuals arrive.

## Learning policy
Models improve through controlled retraining and promotion. They do not silently rewrite themselves after every request.
