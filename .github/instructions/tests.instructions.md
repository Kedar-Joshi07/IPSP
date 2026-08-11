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
