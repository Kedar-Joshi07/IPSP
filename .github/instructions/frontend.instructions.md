---
applyTo: "frontend/**"
---
# Frontend Instructions

- Preserve the canonical CampaignSim visual language: dark surfaces, indigo/violet accents, cards, stepper, compact typography, metric cards, alerts, progress patterns, and responsive grids.
- Implement a complete light theme using shared design tokens, not one-off overrides.
- Do not hardcode campaign-specific controls. Build controls from API capability metadata.
- Keep authentication tokens out of `localStorage`; use secure server-managed sessions.
- Use accessible semantic HTML, keyboard focus states, labels, reduced-motion consideration, and responsive layouts.
- Use Plotly.js for dynamic charts unless the spec is amended.
- Significant frontend actions/errors emit sanitized events to the backend observability endpoint; do not log every hover/click.
