# Observability & Audit Specification

## Event envelope
Every event requires `timestamp_utc`, `event_id`, `trace_id`, `request_id`, `component`, `action`, `status`, `severity`, and sanitized metadata. Include `session_correlation_id`, `user_id`, resolved role, `duration_ms`, `error_code`, `resource_type`, `resource_id`, and relevant project/dataset/version/model/run/LLM references when the event context supplies them.

`session_correlation_id` is a non-secret, pseudonymous correlation value. It is never the raw bearer token or cookie value.

## Logical streams
Audit, Security, Application, Frontend, Data Processing, ML, LLM, Simulation, Performance, Export, Errors, System.

Durable audit and security events may be stored in SQLite. High-volume application, frontend, performance, and runtime logs go to structured rotating files or another configured log sink; SQLite is not the complete runtime log warehouse.

## Trace propagation
Browser action → FastAPI → permission → dataset/capability/model/LLM/simulation/trust/reporting, all linked by a trace ID.

## Do not log
Passwords, password hashes, API keys, raw cookies, auth headers, secret material, unrestricted sensitive records, complete sensitive prompts.

## Frontend
Log meaningful transitions/submissions/API failures/session expiry/export/error events, filtered and rate-limited. Do not log every UI interaction.
