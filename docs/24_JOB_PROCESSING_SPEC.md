# Background Job Processing Specification

## Status and current boundary

The v0.1.0 foundation defines `JobBackend`, `LocalJobBackend`, `JobService`, `JobRepository`,
`JobStatus`, and `JobType`, with progress, cancellation, retry, sanitized errors, and durable SQLite
job metadata. `LocalJobBackend` is single-process and in-process; it is not a distributed worker,
cross-process queue, or multi-node executor.

F2-G does not implement future workers, providers, job types, Redis, Celery, or migrations.

## Provider-neutral job purposes

Long-running target work may include ingestion/canonicalization, profiling/data understanding,
semantic/relationship/metric validation, model training/evaluation, synthetic fitting/support,
simulation/Monte Carlo/optimization, Composite/Cross-Domain execution, evidence retrieval,
report/export, observed-outcome reconciliation, learning/training-dataset construction, Local AI
evaluation/adaptation, backup/restore, and maintenance.

These are generic capability purposes, not guaranteed current `JobType` members or domain-specific
jobs. Generic core must not replace durable vocabulary with Marketing-, Finance-, benchmark-, or
physical-column-specific types. `SYNTHETIC_FITTING` may remain a generic type; it represents the
provider-neutral synthetic capability and does not select SDV or another provider.

## Backend abstraction

Application services submit typed work through `JobBackend`; they do not depend directly on a queue
vendor. Future backends may support separate processes or distributed execution only after their
dependency, license, serialization, security, concurrency, recovery, and integration contracts pass.
LocalJobBackend remains acceptable for the bounded local-first implementation where workload and
durability requirements fit its single-process constraint.

## Canonical states

- `QUEUED`
- `RUNNING`
- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

Additional persisted states require an owning contract/migration. Capability-specific phases and
safe reason codes belong in metadata, not invented global states.

## Submission and execution snapshot

A job conceptually retains stable job/attempt identity, owner, purpose/type, priority, trace/parent
context, target resource/version, submitted/start/heartbeat/completion times, progress phase/message,
resource limits, cancellation/retry policy, artifact/result references, and sanitized error.

Future provider work also references exact capability, semantic/metric/graph/model, engine/provider/
inventory/resolver/license, evidence/policy/consent, Trust, non-secret configuration, and seed versions
applicable to the job. Secrets remain references resolved only at authorized execution time.

## Authority revalidation

Submission authorization does not permanently authorize execution. The worker revalidates current
role/resource access, project/dataset policy, runtime-consent validity where applicable, evidence mode,
learning eligibility, provider/license/security/resource gates, and cancellation before sensitive
work or material outbound access. Expired/withdrawn authority fails safely and is audited.

## Progress, cancellation, retry, and failure

Progress is monotonic within an attempt and reports percent only when meaningful, plus stable phase,
safe message, timestamp, and trace. Cancellation is cooperative and allowed only at safe boundaries;
partial artifacts are quarantined/marked incomplete and never presented as successful results.

Retries require idempotency or explicit duplicate protection, bounded attempt/backoff policy, and a
fresh eligibility/authority snapshot. Provider fallback is not an implicit retry. Terminal failures
store safe codes/messages/retryability while redacted diagnostics remain in controlled logs.

## Observability and recovery

Lifecycle transitions, attempts, authority/gate decisions, provider selections, artifacts, and
terminal states are traceable and auditable. Local process restart recovery must not mark abandoned
work successful. Exact heartbeat/lease/recovery semantics, distributed backends, and future job-type
migrations arrive only with their owning milestone contracts.
