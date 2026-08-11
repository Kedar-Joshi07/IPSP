# Copilot Testing Prompts

## New feature test prompt
> For this feature, add tests covering happy path, boundary/invalid input, authorization denial, error logging/trace ID, reproducibility where stochastic, and one anti-contamination/unsupported-capability case if relevant.

## Benchmark prompt
> Use the benchmark only as a fixture. Assert generic semantic outcomes (grain/relationship/journey/measure family/privacy/etc.). Do not create benchmark-name branches or constants in production code.

## Regression prompt
> Run tests that protect locked architectural decisions: ML-only operation, remote policy denial, semantic conflict blocking, unsafe join warning, target leakage rejection, and reproducible exact-version simulation.
