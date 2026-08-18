# Copilot Code Review Prompts

## Authority and gate
> Review first against `docs/44_F002_ARCHITECTURE_FREEZE.md` and `docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md`, then compatible predecessor decisions in `docs/00_SCOPE_FREEZE.md` and `docs/32_DECISION_LOG.md`. Verify the exact accepted base, authorized workstream, owned/shared/forbidden paths, and current gate in `docs/31_IMPLEMENTATION_PROGRESS.md` and `docs/42_ACTIVE_WORKSTREAMS.md`. Flag future-milestone implementation or claims.

## Architecture drift
> Identify benchmark/source-column assumptions, hardcoded domains/metrics/formulas/controls/providers, layer violations, or business logic in routes/UI. Verify IPSP Core remains domain neutral; registered Domain Experience Packs contribute governed metadata and metric requests without becoming core branches or numerical authority.

## Data/semantic safety
> Review grain/cardinality, unsafe joins, denominators, target leakage, future/post-outcome features, missing/zero and sentinel handling, sampling claims, entity/time/calendar/unit/currency compatibility, and causal language. Numerical metric truth must resolve through exact versioned Metric & Formula Registry definitions and lineage.

## Capability, engine, and license
> Verify semantic/data capability validity is decided before engine family or provider selection. Review EngineRegistry, factual runtime inventory, LicenseRegistry, EngineResolver priority, dependency/model-weight/solver license decisions, resources/security, and explicit compatible fallback or reasoned refusal. Installation alone must not enable a capability.

## Scenario and graph safety
> Where implemented and in scope, verify ScenarioIntentManifest records exactly one of `DATA_BASED`, `MIXED`, or `INTENT_BASED`; CrossDomainSemanticGraph owns supported semantic relationships; and CompositeSimulationGraph uses validated typed nodes/edges without invented joins, effects, conversions, formulas, or evidence. Hard constraints must be intrinsic or explicitly confirmed. Unsupported paths must limit, block, or refuse safely.

## Security
> Review auth/session/permission/secret/log/upload/export behavior. Find any way a user could access an unauthorized dataset/column/run, bypass outbound policy, expose a secret, or receive a raw traceback.

## Trust, evidence, provenance, and learning
> Verify Trust and Evidence Profile remain separate authorities; neither is replaced by model/LLM confidence. Preserve exact evidence/provenance classes, consent/policy snapshots, reproducibility references, and `SYNTHETIC_DATA` separation. SimulationLearningStore must remain separate from empirical analytical data; observed-outcome matching, learning eligibility, governed dataset construction, challenger evaluation, and authorized promotion must precede learning. Simulations, assumptions, synthetic data, benchmarks, external evidence, and LLM proposals never silently become observed truth.

## Review outcome
> Require safe actionable errors, trace/audit evidence, negative-path tests, and responsible refusal. Report contract, migration, dependency/license, shared-file, security-authority, or architecture changes instead of silently broadening the reviewed scope.
