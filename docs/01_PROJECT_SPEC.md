# Project Specification

## Status and authority

This document defines the target IPSP product under the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and the
[Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md).
It distinguishes frozen target behavior from the accepted v0.1.0 foundation. A requirement in this
document is not evidence that its runtime capability is implemented.

## Product goal

Create a local-first, extensible, domain-adaptive web platform that accepts arbitrary structured or
tabular business data, determines what the data means, discovers which analyses, predictions,
forecasts, simulations, or optimizations are defensible, and explains when a requested capability
must be limited or refused.

The generic core remains dataset- and domain-agnostic. IPSP does not require a fixed schema and does
not specialize its core around Marketing, Finance, Product, Sales, Customer Experience, Operations,
or any benchmark narrative.

## Current implementation and target state

| State | Meaning |
|---|---|
| v0.1.0 | Formally accepted security, repository, API, jobs, observability, health, and offline-frontend foundation |
| v0.1.1 | F-002 documentation, contract, governance, and minimal compatibility reconciliation; in progress and not accepted |
| v0.2.0 and later | Capability milestones that remain not started |
| v1.0.0 | First complete, production-usable IPSP release; target, not a current implementation |

No ingestion, semantic inference, Domain Experience execution, modelling, simulation,
Cross-Domain execution, governed-learning runtime, or LLM runtime is implemented merely because
its architecture is specified here.

## Primary users

### Admin

Configures users, projects, dataset access, semantics, permissions, provider and license policies,
evidence and outbound policy, models, feature flags, logs, backup/retention, and system settings.

### User

Works only with permitted projects and datasets, uses capabilities that pass evidence and policy
gates, reviews Trust and Evidence Profiles, compares permitted results, and exports permitted
artifacts.

## Canonical product lifecycle

```text
Data
  → Understanding
  → Semantic Contract
  → Domain / Cross-Domain Activation
  → Capability Discovery
  → Analysis / Diagnosis
  → Model + Engine Selection
  → Simulation / Optimization
  → Trust + Evidence
  → Results / Comparison
  → Scenario & Experience Memory
  → Governed Learning
  → Better Future Models / Local AI
```

Not every dataset traverses every stage. An unsupported path is limited, disabled, blocked, or
refused with an actionable reason.

## Domain-adaptive composition

IPSP Core composes with registered Domain Experience Packs. A pack can contribute terminology,
semantic concepts, metric requests, objectives, controls, constraints, UI metadata, explanations,
comparison views, and prerequisites. It cannot define generic numerical truth, require physical
source-column names, select a universal model winner, or bypass evidence, Trust, or license policy.

First-class target families are Marketing, Product, Sales, Customer Experience, Finance,
Operations/Demand, Generic/Custom, and Composite/Cross-Domain. Finance is dynamically activated and
does not impose a mandatory accounting schema. Composite/Cross-Domain capability requires
validated entity, grain, time, unit, currency, transformation, and evidence relationships; IPSP
never invents joins to satisfy a requested scenario.

## Provider-neutral execution

Capability validity and provider selection are separate decisions. Target services resolve
eligible implementations through EngineRegistry, LicenseRegistry, and EngineResolver boundaries.
Vendor names are candidates or adapters, not core architecture and not evidence that a dependency
is installed.

## Trust, evidence, and learning

Trust evaluates whether data, semantics, relationships, models, support, constraints, privacy,
licensing, and reproducibility permit use. The separate Evidence Profile describes dependence on
observations, actual outcomes, assumptions, synthetic data, analogs, external evidence,
extrapolation, freshness, and coverage.

SimulationLearningStore and OutcomeReconciliation preserve scenario experience and later actual
outcomes without treating every run as empirical truth. Learning candidates require provenance,
leakage, eligibility, challenger, validation, Trust, and promotion gates. One simulation never
directly retrains a model.

## Core success condition

A previously unseen structured dataset can be onboarded with contextual descriptions; IPSP
profiles it, produces an evidence-backed semantic interpretation, asks targeted clarification
questions, persists a versioned semantic manifest, activates relevant Domain Experiences,
discovers responsible capabilities, validates models and eligible engines, and dynamically renders
controls and results appropriate to the evidence.

## Product quality goals

- Trustworthy refusal is preferable to fabricated capability.
- Results are reproducible, traceable, and explicit about evidence dependence.
- Users can understand why a capability is available, limited, blocked, or refused.
- ML-only operation remains fully functional when no LLM is enabled.
- Domain Experiences extend one generic backend rather than create hardcoded product forks.
- Prediction, attribution, causation, simulation, and optimization remain distinct.

## Bounded v1.0 definition

v1.0 is the first complete, production-usable expression of IPSP, not every future capability.
Advanced production causal workflows, full solver-backed optimization, automatic LLM fine-tuning,
Remote/Hybrid LLM execution, public-web evidence, enterprise connectors, distributed enterprise
scale, and specialized Quant Finance may mature after v1.0 when their architecture boundaries are
preserved.
