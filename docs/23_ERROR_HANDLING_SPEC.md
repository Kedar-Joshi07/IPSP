# Error Handling Specification

## Goals and boundary

Provide safe user messages, detailed redacted internal diagnostics, stable error codes, traceable
failures, and actionable limitation/refusal reasons. Adding target taxonomy does not claim the related
F-002 service is implemented.

## Taxonomy families

- `AUTH-*` — authentication/session
- `AUTHZ-*` — role, resource, project/dataset, permission, or consent authorization
- `DATA-*` — ingestion, storage, dataset version, sampling, profile, or provenance
- `SEM-*` — semantic manifest, Domain Experience, clarification, or confirmation
- `REL-*` — relationships, entity/grain/cardinality, join safety, or Cross-Domain semantics
- `METRIC-*` — formula, aggregation, unit/currency/time, or registry validation
- `CAP-*` — capability discovery, unsupported/limited/refused path
- `ENGINE-*` — provider inventory/resolution, availability, resource, or execution
- `LICENSE-*` — dependency/model-weight/solver/evidence/provider license decision
- `ML-*` — training, model, artifact, evaluation, calibration, drift, or promotion
- `LLM-*` — local/remote provider, schema, validation, or numerical-authority boundary
- `EVIDENCE-*` — access mode, source, retrieval, provenance, freshness, or applicability
- `POLICY-*` — privacy, outbound, project/dataset policy, runtime consent, or retention
- `SIM-*` — Scenario Intent, assumptions, graph, simulation, reconciliation, or support
- `TRUST-*` — Trust/Evidence Profile validation and mandatory checks
- `LEARN-*` — observed-outcome matching, eligibility, training builder, challenger/promotion
- `EXP-*` — export/report
- `JOB-*` — job submission, lifecycle, cancellation, retry, or worker
- `BACKUP-*` — backup, retention, restore, or integrity
- `SYS-*` — configuration, readiness, storage/resource, or system failure

Exact codes are frozen with each owning API/capability rather than guessed in F2-G.

## Response contract

The user/API receives a stable `error_code`, safe `message`, `trace_id`, and optional authorized field
details, recoverability/clarification/remediation hints, retryability, and resource/job/run reference.
Responses distinguish invalid request, unauthorized/forbidden, unavailable, limited, blocked,
refused, conflict, not-ready, and internal failure without revealing hidden capability or resource
existence.

Internal diagnostics may include redacted exception type/stack, component/provider, versions, safe
context and reason chain, policy/license decision references, job attempt, and trace. No raw Python
traceback, SQL, filesystem secret, credential, inaccessible metadata, sensitive row/prompt/evidence,
or provider payload appears in production UI/API responses.

## Provider, policy, and fallback behavior

Unavailable or blocked engines, evidence sources, connectors, models/adapters, licenses, permissions,
or consent produce their governed safe reason. They never trigger an undeclared provider fallback,
mode expansion, evidence substitution, graph-edge invention, or policy weakening. An allowed fallback
has its own recorded resolver/policy decision and trace.

Partial Composite/Cross-Domain or learning results identify omitted/blocked paths and never imply the
downstream output ran. Background jobs persist sanitized terminal error and retry/cancellation state;
raw worker exceptions remain in access-controlled redacted diagnostics only.

## Validation and observability

Error envelopes are schema-validated and tested for redaction, stable codes, trace correlation,
authorization leakage, and safe unknown failures. Error reporting itself must not recursively expose
secrets or replace the originating failure. Meaningful failures and refusals emit the applicable
audit/observability event.
