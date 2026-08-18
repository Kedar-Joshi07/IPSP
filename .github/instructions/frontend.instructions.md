---
applyTo: "frontend/**"
---
# Frontend Instructions

- Present IPSP as the top-level product identity. Historical prototype assets may inform compatible
  cards, steppers, alerts, typography, themes, and responsive interaction patterns only.
- Implement a complete light theme using shared design tokens, not one-off overrides.
- Do not hardcode domain-specific pages, controls, metrics, models, or outcomes. Render activated
  Domain Experience and validated capability metadata from APIs.
- Keep authentication tokens out of `localStorage`; use secure server-managed sessions.
- Use accessible semantic HTML, keyboard focus states, labels, reduced-motion consideration, and responsive layouts.
- Use Plotly.js for dynamic charts unless the spec is amended.
- Significant frontend actions/errors emit sanitized events to the backend observability endpoint; do not log every hover/click.
- Keep Trust and Evidence Profile visibly distinct, and show assumptions, basis, limitations,
  blocked paths, provider/license conditions, and reproduce state where the contract requires them.
