# REST API Contract — Domain Map

Business, application, and Admin REST APIs use `/api/v1`.

## Status boundary

This document identifies target API ownership domains. It does not claim that every route family is
implemented. The accepted v0.1.0 surface is limited to the verified foundation routes documented in
the [README](../README.md); v0.2.0 and later capability endpoints are not started. Exact F-002
resources, payloads, paths, compatibility rules, and authorization matrices are deferred to F2-G
and their owning milestone contract freezes.

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

F-002 requires future API ownership to be capable of exposing, when implemented and authorized:

- Dataset Semantic Manifest, Metric & Formula Registry, Domain Experience activation, and
  CrossDomainSemanticGraph state;
- capability decisions separately from EngineRegistry, LicenseRegistry, and EngineResolver results;
- ScenarioIntentManifest and CompositeSimulationGraph versions;
- separate Trust and Evidence Profile results;
- history, comparison, re-run, reproduce, and authorized export;
- SimulationLearningStore, observed-outcome reconciliation, and learning-eligibility status.

This list reserves architectural ownership only. It does not create endpoints or settle whether a
concept is nested under a project, dataset, scenario, run, registry, or Admin resource.

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
- Future versioned APIs also reference applicable metric, Domain Experience, engine/license,
  scenario graph, evidence, policy/consent, and learning-contract versions when reproducibility
  requires them.
- Responses distinguish implemented, unavailable, limited, blocked, and refused capability states;
  a frozen target is never advertised as operational.
