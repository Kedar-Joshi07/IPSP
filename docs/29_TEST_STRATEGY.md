# Test Strategy

## Status boundary

This strategy covers future milestones under the [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md). It does not claim those tests or capabilities exist in the accepted v0.1.0 runtime. Each milestone freezes its own detailed acceptance contract before implementation.

## Test layers

### Unit

Profilers, semantic and relationship rules, Metric & Formula Registry validation, graph validation, Trust checks, Evidence Profile construction, provider/resolver policies, learning eligibility, outcome matching, permissions, and safe failures.

### Integration

Exercise the applicable lifecycle from upload and profiling through manifests, domain activation, metric resolution, capability discovery, engine/license resolution, scenario execution, Trust/Evidence, history, outcome reconciliation, governed learning, and export. Integration tests retain exact contract, evidence, consent, provider, license, seed, and configuration snapshots needed for reproduction.

### Security and governance

Cover authentication, CSRF/session behavior, authorization, dataset/column policy, consent, outbound denial, fail-closed secrets, upload/path traversal, redaction, dependency and model-weight license blocks, and provider fallback rules. A fallback must remain capability-equivalent, licensed, safe, explicit, and reproducible; otherwise the path refuses.

### Semantic, metric, and domain neutrality

- Verify generic core has no benchmark source columns, domain-specific dispatch, fixed metrics, formulas, controls, or provider winners.
- Validate Metric & Formula Registry identity/versioning, safe expressions, dependency cycles, precedence/conflicts, null/safe-division behavior, grain/cardinality, accounting identities, units, currencies, calendars, fiscal periods, and time alignment.
- Activate Domain Experiences only from versioned semantic evidence; absence, ambiguity, and conflicting packs must limit, clarify, or refuse.
- Exercise multiple domain families and Composite/Cross-Domain graphs without converting benchmark knowledge into production truth.

### Capability, engine, and model

Test semantic/data validity independently from provider selection. Cover EngineRegistry inventory distinctions, LicenseRegistry decisions, deterministic resolver priority, resource/security gates, explicit provider fallback or refusal, meaningful baselines, leakage-safe splits, calibration, challenger/champion decisions, rollback lineage, and unsupported-capability reasons.

### Simulation, Trust, and evidence

- Test exactly `DATA_BASED`, `MIXED`, and `INTENT_BASED`, including immutable basis and assumption provenance.
- Validate CompositeSimulationGraph nodes, edge meanings, acyclicity, ordering, constraints, cross-domain entity/grain/cardinality/time/calendar/unit/currency reconciliation, and safe partial/refused paths.
- Retain `SYNTHETIC_DATA` provider/version/seed/configuration/quality/privacy provenance and prove it never silently becomes observed truth.
- Test Trust independently from the Evidence Profile: neither score may replace the other, and Evidence Profile coverage, freshness, assumptions, synthetic, analog, external, and extrapolation dependence remain visible.

### Learning, outcomes, and Local AI

Test SimulationLearningStore separation from empirical analytical data, actual-outcome semantic/grain/time/unit/maturity matching, LearningEligibilityGate decisions, governed Training Dataset Builder leakage/provenance controls, and batch-default champion/challenger promotion. Intent-based, mixed-assumption, synthetic, LLM-proposed, and unverified external values never directly become observed labels or training rows.

Local AI tests preserve the order retrieval/memory → curated events → optional adaptation challenger → evaluation → promotion/rejection. Structured output, privacy/consent, provenance, reproducibility, dependency/model-weight licenses, and the rule that LLMs never gain numerical authority are mandatory.

### Reproducibility

Reproduce tests freeze dataset/table, semantic, Domain Experience, metric/dependency, graph, model/artifact, engine/inventory/license, evidence cutoff, consent/policy, seeds, code, and non-secret configuration snapshots. Re-run with newer eligible components must be visibly distinct from reproduce; unavailable historical components are reported, never silently substituted.

### Acceptance/E2E

Cover admin bootstrap, dataset onboarding, clarification, supported and refused capabilities, scenario definition/configuration/enrichment/run/results-and-compare, Trust and Evidence presentation, history, re-run/reproduce, outcome reconciliation where mature actuals exist, and authorized PDF/Excel export.

### Architecture conformance

Verify dataset/domain neutrality, provider-neutral interfaces, one ORM definition per entity, separate Pydantic contracts, synchronous SQLAlchemy 2.x repository patterns, one migration history, thin routes, vendored browser assets, both themes, immutable references, safe jobs/errors, and distinct liveness/readiness/Admin-health behavior.

## Benchmark principle

Benchmarks prove generic discovery and safe composition. Large datasets may support scale testing; documented samples support schema/semantic tests but do not prove full-population modelling sufficiency. Benchmark expectations belong in fixtures and acceptance evidence, never generic production branches.

## Phasing rule

These are future test obligations, not a direction to add all tests during F2-H. Every capability milestone selects the relevant subset in its frozen acceptance contract and adds tests with its behavior changes.
