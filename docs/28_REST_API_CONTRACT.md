# REST API Contract — Domain Map

Business, application, and Admin REST APIs use `/api/v1`.

## Route families
- `/auth`
- `/users`
- `/projects`
- `/datasets`
- `/datasets/{id}/versions`
- `/datasets/{id}/semantics`
- `/datasets/{id}/relationships`
- `/datasets/{id}/capabilities`
- `/models`
- `/simulations`
- `/simulations/{id}/reports`
- `/jobs`
- `/admin/ai`
- `/admin/outbound-policy`
- `/admin/system`
- `/logs`

All FastAPI route modules are owned under `backend/ipsp/api/routes/`; domain packages expose services and policies rather than duplicate routers.

## Health routes

- `/health/live` is an intentionally unversioned infrastructure probe that reports process liveness without detailed diagnostics.
- `/health/ready` is an intentionally unversioned infrastructure probe that reports whether required database/storage/runtime dependencies are ready.
- `/api/v1/admin/system/health` is the versioned application/Admin route and exposes sanitized rich diagnostics only to authorized Admin users.

## Contract rules
- Pydantic request/response schemas.
- No database ORM objects leaked directly.
- Permission checks occur server-side.
- Async job endpoints return job/run IDs and status links.
- Stable error envelope includes `error_code`, safe `message`, `trace_id`, optional field details.
- Version APIs explicitly reference dataset/semantic/model versions when reproducibility matters.
