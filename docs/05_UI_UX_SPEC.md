# UI / UX Specification

## Canonical reference
`reference/Campaign_simulator_UI.html` is the official visual reference for IPSP v1.0.

Preserve its design language: dark layered surfaces, indigo/violet accents, glow treatment, compact cards, stepper, metric cards, selectable cards, status badges, alerts, progress, tabs, comparison tables, mono metric typography, and responsive grids.

## Themes
- Dark: default/original identity.
- Light: complete equivalent theme using the same component/token system.
- User preference persisted; system/default setting available.
- The v0.1.0 foundation includes shared semantic tokens, complete dark and light token sets, theme switching, and preference persistence. Later UI milestones apply that foundation to richer pages.

## Offline browser assets

Production UI operation must not require a public CDN. Plotly.js and other third-party browser bundles are pinned and vendored under `frontend/assets/vendor/`, with version and license inventory. Any explicitly enabled external asset access is backend-policy governed.

## Main page families

- Login
- Dashboard
- Projects / workspace
- Dataset onboarding workflow
- Simulation workflow
- Simulation history
- Profile/preferences
- Admin overview
- Admin users/access
- Admin datasets/semantics/models
- Admin AI/outbound policy
- Admin system/health/backups
- Admin logs

## Dataset onboarding — 5 steps
1. Upload & context
2. Understand
3. Clarify/confirm
4. Capability discovery
5. Ready

## Simulation — 5 steps
1. Select dataset/capability
2. Configure scenario
3. Validate support
4. Run
5. Results

## Dynamic controls
Controls come from capability metadata:
- Numeric → slider/input with empirical/support bounds
- Categorical → select/cards
- Boolean → toggle
- Date/time → appropriate picker
- Hierarchy → dependent filters
- Assumption-only controls must display `USER-DEFINED ASSUMPTION — Not learned from historical data`.

## Trust UI
- Green: validated/high support
- Amber: limited/novel/extrapolative/review
- Red: blocked/invalid/critical ambiguity

Disabled capabilities remain visible with an explanation when useful.
