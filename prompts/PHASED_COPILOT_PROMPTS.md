# Phased GitHub Copilot Implementation Prompts

## How to use
Run one phase at a time. At the start of each phase tell Copilot to read `AGENTS.md`, `.github/copilot-instructions.md`, the referenced specifications, and the previous phase progress. Do not let it redesign locked architecture.

---

## Phase 0 — Repository audit / plan only

**Prompt**

> Read `AGENTS.md`, `.github/copilot-instructions.md`, `docs/00_SCOPE_FREEZE.md`, `docs/03_ARCHITECTURE.md`, `docs/04_PROJECT_STRUCTURE.md`, `docs/30_ACCEPTANCE_CRITERIA.md`, and every flow file. Do not write production code yet. Produce a concrete implementation plan for v0.1.0 including proposed modules/classes, dependencies, migrations, tests, and risks. Verify that no benchmark-specific fields or Streamlit assumptions enter the design. Update no locked decisions without asking.

Gate: plan aligns with docs; no architecture drift.

---

## Phase 1 — v0.1.0 Foundation, security, configuration, observability

Read: security/RBAC, configuration, observability, error, SQLite specs.

**Prompt**

> Implement the v0.1.0 repository skeleton and foundation: FastAPI app factory/bootstrap, typed configuration, SQLAlchemy setup/migration framework, users/roles/permissions, secure password hashing, server-side session foundation, CSRF design for browser writes, Admin/User RBAC, repositories, error envelope/taxonomy, trace/request IDs, audit/application/security logging, feature flags, SecretProvider and OutboundPolicy interfaces, health endpoint, and CLI admin bootstrap. Keep routers thin. Add unit/integration/security tests. Update `docs/31_IMPLEMENTATION_PROGRESS.md` only after tests pass.

Gate: auth/RBAC/logging/config DB skeleton passes tests.

---

## Phase 2 — v0.2.0 Ingestion, storage, versioning, provenance

**Prompt**

> Implement secure structured uploads, staging/quarantine, supported-format parsing, immutable originals, canonical Parquet output, project/dataset/dataset-version tables and services, sampling/provenance metadata, multi-sheet/table registration, and background job status. Do not analyze business semantics yet beyond structural metadata. Add file type/size/path traversal/archive tests and versioning tests.

Gate: uploads/versioning safe and reproducible.

---

## Phase 3 — v0.3.0 Deterministic data understanding and relationships

**Prompt**

> Implement deterministic profiling: dtypes, missingness/sentinels, cardinality, examples, distributions, dates, candidate identifiers/grain/entities/dimensions/measures/helper fields, key/FD candidates, relationships, hierarchy candidates, join cardinality/multiplication warnings, units candidates, feature lineage/derived-field candidates, sampling-aware evidence, and privacy/sensitivity candidates. Use Polars/PyArrow first. Build Dataset Intelligence Packet contracts. No LLM dependency. Add semantic benchmark tests using generic expected concepts only.

Gate: benchmark schemas are understood without special cases.

---

## Phase 4 — v0.4.0 Semantic manifest and clarification workflow

**Prompt**

> Implement semantic proposal models, evidence/confidence synthesis, semantic conflicts, clarification questions, user confirmations/corrections, versioned Dataset Semantic Manifest, KPI/metric dependency proposals and validation, relationship confirmation, prediction-horizon/feature-availability metadata, measurement-unit/entity-scope metadata, and manifest persistence. Build API contracts needed by the five-step dataset UI. Keep LLM provider as NullLLMProvider for now.

Gate: ambiguous semantics block dependent capabilities until confirmed.

---

## Phase 5 — v0.5.0 Capability discovery, modelling, registry

**Prompt**

> Implement capability discovery and gates, baseline model routing, regression/classification/count/forecast candidate families, similarity/look-alike path where valid, validation split strategy selection, target-label validation, leakage checks, model registry, metrics, candidate/challenger/champion statuses, and deterministic capability validations. Do not enable a predictive capability merely because a target exists. Add model tests and benchmark refusal cases.

Gate: valid capabilities enable; invalid/unsupported capabilities give reasoned refusal.

---

## Phase 6 — v0.6.0 Simulation, uncertainty, trust, history, exports

**Prompt**

> Implement scenario metadata/controls, predictive and deterministic what-if engines, benchmark scenarios, Monte Carlo where calibrated, SDV provider boundary, Run Result Object, Trust & Validation Engine, constraint classes, support/extrapolation checks, reproducible seeds, simulation history, compare/re-run/reproduce, PDF and Excel generators from persisted results, export permissions, and background jobs. Add end-to-end run tests.

Gate: no result bypasses trust; reproduce is deterministic for fixed versions/seeds.

---

## Phase 7 — v0.7.0 Dynamic frontend and design system

**Prompt**

> Refactor `reference/Campaign_simulator_UI.html` into modular production HTML/CSS/JS while preserving its visual language. Implement dark/light tokens, login, dashboard, project/workspace, five-step dataset onboarding, five-step simulation, dynamic controls, dynamic results, trust UI, history, Admin pages, errors, loading/jobs, and Plotly charts. Remove hardcoded marketing controls/values. Use secure session APIs, accessibility, and responsive behavior. Add frontend/API integration tests as practical.

Gate: entire app feels like one coherent evolution of the reference HTML and is metadata driven.

---

## Phase 8 — v0.8.0 Local LLM semantic provider

**Prompt**

> Implement LocalLLMProvider behind SemanticLLMProvider using an OpenAI-compatible local endpoint where possible. Require strict structured/Pydantic outputs. Implement semantic schema classification, relationship proposals, clarification generation, KPI proposal, capability explanation, and result narrative. Feed only Dataset Intelligence Packets/evidence tools, not bulk raw data. Validate every output. Add provider health/config Admin UI and tests with deterministic mocks.

Gate: app remains fully functional when local LLM is disabled/unavailable.

---

## Phase 9 — v0.9.0 Remote/hybrid LLM and privacy routing

**Prompt**

> Implement RemoteLLMProvider and HybridLLMProvider, privacy sanitizer, dataset/column transmission policy, outbound-policy enforcement, secret references, provider/token/cost/latency usage tracking, escalation rules, and Admin controls. Never send raw data by default. Add policy-denial, redaction, invalid JSON, timeout/fallback, and budget tests.

Gate: remote access cannot bypass policy, privacy, or structured validation.

---

## Phase 10 — v1.0.0 Integration hardening

**Prompt**

> Run the full acceptance suite. Validate all seven benchmark families for semantic diversity, not source-specific branches. Run scale tests using the large benchmark where available. Fix security, performance, UI, reliability, export, backup/restore, logging, and documentation gaps. Produce a release readiness report mapping every criterion in `docs/30_ACCEPTANCE_CRITERIA.md` to test evidence. Do not call the release v1.0.0 until all critical criteria pass.
