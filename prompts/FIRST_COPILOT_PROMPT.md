# Recommended First Copilot Prompt

Paste this into GitHub Copilot Chat after adding this pack to the new repository:

> We are starting IPSP, that is Intelligent Predictive Simulation Platform from the finalized v1.0 specification pack. First read `AGENTS.md`, `.github/copilot-instructions.md`, all scoped `.github/instructions/*.instructions.md`, `docs/00_SCOPE_FREEZE.md`, `docs/01_PROJECT_SPEC.md`, `docs/03_ARCHITECTURE.md`, `docs/04_PROJECT_STRUCTURE.md`, `docs/30_ACCEPTANCE_CRITERIA.md`, `docs/32_DECISION_LOG.md`, and `flows/README.md` plus all referenced flow files. Also inspect `reference/Campaign_simulator_UI.html` for design language only. Do not write production code yet. Produce the Phase 0 implementation plan from `prompts/PHASED_COPILOT_PROMPTS.md`. Explicitly identify any proposed decision that would violate dataset agnosticism, LLM authority boundaries, trust validation, RBAC/security, SQLite-control/Parquet-data separation, or the canonical UI contract.
