# Error Handling Specification

## Goals
Safe user messages, detailed internal diagnostics, stable error codes, traceable failures.

## Taxonomy examples
- `AUTH-*` authentication
- `AUTHZ-*` authorization
- `DATA-*` ingestion/data/profile
- `SEM-*` semantic/clarification
- `REL-*` relationships/join safety
- `ML-*` training/model
- `LLM-*` provider/schema/policy
- `SIM-*` simulation
- `TRUST-*` validation
- `EXP-*` export/report
- `JOB-*` job processing
- `SYS-*` system

## Response contract
User/API gets safe message, code, trace ID, recoverability hints. Logs get exception type/stack trace/context subject to redaction.

No raw Python traceback in production UI.
