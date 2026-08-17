# UI / UX Specification

## Status and product identity

**F-002 target contract:** FROZEN

**Dynamic target UI implementation:** NOT IMPLEMENTED

The target product identity is **Intelligent Predictive Simulation Platform (IPSP)**. CampaignSim
and `reference/Campaign_simulator_UI.html` are historical visual references only; they do not define
the product name, information architecture, domain architecture, workflow semantics, or runtime
capabilities.

## Visual reference

Preserve the reference's design language: dark layered surfaces, indigo/violet accents, glow
treatment, compact cards, steppers, metric and selectable cards, status badges, alerts, progress,
tabs, comparison tables, mono metric typography, and responsive grids.

## Themes

- Dark: default/original visual direction.
- Light: complete equivalent theme using the same component/token system.
- User preference is persisted; a system/default setting is available.
- The v0.1.0 foundation includes shared semantic tokens, complete dark/light token sets, theme
  switching, and preference persistence. Later UI milestones apply that foundation to richer pages.

## Offline browser assets

Production UI operation must not require a public CDN. Plotly.js and other third-party browser
bundles are pinned and vendored under `frontend/assets/vendor/`, with version and license inventory.
Any explicitly enabled external asset access is governed by backend policy.

## Frozen target navigation

- Home / Overview
- Projects / Workspaces
- Data
- Analysis & Simulation
  - Marketing
  - Product
  - Sales
  - Customer Experience
  - Finance
  - Operations / Demand
  - Generic / Custom
  - Composite / Cross-Domain
- Scenario Library
- Compare
- Models & Learning
- Jobs
- Administration
- Profile

Login and authorization entry remain outside or before this authenticated navigation. Administration
may compose users/access, data/semantics/models, AI/outbound/license policy, system/health/backups,
and audit/log views according to permissions. Target placement is not an implementation claim.

## Dataset onboarding — five steps

1. Upload & Context
2. Understand
3. Clarify & Confirm
4. Capability Discovery
5. Ready

## Simulation — exactly five steps

1. Define
2. Configure
3. Enrich & Validate
4. Run
5. Results & Compare

No sixth canonical step or alternate domain-specific workflow replaces this sequence.

## Capability-driven UI composition

Target UI composition is driven by:

```text
Semantic Manifest
+ Capability Manifest
+ Domain Experience Manifest
+ Scenario Intent
+ Organization Config
+ Permissions / Consent
```

The UI renders only schema-validated, version-compatible, permission-eligible metadata. Domain pages
are capability-driven views, not guaranteed static screens. A Domain Experience may recommend
terminology, sections, controls, comparison views, and explanations, but it cannot embed private
formula truth, invent a relationship, expose an unsupported control, or bypass Trust, Evidence,
license, privacy, or policy gates.

## Dynamic controls

Controls derive from validated semantic/capability/scenario contracts:

- Numeric → bounded slider/input with unit, support, and extrapolation state.
- Categorical → select/cards with eligible values and unknown/missing semantics.
- Boolean → toggle when the concept is validly Boolean and controllable.
- Date/time → picker aligned to horizon, time zone, calendar, and maturity semantics.
- Hierarchy → dependent filters only through validated hierarchy/relationship versions.
- Assumption-only controls display `USER-DEFINED ASSUMPTION — Not learned from historical data`.

Identifiers, outcomes, post-outcome fields, unavailable-at-decision-time values, and prohibited
sensitive features are not exposed as ordinary controls.

## Trust, Evidence, and capability states

- Green: required applicable validation passes.
- Amber: limited, novel, extrapolative, assumption-dependent, or review-worthy.
- Red: blocked, invalid, prohibited, or critically ambiguous.

Trust and the Evidence Profile are displayed as separate authorities. Implemented, unavailable,
limited, blocked, and refused states remain distinct. Disabled or refused capabilities remain visible
with safe actionable reasons when useful; planned capability is never advertised as operational.

## Permissions, consent, and safe failure

Navigation, controls, evidence access, provider choices, learning actions, exports, and administration
are permission/policy driven and revalidated server-side. The UI does not infer authority from a
visible element, feature flag, stored credential, or prior consent. Errors show safe messages, stable
codes, trace IDs, and remediation without raw stack traces or inaccessible metadata.
