# Sampling & Provenance Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

This specification freezes sampling interpretation and conceptual provenance classes. It does not
create ingestion/storage runtime, tables, APIs, synthetic providers, or dependencies and does not
authorize v0.2.0 implementation.

## Sampling boundary

A sample can accurately expose schema or semantic candidates while misrepresenting full-population
frequency, class balance, time density, relationship coverage, or model support.

Dataset role values are:

- `FULL`
- `RANDOM_SAMPLE`
- `STRATIFIED_SAMPLE`
- `TIME_WINDOW_SAMPLE`
- `FILTERED_SUBSET`
- `AGGREGATED_EXTRACT`
- `UNKNOWN`

Optional sampling metadata includes source/population reference, original row count/date range,
sampling method and version, seed, strata, filters, sample fraction, population description,
selection/inclusion rules, extraction time, and provenance.

Low support in a small sample is not equivalent to low support in the full population. Capability
Discovery may mark semantic capability as discovered while statistical validation remains pending on
representative/full data. A 500-row random sample does not prove that its source population contains
only 500 rows or that observed categories are rare in the source. If a model is trained on those 500
rows, however, 500 is its training sample size and must affect validation and Trust.

## Frozen provenance classes

The complete F-002 conceptual provenance classification is:

- `OBSERVED_DATA`
- `DERIVED_DATA`
- `ORGANIZATION_CONFIG`
- `DOMAIN_CATALOG`
- `USER_ASSUMPTION`
- `PRIOR_IPSP_RUN`
- `OBSERVED_OUTCOME`
- `CURATED_BENCHMARK`
- `EXTERNAL_EVIDENCE`
- `LOCAL_KNOWLEDGE_BASE`
- `LLM_PROPOSAL`
- `SYNTHETIC_DATA`

These classes preserve evidence meaning; they are not a quality ranking or permission grant. Exact
persistence enums and storage schemas are deferred to their owning milestone.

## Common provenance record

A provenance reference conceptually retains:

- class, stable source identity/version, provider/owner, creation/acquisition time, and checksum or
  immutable reference where available;
- dataset/table/record/field/metric/result scope and source population/entity/grain;
- event/as-of/availability time, evidence cutoff, time zone, calendar/fiscal period, and freshness;
- units, currency, scale, transformations, aggregation, filters, and upstream lineage;
- collection/generation method, configuration, validation/quality, limitations, and confirmation;
- privacy/sensitivity, license/usage rights, retention, consent/evidence-access and outbound-policy
  context;
- downstream semantic, metric, model, graph, Trust, Evidence Profile, result, and audit references.

Unknown or incomplete provenance stays explicit and may limit, block, or require clarification. A
change in source, evidence meaning, method, or material metadata creates a new version/reference and
does not rewrite historical results.

## Class boundaries

`OBSERVED_DATA` records a first-party/external observation retained as source data. `DERIVED_DATA`
records a deterministic or governed transformation of observations with complete lineage; derivation
does not erase the original source class. `OBSERVED_OUTCOME` is a later real-world actual used for
reconciliation and remains distinct from a prediction, scenario output, or prior run.

Organization configuration and Domain Experience catalogs are governed configuration/knowledge, not
dataset observation. A user assumption is scenario authority only within its confirmed scope. Prior
IPSP runs preserve their original simulation basis and evidence dependence. Benchmarks, external
evidence, and local knowledge retain applicability, population, period, provenance, license, and
freshness. An `LLM_PROPOSAL` remains a proposal until separately validated and promoted through an
authorized process; the LLM never becomes numerical or evidence authority.

## Synthetic-data boundary

Every `SYNTHETIC_DATA` reference retains at least:

- generator identity/type and generator version;
- provider/adapter identity and version plus underlying library/runtime/model or model-weight
  versions where applicable;
- seed and determinism behavior;
- complete non-secret generation configuration or an immutable retrievable reference/hash;
- training/input evidence references and their access/privacy boundaries without copying secrets;
- intended purpose, population/grain/schema scope, volume, and generation time;
- quality evaluation methods, results, thresholds, evaluator versions, and limitations;
- privacy evaluation methods, results, thresholds, evaluator versions, and residual risk;
- EngineRegistry/Inventory/Resolver and independent dependency/model license decisions;
- transformations, lineage, Trust, Evidence Profile contribution, retention, and audit references.

Synthetic data may support analysis only where capability, data suitability, privacy, quality,
license, security, and policy gates pass. It never silently becomes `OBSERVED_DATA` or
`OBSERVED_OUTCOME`, never establishes that an event occurred, and never repairs absent empirical
support merely by increasing row count. Derived records that depend on synthetic input retain that
dependency in lineage and the Evidence Profile.

Provider terminology remains generic. Representative providers are governed by the
[Engine & License Registry Specification](48_ENGINE_LICENSE_REGISTRY_SPEC.md); a named candidate is
not an installed or approved runtime.

## Trust, Evidence Profile, and reproducibility

Trust evaluates provenance completeness, sampling suitability, evidence quality/applicability,
privacy, license, support, and downstream validation. The separate Evidence Profile describes the
composition and dependence on each provenance class. Neither changes a source's class.

Reproduction resolves original immutable evidence/provenance snapshots and generation metadata.
Re-run may select current eligible evidence only when clearly distinguished from reproduction.

## Deferred implementation detail

Exact provenance record schemas, row/field lineage representation, storage, retention enforcement,
APIs, synthetic generation, promotion workflows, and UI require later contract freezes and accepted
milestones.
