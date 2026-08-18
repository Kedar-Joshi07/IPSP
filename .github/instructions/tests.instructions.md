---
applyTo: "tests/**/*.py"
---
# Test Instructions

Tests are first-class acceptance evidence.

- Use semantic benchmark fixtures only to verify discovery behavior; never require production special-casing.
- Include negative tests: unsupported capabilities, ambiguous labels, unsafe joins, leakage, unauthorized access, outbound-policy denial, invalid LLM JSON, and blocked simulations.
- Include reproducibility tests for fixed seeds and exact model/dataset/semantic versions.
- Compare predictive models to simple baselines.
- Test business constraints only when they are intrinsic or explicitly confirmed.
- Test multiple Domain Experience families and safe Composite/Cross-Domain refusal using semantic
  assertions, renamed/perturbed schemas, and no benchmark constants in production.
- Cover Metric & Formula Registry cycles/grain/time/unit/currency rules, engine/license resolution,
  explicit fallback/refusal, all three simulation bases, synthetic provenance, and Trust/Evidence
  separation when the owning milestone implements them.
- Learning/outcome/Local-AI tests must prove authority tiers, empirical-data separation, eligibility,
  leakage-safe champion/challenger decisions, exact evidence snapshots, and no LLM numerical authority.
