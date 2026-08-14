# Open Questions

No question in this file blocks the accepted v0.1.0 foundation. F-002 architecture decisions are
not reopened here. Milestone-specific questions must be resolved by the appropriate functional,
data/schema, API/interface, acceptance, and dependency/license contract freezes.

## Non-blocking implementation choices

- Which supported operating-system secret store, if any, should supplement environment-backed
  SecretProvider implementations in a future milestone?
- Which PDF and Excel libraries satisfy reporting, accessibility, security, license, and
  reproducibility requirements when export implementation begins?
- Which documented thresholds and aggregation method should produce overall Trust outcomes while
  preserving mandatory dimension scores and reason codes?
- Which local LLM runtime/model should be the default candidate after capability, hardware,
  security, model-weight-license, and evaluation review?
- What persistence shapes, identifiers, retention rules, and indexes should implement Domain
  Experience, metric, engine/license, scenario/evidence, and learning contracts? Detailed schema
  decisions are deferred to F2-G and owning capability milestones.
- What exact route/resource shapes should expose those contracts without implying that future
  surfaces are currently implemented? Detailed API decisions are deferred to F2-G.

## Future-scope timing and activation questions

- What evidence and scale threshold should justify optional PostgreSQL after v1.0?
- Which datasets and validation requirements should activate advanced causal or solver-backed
  optimization providers after the bounded v1.0 foundation?
- Which post-v1 milestone should introduce MFA, enterprise SSO, or directory integration?
- What governance evidence should permit optional PEFT/LoRA adaptation after retrieval and memory
  approaches have been evaluated?
- What security, privacy, license, consent, and evidence contracts must be met before enabling
  Remote/Hybrid LLM, `PUBLIC_WEB`, or `APPROVED_CONNECTORS`?

## Resolved by F-002 — not open

- IPSP is the neutral product identity; CampaignSim is historical visual reference only.
- Domain Experience Packs extend one dataset/domain-agnostic core.
- Finance and Composite/Cross-Domain are first-class, evidence-activated domain families.
- Numerical metric truth belongs to the Metric & Formula Registry.
- EngineRegistry, LicenseRegistry, and EngineResolver provide provider-neutral selection boundaries.
- The exact simulation bases are `DATA_BASED`, `MIXED`, and `INTENT_BASED`.
- Trust and Evidence Profile are separate authorities.
- SimulationLearningStore and OutcomeReconciliation preserve governed learning without circular
  contamination.
- v1.0 is bounded; advanced causal, optimization, external-intelligence, enterprise-scale, and
  specialized Quant Finance capabilities may mature later.
- v2.0 is not pre-assigned.
