# UI Design System

Target identity and capability-driven presentation follow the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md). Historical visual references do not
override that authority.

## Design contract

All user-facing and administrative interfaces use the IPSP product identity and extend one shared
design system. The supplied CampaignSim HTML is a historical visual-language reference only. New
features may not rebrand IPSP as CampaignSim or introduce visually unrelated mini-applications.

The v0.1.0 foundation establishes shared semantic tokens, dark/light theme token sets, a theme switch,
and persisted preference. Later frontend milestones complete dynamic target pages using this
foundation; F2-G does not claim those pages are implemented.

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

`tokens.css`, `themes.css`, `base.css`, `layout.css`, `navigation.css`, `cards.css`, `forms.css`,
`buttons.css`, `tables.css`, `alerts.css`, `progress.css`, `charts.css`, `admin.css`, `responsive.css`,
and `print.css`.

Third-party browser assets are pinned and stored under `frontend/assets/vendor/`. Maintain version
and license metadata and do not depend on public CDNs at runtime.

## Component families

Card, metric card, selectable card, badge, alert, modal, stepper, progress, table, form group, range
control, chart container, Trust meter, Evidence Profile, assumption/constraint, graph/path lineage,
comparison, reconciliation, job state, provider/license state, consent/evidence-access state, empty
state, permission state, limitation/refusal state, and error state.

These are target component families, not claims that the complete dynamic v1.0 UI exists in v0.1.1.

## Manifest-driven composition

Components consume validated presentation metadata derived from the Semantic Manifest, Capability
Manifest, Domain Experience Manifest, Scenario Intent, organization configuration, and effective
permissions/consent. The same generic components render eligible domain and Composite/Cross-Domain
experiences. Physical source-column names, provider-specific branches, and guaranteed static domain
pages do not belong in the design-system contract.

The canonical simulation stepper labels are exactly **Define**, **Configure**,
**Enrich & Validate**, **Run**, and **Results & Compare**. Status styling never turns Amber into Green,
hides Red/blocked state, or combines Trust with the Evidence Profile.

## Accessibility

- WCAG-aware contrast in both themes.
- Visible keyboard focus and logical focus order.
- Semantic labels, form associations, and accessible validation/error summaries.
- Do not encode status, evidence authority, or graph/path state by color alone.
- Respect reduced-motion preferences.
- Responsive behavior preserves function, disclosure, warnings, and permission boundaries.
- Dynamic metadata cannot inject arbitrary HTML/script or remove required safety disclosures.
