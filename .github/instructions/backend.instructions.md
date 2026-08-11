---
applyTo: "backend/**/*.py"
---
# Backend Instructions

- Keep FastAPI routers thin: validation, authorization, service invocation, response mapping.
- Business logic belongs in services/engines, persistence in repositories.
- Use typed interfaces/protocols where provider substitution is required.
- All meaningful operations propagate `trace_id` and relevant `request_id`, `user_id`, `dataset_id`, and `simulation_run_id`.
- Never return raw exceptions to clients.
- Long-running profiling/training/simulation/reporting is a background job.
- All model and simulation outputs go through Trust & Validation before presentation.
