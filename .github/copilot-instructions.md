# GitHub Copilot Instructions — IPSP v1.0

You are assisting with a production-oriented, dataset-agnostic predictive simulation platform.

## First principles

- Read `AGENTS.md` and the relevant scoped instruction file before generating code.
- For post-v0.1.0 architecture and product-development decisions, read and follow
  `docs/44_F002_ARCHITECTURE_FREEZE.md` and
  `docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md` before older target wording.
- Continue to follow `docs/00_SCOPE_FREEZE.md` and `docs/32_DECISION_LOG.md` for their compatible
  locked decisions and accepted history. Where older target wording conflicts, F-002 wins.
- F-002 is planned architecture until implemented and accepted by its owning milestone; it does not
  authorize v0.2 implementation or make a future capability operational.
- Do not redesign locked architecture during implementation unless explicitly asked.
- The backend package namespace is `ipsp`, never `campaign_*`, `marketing_*`, or benchmark-specific naming.
- IPSP is the only top-level product identity. Historical prototype assets are visual references
  only; reuse compatible interaction/design patterns without copying their branding, schema,
  terminology, calculations, or assumptions into generic behavior.

## Current and target stack boundary

- Preserve the accepted Python/FastAPI/Uvicorn/SQLAlchemy/SQLite and vendored HTML/CSS/JavaScript
  foundation unless the owning milestone authorizes change.
- SQLite is the control/governance/knowledge plane; source and Parquet files are the analytical
  plane. Do not turn SQLite into a mandatory analytical warehouse.
- Future data, model, synthetic, optimizer, explainability, and LLM libraries are provider
  candidates behind IPSP interfaces, not core architecture or permission to add dependencies.
- Synthetic capability is provider-neutral; no library is the generic synthetic engine.
- Do not modify `pyproject.toml` or `requirements.lock` without explicit Kedar authorization and an
  accepted dependency/license contract.

## Mandatory architecture layers

Adaptive frontend → API → authentication/RBAC/policy/consent → ingestion/storage → Data
Understanding → semantic/metric layer → Domain Experience activation → Cross-Domain composition →
Capability Discovery → scenario/evidence → Engine/License resolution → CompositeSimulationGraph →
Trust + separate Evidence Profile → results/compare/history/export → learning/reconciliation →
model/Local-AI improvement.

Cross-cutting: permissions, privacy, outbound policy, secrets, jobs, versioning, logging, trace IDs, feature flags, error taxonomy.

## Dataset handling

- Structured/tabular data only in v1.0: CSV/TSV, XLSX, Parquet, JSON/JSONL, ZIP containing supported files.
- Profile first. Determine grain, keys, entities, dimensions, measures, time, relationships, derived fields, units, sentinels, hierarchies, sampling provenance, and feature lineage.
- Basic multi-table support is required.
- Relationship inference is proposal-based: infer → validate → confirm when ambiguous → persist.

## LLM behavior

- LLMs never calculate authoritative metrics or predictions.
- Require structured JSON/Pydantic outputs.
- Validate every output.
- Prefer deterministic rules before LLM calls.
- Local LLM is the default semantic assistant when enabled.
- Remote LLM requires outbound policy approval and privacy sanitization.

## Capability behavior

A capability is enabled only after semantic validity, data support, model/engine validation, and trust checks. Correctly refusing unsupported simulation is a product feature.

- Domain Experience Packs contribute governed metadata and requests; they do not fork IPSP Core or
  own formulas.
- Numerical metric truth belongs to the Metric & Formula Registry.
- Capability validity is decided before provider selection. EngineRegistry, Runtime Engine
  Inventory, LicenseRegistry, and EngineResolver keep declared, installed, available, eligible, and
  selected states distinct.
- Scenario bases are exactly `DATA_BASED`, `MIXED`, and `INTENT_BASED`.
- ScenarioIntentManifest states intent; CrossDomainSemanticGraph states supported semantic
  relationships; CompositeSimulationGraph states validated execution.
- SimulationLearningStore is separate from empirical data. Outcome reconciliation and learning
  eligibility precede any training-dataset construction or challenger evaluation.

## Parallel workstream behavior

IPSP uses same-version, different-module parallel development.

Before changing code:

- read `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`;
- read `docs/42_ACTIVE_WORKSTREAMS.md`;
- obey the assigned workstream contract;
- verify exact base SHA, branch, merge target, owned paths, shared paths, forbidden paths, migration owner, and dependency owner;
- verify functional, data/schema, API/interface, acceptance, and dependency/license contracts;
- verify branch, post-merge integration, and milestone acceptance gates.

Do not broaden scope because another active branch is implementing adjacent functionality.

Do not:
- merge to `integration/*` or `main`;
- create migrations unless assigned migration ownership;
- modify `pyproject.toml` or `requirements.lock` unless explicitly authorized;
- reinterpret a frozen shared contract;
- resolve semantic conflicts between parallel branches by guessing;
- edit repository-wide progress/status/governance files unless assigned.

When blocked by coordination, return a structured stop reason such as:
- `CONTRACT CHANGE REQUIRED`
- `MIGRATION OWNERSHIP REQUIRED`
- `DEPENDENCY CHANGE REQUIRED`
- `SHARED FILE OWNERSHIP REQUIRED`
- `ARCHITECTURE CHANGE REQUIRED`
- `SECURITY AUTHORITY CHANGE REQUIRED`

Kedar is the integration owner and final merge authority.

## Testing

Every feature must include tests for normal behavior, unsafe/invalid behavior, and benchmark contamination risk when relevant.

A feature-branch PASS means only that the workstream is ready for Kedar review. It is not permission to merge and does not establish milestone acceptance.
