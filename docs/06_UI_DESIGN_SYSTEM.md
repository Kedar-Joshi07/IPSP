# UI Design System

## Design contract
All user-facing and administrative interfaces must extend the visual language established by the supplied CampaignSim HTML. New features may not introduce visually unrelated mini-applications.

The v0.1.0 foundation establishes shared semantic tokens, dark and light theme token sets, a theme switch, and persisted preference. The v0.7.0 frontend milestone completes all dynamic pages using this existing foundation; light-theme architecture is not deferred to that milestone.

## Token families
- Background/surface levels
- Text/muted text
- Accent/accent-secondary
- Green/amber/coral status colors
- Borders
- Typography: heading/body/mono metric roles
- Spacing scale
- Radii
- Shadows/glows
- Motion duration/easing

## CSS modules target
`tokens.css`, `themes.css`, `base.css`, `layout.css`, `navigation.css`, `cards.css`, `forms.css`, `buttons.css`, `tables.css`, `alerts.css`, `progress.css`, `charts.css`, `admin.css`, `responsive.css`, `print.css`.

Third-party browser assets are pinned and stored under `frontend/assets/vendor/`. Maintain version and license metadata and do not depend on public CDNs at runtime.

## Component families
Card, metric card, selectable card, badge, alert, modal, stepper, progress, table, form group, range control, chart container, trust meter, empty state, permission state, error state.

## Accessibility
- WCAG-aware contrast in both themes.
- Visible keyboard focus.
- Semantic labels and form associations.
- Do not encode status by color alone.
- Respect reduced-motion preferences.
- Responsive behavior must preserve function, not only appearance.
