# Copilot Testing Prompts

## Authority and phasing
> Derive tests from the accepted workstream contract, implemented behavior, and `docs/29_TEST_STRATEGY.md`, under `docs/44_F002_ARCHITECTURE_FREEZE.md` and `docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md`. Check `docs/31_IMPLEMENTATION_PROGRESS.md` and `docs/42_ACTIVE_WORKSTREAMS.md` before proposing tests. Do not require runtime tests for a future capability whose implementation milestone has not begun; preserve its boundary with architecture/static checks or explicit unavailable/refusal tests only when applicable to the current implementation.

## New feature test prompt
> For the authorized feature, add tests covering happy path, boundary/invalid input, authorization and policy denial, safe errors, logging/trace/audit context, deterministic reproduction or seeded behavior, and relevant unsupported-capability/refusal and anti-contamination cases. Assert only behavior implemented by the current milestone.

## Benchmark prompt
> Use benchmarks only as fixtures for generic semantic outcomes such as grain, relationship, journey, measure family, privacy, and safe Cross-Domain reconciliation. Include renamed/perturbed or incompatible cases where appropriate. Never require benchmark-name branches, physical columns, fixed metrics/formulas/controls, or preferred providers in production.

## Regression prompt
> Run the applicable implemented regression set protecting ML-only/local-first operation, remote/outbound denial, auth/session/RBAC and secret redaction, semantic conflict blocking, unsafe joins, missing/sentinel distinctions, target leakage rejection, causal-language boundaries, and exact-version reproducibility. Preserve immutable data/semantic/model/run references and safe negative paths.

## F-002 contract prompt
> For F-002 capabilities already implemented by the current milestone, test Domain Experience neutrality; Metric & Formula Registry version/validation authority; capability-before-provider selection; engine/license eligibility and explicit fallback/refusal; ScenarioIntentManifest basis provenance; graph entity/grain/time/unit/currency/evidence safety; separate Trust and Evidence Profile; synthetic and other provenance classes; learning eligibility/outcome reconciliation; Local AI's lack of numerical authority; and exact evidence/consent/provider/license snapshots. For capabilities not yet implemented, do not fabricate fixtures, providers, schemas, or expected runtime behavior—test only the present contract boundary where relevant.

## Completion prompt
> Run unit, relevant integration, security/permission, architecture/anti-contamination, Ruff, strict mypy, compileall, dependency integrity, Markdown/documentation gates, and the workstream's exact branch gate. Record skips, environment-sensitive failures, retries, and unsupported paths honestly; a branch PASS does not establish post-merge or milestone acceptance.
