# Copilot Code Review Prompts

## Architecture drift
> Review the changed files against `AGENTS.md`, `docs/00_SCOPE_FREEZE.md`, and `docs/32_DECISION_LOG.md`. Identify benchmark-specific assumptions, hardcoded fields/KPIs, layer violations, missing provider abstractions, or logic placed in API/UI that belongs in services.

## Data/semantic safety
> Review for grain errors, unsafe joins, denominator mistakes, target leakage, future/post-outcome features, missing/zero confusion, sentinel handling, measurement-unit assumptions, sampling-overgeneralization, and causal-language mistakes.

## Security
> Review auth/session/permission/secret/log/upload/export behavior. Find any way a user could access an unauthorized dataset/column/run, bypass outbound policy, expose a secret, or receive a raw traceback.

## Trust
> Verify that every model/simulation result is routed through Trust & Validation and that hard constraints are intrinsic/confirmed rather than historical assumptions.
