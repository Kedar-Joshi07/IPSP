# AGENTS.md — IPSP v1.0

This file is authoritative for coding agents working anywhere in this repository.

## Mission
Build the **Intelligent Predictive Simulation Platform (IPSP)** exactly as defined by the v1.0 specification set. The project must remain dataset/schema agnostic.

IPSP is the only top-level product identity. Historical prototypes and benchmark narratives may
inform tests or visual design, but they are not architecture authority, product shells, or generic
runtime behavior.

## Non-negotiable rules

- Never introduce a source-column name from a benchmark dataset into generic core logic unless the code is in a benchmark fixture/test.
- Never implement logic because a benchmark happens to contain a funnel, campaign, order, hotel, product, customer, inventory field, or finance field.
- Never treat LLM text as system truth without schema validation and deterministic/evidence checks.
- Never transmit raw dataset rows to a remote LLM by default.
- Never store plaintext passwords, API keys, auth cookies, or secrets.
- Never expose raw stack traces in production UI/API responses.
- Never claim causality from observational predictive associations.
- Never silently map `Unknown` to a negative target label.
- Never infer `0 == missing` or `missing == 0` without a confirmed semantic rule.
- Never assume monetary measures are non-negative; enforce only intrinsic or confirmed constraints.
- Never force every ordered journey into a strict monotonic funnel.
- Never use same-period derived persona/cluster features to predict outcomes from which those personas were derived.
- Never directly aggregate a one-side measure after a one-to-many join without grain/cardinality validation.
- Never let a Domain Experience Pack own generic numerical truth; metric definitions resolve through the versioned Metric & Formula Registry.
- Never select an engine/provider before capability validity, license, Trust, data suitability, security, and resource gates pass.
- Never invent a CrossDomainSemanticGraph or CompositeSimulationGraph edge to satisfy an intended outcome.
- Never collapse Trust into Evidence Profile, or treat either as model/LLM confidence.
- Never promote simulation, assumption, synthetic, benchmark, external, or LLM-proposed values directly to observed truth or empirical training data.

## Source of truth priority

1. `docs/44_F002_ARCHITECTURE_FREEZE.md` and
   `docs/45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md` for post-v0.1.0 architecture and
   product-development decisions.
2. Locked architectural decisions in `docs/00_SCOPE_FREEZE.md` and `docs/32_DECISION_LOG.md`, with
   accepted historical meanings preserved.
3. Explicit specifications under `docs/`.
4. Structured contracts/schemas under future `schemas/`.
5. Confirmed user/admin semantic metadata persisted by the application.
6. Deterministic evidence from data profiling.
7. LLM proposals.
8. Benchmark narrative/commentary.

F-002 extends and supersedes conflicting older target-architecture wording. It does not make its
planned capabilities implemented, does not rewrite the accepted v0.1.0 history, and does not
authorize v0.2 implementation. Follow the frozen v0.1.1 → v0.2.0 → … → v0.15.0 → v1.0.0 roadmap;
never revive the superseded v0.2–v0.9 prompt map or bundle simulation, Trust, history, and UI into
an older milestone merely because a historical prompt did so.

If documents conflict, stop and record the conflict in `docs/33_OPEN_QUESTIONS.md` rather than guessing.

## Coding behavior

- Prefer small cohesive modules, dependency injection, typed interfaces, and testable services.
- Use repositories for database access; do not scatter SQL through API endpoints.
- Keep API routers thin.
- Use Pydantic models for API/LLM contracts.
- Use deterministic validators around any generative output.
- Add tests with every behavior change.
- Update `docs/31_IMPLEMENTATION_PROGRESS.md` after every completed implementation phase.
- Add architecture-changing decisions to `docs/32_DECISION_LOG.md`.

## Parallel development behavior

IPSP uses **same-version, different-module parallel development**.

Before coding on a parallel branch:

1. read `docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md`;
2. read `docs/42_ACTIVE_WORKSTREAMS.md`;
3. read the assigned workstream contract;
4. verify branch name, exact base SHA, merge target, owner, migration owner, dependency owner, owned paths, shared paths, and forbidden paths;
5. verify the functional, data/schema, API/interface, acceptance, and dependency/license contracts;
6. verify branch, post-merge integration, and milestone acceptance gates.

Rules:

- work only inside the assigned workstream scope;
- do not modify a shared/integration-sensitive path unless explicitly authorized;
- do not create migrations unless the workstream is the current Migration Owner;
- do not modify `pyproject.toml` or `requirements.lock` without explicit Kedar authorization;
- do not independently redesign a frozen shared contract;
- if a shared contract must change, stop and report `CONTRACT CHANGE REQUIRED`;
- if a dependency, migration, shared-file, security-authority, or architecture change is required but not authorized, stop and report it;
- a contributor never merges to `integration/*` or `main`;
- Kedar is the integration owner and resolves conflicts, integration ordering, finalization, and milestone promotion;
- a branch PASS is not a milestone PASS; merged integration must be retested and independently reviewed.

## Required verification before declaring a phase/workstream complete

- Unit tests pass.
- Relevant integration tests pass.
- Security/permission checks pass.
- No benchmark-specific production constants were introduced.
- Logging/trace IDs are present for meaningful operations.
- Error messages are safe and actionable.
- Documentation required by the workstream is updated.
- The final report includes the exact branch, base SHA, current SHA, merge target, shared-file changes, migration state, dependency state, tests, and deviations.
