# Benchmark / Domain / Legacy Anti-Contamination Rules

## Authority and invariant

Generic IPSP Core remains dataset/schema and domain agnostic. F-002 permits curated domain knowledge
inside registered, versioned Domain Experience definitions; it does not permit that knowledge to
leak into generic services, schemas, routes, persistence, model routing, or UI control logic.

## Permitted knowledge locations

Domain- or benchmark-specific terminology and examples may appear only in:

- registered Domain Experience Packs and their versioned manifests/catalogs;
- benchmark fixture data and expected semantic manifests;
- benchmark tests, reference documentation, and acceptance evidence;
- explicit organization configuration or user assumptions with provenance;
- versioned Metric & Formula Registry definitions selected through governed precedence.

Presence in a permitted location does not make the content observed truth, mandatory schema, or an
enabled runtime capability.

## Domain Experience boundary

A registered Domain Experience may provide terminology, semantic concepts, objective taxonomy,
metric ID requests, capability hints, controls/constraint templates, UI metadata, recommended
analysis/comparison views, explanation vocabulary, and optional benchmark catalogs.

It must not:

- require physical source-column names;
- define generic numerical truth outside the Metric & Formula Registry;
- hardcode model or provider winners;
- guarantee a relationship, response, causal effect, or capability;
- bypass Dataset Semantic Manifest mapping, relationship/grain validation, Trust/Evidence, license,
  privacy, outbound, or consent gates;
- fork IPSP Core into a separate domain product.

Generic dispatch may load a registered experience by contract identity/version. It may not branch on
benchmark fields, customer narratives, or hardcoded business-domain assumptions.

## Benchmark rule

Benchmarks prove generic discovery; they never define production logic. Benchmark examples remain
fixtures or reference knowledge, not runtime truth. Their source names, stages, labels, formulas,
models, controls, and expected outputs cannot become generic constants or mandatory contracts.

A benchmark passes only when IPSP discovers supported generic concepts through deterministic
evidence, validated metadata, and confirmation without source-specific production branches.

## Metric and relationship rule

Domain catalogs request semantic metric IDs; the generic Metric & Formula Registry owns versioned
formula validation and numerical evaluation. Cross-domain relationships require entity, grain, time,
calendar/fiscal, currency, unit, transformation, evidence, and support reconciliation. No pack,
benchmark, UI reference, or LLM may invent a join or graph edge.

## Legacy and visual-reference boundary

Previous RdF/Streamlit simulator specifications and prompt packs are not IPSP v1.0 implementation
authority. Reusable lessons include progress tracking, acceptance gates, non-causal guardrails,
validation, provider boundaries, and reproducibility. Fixed schemas, stages, targets, KPIs, models,
controls, and framework choices are discarded as generic assumptions.

The supplied HTML contributes visual design and interaction patterns only. Its prototype content,
calculations, search terminology, model names, and static values are not copied into generic runtime
behavior.

## Enforcement expectations

- Architecture/static tests search generic production paths for prohibited benchmark/domain
  constants and vendor-specific architecture assumptions.
- Benchmark-specific tests and fixtures remain clearly scoped outside generic production packages.
- Domain Experience manifests are schema-validated, versioned, provenance-bearing, and separately
  reviewed for contamination.
- Documentation labels representative domain concepts as examples rather than mandatory fields.
- Any proposed exception stops with a contract or architecture review; convenience is not authority.

## Multi-domain and Composite/Cross-Domain testing

Acceptance evidence must span multiple Domain Experience families and include both defensible and deliberately unsupported Composite/Cross-Domain fixture relationships. Tests assert semantic concepts, graph decisions, reconciliation evidence, limitations, and refusals—not benchmark story completion.

Schema-renamed and structurally perturbed variants should prove that generic core behavior does not depend on familiar labels, column order, category values, or a single benchmark's topology. Cross-domain tests must fail safely for incompatible entity/grain/cardinality, time/calendar, unit/currency, transformation, or evidence states. They must not add a production shortcut merely to make a benchmark path pass.

Synthetic fixture data is allowed for test construction only with explicit fixture scope and provenance. It does not establish empirical truth, a runtime catalog, a default formula, or a supported production relationship.
