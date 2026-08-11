# Product Requirements

## Functional requirements

### Authentication & governance
- Local username/password authentication.
- Roles: Admin, User.
- Granular permissions under the roles.
- Dataset-specific `view`, `simulate`, `export_results`, `export_data` permissions.
- User activation/deactivation, password change, failed-login lockout, session expiry.

### Project and dataset lifecycle
- Project/workspace parent object.
- Dataset upload, staging, validation, versioning, archive/delete with dependency checks.
- Dataset provenance: full dataset vs random/stratified/time-window/filtered/aggregated sample.
- Optional original row count and original time coverage.

### Understanding
- Column profile, missingness, cardinality, distributions, examples.
- Candidate identifiers/entities/grain.
- Dimensions/measures/targets/controls/time/helper fields.
- Units and currencies where inferable.
- Hierarchies, functional dependencies, relationship cardinalities.
- Multi-table relationship proposals, normalized/temporal relationship support.
- Feature lineage, derived/binned/aggregate fields, semantic redundancy.
- Sentinel values and semantic missingness.
- Sensitive/quasi-identifier classification.
- Clarification questions and persisted confirmations.

### Capabilities and modelling
- Discover descriptive, diagnostic, predictive, similarity, forecasting, deterministic what-if, Monte Carlo, and synthetic-context capabilities.
- Model candidate families chosen by target semantics and data evidence.
- Baselines required.
- Chronological/group/entity validation strategies when appropriate.
- Model registry and version lineage.

### Simulation
- Dynamic controls generated from validated capability metadata.
- Distinguish learned predictive controls from user-defined assumptions.
- Scenario support checks and extrapolation warnings.
- P10/P50/P90 or other uncertainty outputs only when justified.

### Results
- Dynamic KPI cards/tabs/charts.
- Trust score decomposition.
- Warnings and model/data support.
- PDF and Excel exports.
- Run history, compare, re-run, reproduce.

### Administration
- AI provider configuration.
- Internet/outbound policy.
- Secrets references.
- Model lifecycle controls.
- Logs and system health.
- Backup/retention configuration.
