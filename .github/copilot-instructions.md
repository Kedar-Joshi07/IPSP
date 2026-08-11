# GitHub Copilot Instructions — IPSP v1.0

You are assisting with a production-oriented, dataset-agnostic predictive simulation platform.

## First principles

- Read `AGENTS.md` and the relevant scoped instruction file before generating code.
- Follow `docs/00_SCOPE_FREEZE.md`. Do not redesign locked architecture during implementation unless explicitly asked.
- The backend package namespace is `ipsp`, never `campaign_*`, `marketing_*`, or benchmark-specific naming.
- The frontend may use **CampaignSim — Powered by IPSP** as branding, but all behavior must be metadata driven.
- The supplied `reference/Campaign_simulator_UI.html` is the canonical visual reference. Reuse its design language, not its hardcoded campaign assumptions.

## Core stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy
- SQLite for control/knowledge metadata
- Parquet/source files for analytical data
- Polars + PyArrow; Pandas where a library requires it
- scikit-learn, LightGBM, CatBoost, Statsmodels
- SDV only where capability validation allows it
- SHAP where supported
- HTML/CSS/vanilla JavaScript + Plotly.js

## Mandatory architecture layers

Authentication/RBAC → API → application services → ingestion/profiling/semantics → capability discovery → modelling/simulation → trust validation → reporting/history.

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

## Testing

Every feature must include tests for normal behavior, unsafe/invalid behavior, and benchmark contamination risk when relevant.
