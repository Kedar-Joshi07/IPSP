# Simulation History & Reproducibility

## Run identity
Use stable run IDs such as `SIM-YYYYMMDD-NNNNNN` or UUID-backed equivalent with friendly display ID.

## User actions
Open, compare, re-run, reproduce, export PDF, export Excel.

## Definitions
- **Re-run:** same scenario intent using current eligible/champion model.
- **Reproduce:** exact dataset version + semantic version + model version + seed + configuration.

## Persist
Input controls, assumptions, baseline, capability version, model artifact/version, random seeds, provider mode, trust output, warnings, result artifact refs, timestamps and user.

References resolve to immutable dataset-version, semantic-manifest-version, capability-version, and model-version records rather than mutable labels. Persist the effective non-secret numerical/runtime configuration snapshot or a stable hash sufficient to retrieve it.
