# IPSP v1.0 — Intelligent Predictive Simulation Platform

**Product:** Intelligent Predictive Simulation Platform (IPSP)  
**Initial experience:** CampaignSim — Powered by IPSP  
**Specification status:** v1.0 architecture frozen
**Implementation status:** Phase 1B / v0.1.0 configuration and security-policy foundation
**Implementation releases:** v0.1.0 → v1.0.0

This repository contains the frozen specifications and the local-first IPSP application foundation.
The current implementation provides the FastAPI factory, safe error/trace scaffolding, typed nested
configuration and feature flags, environment-backed secret resolution, backend outbound policy,
job contracts, health probes, and an offline dark/light frontend shell. Network adapters,
analytical workflows, persistence, and authentication remain intentionally unimplemented until
their scheduled phases.

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

## Local development

Python 3.11 or newer is required. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m uvicorn ipsp.main:create_app --factory --reload
```

Open `http://127.0.0.1:8000`. The UI and API foundation require no Internet connection at runtime.

### Local job-worker deployment constraint

`LocalJobBackend` is a single-process execution provider. Do not run multiple active local worker
processes against the same SQLite control-plane database. Multi-process or distributed execution
requires a future provider with explicit worker ownership and leases; the current local backend does
not implement distributed locking, heartbeats, or coordination.

## Configuration and secrets

Copy `.env.example` to a local ignored `.env` when environment overrides are needed. Nested settings
use a double underscore, for example `IPSP_FEATURES__REMOTE_LLM_ENABLED` and
`IPSP_OUTBOUND__INTERNET_ENABLED`. Feature availability never overrides outbound denial; all feature
and outbound controls default off.

Secret values are injected separately into the process environment and resolved only through an
explicit `SecretRef`. They are not normal Settings fields, examples, or persisted configuration.
See `config/README.md` for the canonical environment shape and migration from Phase 1A names.

For a reproducible environment after `requirements.lock` is generated:

```powershell
python -m pip install -r requirements.lock
python -m pip install -e . --no-deps
```

## Quality gates

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy backend/ipsp
```

Infrastructure probes are intentionally unversioned at `/health/live` and `/health/ready`. Application APIs begin under `/api/v1`.
