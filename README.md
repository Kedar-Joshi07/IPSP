# IPSP v1.0 — Copilot Foundation Pack

**Product:** Intelligent Predictive Simulation Platform (IPSP)  
**Initial experience:** CampaignSim — Powered by IPSP  
**Specification status:** v1.0 architecture freeze  
**Implementation releases:** v0.1.0 → v1.0.0

This repository pack is the implementation control plane for GitHub Copilot, Codex, and human developers. It converts the finalized design decisions into explicit architecture, flows, acceptance gates, and coding instructions.

## Core product statement

IPSP is a dataset-agnostic predictive simulation platform that accepts structured datasets plus business/column context, understands their semantics and relationships, asks targeted clarification questions when needed, discovers only supportable analytical/predictive/simulation capabilities, validates candidate models, dynamically builds scenario controls, executes simulations, quantifies uncertainty where valid, explains results, and records the complete lineage and audit trail.

## Architectural direction

```text
DATA → UNDERSTANDING → SEMANTIC CONTRACT → CAPABILITY DISCOVERY
     → MODEL VALIDATION → DYNAMIC UI → SIMULATION → TRUST GATE
     → RESULTS / PDF / EXCEL / HISTORY
```

The platform is **not** a marketing-specific simulator. Marketing is only one benchmark/application domain.

## Mandatory principles

1. **Dataset-agnostic core.** No benchmark dataset may hardcode fields, KPIs, funnels, model choices, or controls into production logic.
2. **ML/statistics are quantitative authority.** LLMs propose semantics, questions, explanations, and candidate interpretations; they do not invent numerical truth.
3. **LLMs are optional.** `ML_ONLY`, `LOCAL_LLM`, `REMOTE_LLM`, and `HYBRID_LLM` modes share one architecture.
4. **Predictive is not causal.** Attribution, correlation, forecast, and causal intervention must remain distinct.
5. **Trust is independent.** Neither ML nor an LLM grades its own output; the Trust & Validation Engine performs independent checks.
6. **Human review is exception-based.** Green continues automatically, Amber warns/reviews, Red blocks.
7. **Reproducibility is mandatory.** Every simulation records dataset version, semantic version, model version, seed, config, and trust result.
8. **Security/governance are foundation features.** RBAC, dataset permissions, outbound policy, secrets, audit logs, trace IDs, and safe uploads begin in v0.1.0.
9. **UI design is canonical.** `reference/Campaign_simulator_UI.html` is the visual baseline; the whole application must preserve its design language while adding a full light theme.
10. **Large analytical data lives outside SQLite.** SQLite is the control/knowledge plane; Parquet/source files are the analytical data plane.

## Start here

Read in this order:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/01_PROJECT_SPEC.md`
5. `docs/03_ARCHITECTURE.md`
6. `docs/07_DATA_UNDERSTANDING_SPEC.md`
7. `docs/08_SEMANTIC_MODEL_SPEC.md`
8. `docs/11_CAPABILITY_DISCOVERY_SPEC.md`
9. `docs/15_TRUST_AND_VALIDATION_SPEC.md`
10. `docs/30_ACCEPTANCE_CRITERIA.md`
11. `prompts/PHASED_COPILOT_PROMPTS.md`

## Implementation rule

Do not jump directly to predictive models. Build the platform in phase order and pass the phase acceptance gate before proceeding.
