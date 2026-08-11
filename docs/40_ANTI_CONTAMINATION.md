# Benchmark / Legacy Anti-Contamination Rules

## Superseded artifacts
Previous RdF/Streamlit simulator specification/prompt packs are **not implementation authority** for IPSP v1.0.

Reusable lessons: progress tracking, acceptance gates, non-causal guardrails, validation, SDV boundary, reproducibility.

Discarded as core assumptions: fixed source columns, fixed funnel stages, fixed targets/KPIs, fixed model families, hardcoded marketing controls, Streamlit architecture.

## Production-code rule
Benchmark-specific names may appear only in:
- benchmark fixture data
- benchmark expected semantic manifests
- benchmark tests/documentation
- optional future domain plugins

They must not appear in generic services, database schema, API field names, model routing, or UI control definitions.

## UI reference rule
The supplied HTML contributes **visual design and interaction patterns only**. Its ROAS/CPA/channel/budget/FAISS/XGBoost/static chart values are demo content and are not copied into generic production behavior.
