# Domain Experience Pack Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.5.0 — Metric & Formula Registry + Domain Experience Foundation

This specification freezes the provider/registry-style Domain Experience contract and the
CrossDomainSemanticGraph semantic contract. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md). It does not create packages, runtime
registries, database tables, API routes, dependencies, or simulation execution behavior.

## Core invariant

IPSP Core remains dataset- and domain-agnostic. Registered Domain Experience Packs extend the core;
they do not fork it into separate Marketing, Finance, Product, Sales, Customer Experience, or
Operations engines.

A pack may contribute domain knowledge and presentation metadata. It cannot:

- define generic numerical truth outside the Metric & Formula Registry;
- require a benchmark or domain-specific physical source-column name;
- make one physical schema mandatory;
- hardcode a model, provider, solver, or guaranteed response;
- bypass semantic, relationship, capability, Trust, Evidence, license, privacy, or consent gates;
- invent cross-domain relationships or simulation edges;
- treat benchmark narrative as runtime truth.

## Provider and registry concepts

### DomainExperience

`DomainExperience` is the provider-neutral interface exposed by a pack implementation. Conceptually
it supplies an immutable manifest and curated catalogs through typed contracts. Core services query
the interface; they do not branch on hardcoded domain names or import provider-specific logic.

### DomainExperienceManifest

Each `DomainExperienceManifest` conceptually declares:

| Contract area | Content |
|---|---|
| Identity | Stable experience ID, name, domain family, manifest version, provider, and provenance |
| Compatibility | Supported IPSP Core and contract versions plus declared dependencies/conflicts |
| Semantic catalog | Semantic concept IDs, descriptions, aliases, relationship hints, and prerequisites |
| Objective taxonomy | Supported analytical or decision objectives and their semantic prerequisites |
| Metrics | Metric IDs requested from the Metric & Formula Registry; never private formula authority |
| Capabilities | Hints and prerequisites used as proposals for Capability Discovery |
| Controls/constraints | Typed templates and eligibility prerequisites; not automatic source-field mappings |
| Presentation | UI metadata, analysis sections, comparison views, terminology, and explanation vocabulary |
| Benchmarks | Optional curated reference catalogs with provenance and applicability constraints |
| Activation | Required/optional semantic evidence, ambiguity rules, and reason templates |
| Governance | License, security, privacy, outbound/evidence requirements, and organization policy hooks |

Exact serialization and persistence fields are deferred to later contract freezes.

### DomainExperienceRegistry

`DomainExperienceRegistry` conceptually:

- discovers installed/available pack providers without importing domain rules into generic core;
- validates manifest schema, identity, version, compatibility, provenance, and policy;
- prevents conflicting duplicate identities/versions;
- exposes eligible semantic catalogs, objectives, metric requests, capability hints, constraints,
  UI metadata, and explanation vocabulary;
- records why a pack is available, ineligible, incompatible, disabled, or blocked;
- resolves exact versions for reproducibility;
- supports multiple simultaneous Domain Experience activations for one dataset/project.

Registry availability is not dataset activation. A pack being installed never proves its semantic
prerequisites are satisfied.

## Frozen domain families

- Marketing
- Product
- Sales
- Customer Experience
- Finance
- Operations / Demand
- Generic / Custom
- Composite / Cross-Domain

A dataset may activate one family, several families, Generic/Custom, or Composite/Cross-Domain.
Finance and Composite/Cross-Domain are first-class but evidence-activated, not guaranteed.

## Representative baseline concept catalog

The following concepts are representative examples for curated packs. They are not mandatory
schema, physical column names, guaranteed relationships, formulas, objectives, or capabilities.

| Domain family | Representative semantic concepts only |
|---|---|
| Marketing | audience, exposure, response, attribution, spend, offer, channel, commercial outcome |
| Product | offering, launch, adoption, price, demand, order, return, inventory, lifecycle |
| Sales | account, opportunity, stage, territory, quota, forecast, win/loss, order, revenue |
| Customer Experience | customer, interaction, satisfaction, effort, issue, resolution, retention, churn |
| Finance | actual, budget, forecast, variance, revenue, cost, margin, cash, receivable/payable, debt, FX |
| Operations / Demand | demand, inventory, capacity, backlog, lead time, fulfilment, supplier, service level |
| Generic / Custom | entity, event, state, time, measure, outcome, control, constraint, relationship |
| Composite / Cross-Domain | domain concept, cross-domain relationship, shared entity, flow, dependency, constraint |

Catalog concepts are semantic IDs mapped through evidence and confirmation. A similarly named source
field is not automatically a match.

## Activation evidence

Activation evaluates a specific dataset/manifest version against an exact pack/manifest version.
The evidence record conceptually includes:

- candidate domain family and experience version;
- matched, missing, ambiguous, and contradicted semantic prerequisites;
- supporting Dataset Semantic Manifest concepts and relationship evidence;
- metric and capability prerequisites;
- time, grain, unit, currency, maturity, and sensitivity limitations;
- organization policy, license, privacy, and evidence-access eligibility;
- confirmation history and reasoned activation/limitation/refusal result;
- provenance and reproducibility references.

Activation follows:

```text
deterministic semantic evidence
  → eligible pack candidates
  → prerequisite and conflict validation
  → targeted confirmation when ambiguous
  → versioned activation decision with reasons
```

Multiple activations remain distinct and may contribute to a Composite/Cross-Domain request only
after cross-domain reconciliation.

## Catalog and override precedence

Domain terminology, concepts, objectives, metric requests, and constraint candidates follow the
frozen precedence:

1. organization-configured;
2. observed or confirmed dataset values;
3. curated Domain Experience Pack;
4. explicit custom user assumption.

Precedence resolves eligible catalog/configuration candidates; it cannot override intrinsic
validity, evidence, provenance, security, license, or relationship-safety requirements. Material
conflicts remain explicit and produce a new version after confirmation.

## Versioning and compatibility

Domain Experience versions may evolve independently from the IPSP application. Each activation and
result references exact core, contract, pack, manifest, semantic, metric, and organization
configuration versions.

Compatibility checks cover:

- required IPSP Core and contract versions;
- semantic-catalog and Metric & Formula Registry compatibility;
- dependent or conflicting packs;
- migration or deprecation notices;
- provider and license eligibility;
- reproducibility of historical activations.

Updating a pack does not rewrite a prior activation or result. Re-run and reproduce distinguish
current eligible versions from the original snapshot.

## Objective, capability, constraint, and UI metadata

Objective taxonomy and capability hints are proposals to generic services. Capability Discovery
independently validates semantics, data, model/engine support, and Trust. Constraint templates become
enforceable only after semantic mapping and confirmation where required.

UI metadata may recommend labels, sections, controls, comparisons, and explanation vocabulary. It
does not create guaranteed static pages, expose unsupported controls, or embed calculations. Generic
frontend services render only validated, authorized, capability-supported metadata.

## Optional benchmark catalogs

A pack may reference curated benchmark knowledge only when it records provenance, population,
period, units, grain, applicability, license, freshness, and limitations. Benchmarks are priors or
assumptions where appropriate, never observed dataset truth or guaranteed effects.

Repository benchmark fixtures remain tests of generic discovery. They do not automatically populate
runtime catalogs.

## CrossDomainSemanticGraph

The `CrossDomainSemanticGraph` is the versioned semantic authority for validated relationships among
concepts used across Domain Experiences. It describes whether concepts can be responsibly composed;
it does not define simulation execution, which is deferred to F2-E.

### Graph identity and nodes

Each graph version references the project/dataset versions, Dataset Semantic Manifest versions,
Domain Experience/manifest versions, organization configuration, evidence cutoff, and supersession
history.

A node conceptually identifies:

- semantic concept ID and owning/declaring experience version;
- dataset/table/entity mappings through exact Semantic Manifest versions;
- entity and aggregation grain;
- event/availability time, time zone, calendar, and fiscal semantics;
- unit, currency, scale, stock/flow, and sensitivity metadata;
- evidence, confirmation, provenance, and support state.

Nodes reference semantic concepts, not mandatory physical columns.

### Relationship contract

Each directed or undirected relationship conceptually records:

- source concept and target concept;
- entity relationship and identity/mapping rule;
- source, target, and required aggregation grain;
- cardinality, direction, coverage, and duplication risk;
- event/availability-time relationship, window, time zone, calendar, and fiscal-period mapping;
- unit, currency, scale, conversion, and stock/flow compatibility;
- explicit transformation or reconciliation reference;
- relationship meaning, such as structural, identity, temporal, hierarchy, measure dependency,
  plan/actual, commercial flow, or another governed semantic type;
- evidence references, confidence, ambiguity, confirmation, provenance, and support status;
- version and supersession references.

Support status distinguishes proposed, validated/confirmed, limited, unsupported, and blocked
relationships conceptually; exact persisted enums are deferred.

### Inference and confirmation

```text
infer → validate → confirm when ambiguous → persist
```

Inference may use deterministic profile evidence, confirmed semantics, organization configuration,
and curated pack catalogs. Statistical association, name similarity, pack hints, benchmarks, or LLM
proposals cannot independently establish a supported relationship.

### Required reconciliation

Before a relationship is supported, the graph reconciles:

1. entity identity and entity grain;
2. source, target, and output aggregation grain;
3. cardinality, join coverage, and measure-multiplication risk;
4. event and availability time plus time-zone alignment;
5. calendar, business-calendar, and fiscal-period mappings;
6. units, scale, denominator, stock/flow behavior, and conversions;
7. currency identity, rate source/type/effective time, and conversion direction where needed;
8. transformation lineage, evidence, support, and reproducibility.

Ambiguity requests targeted confirmation. Incompatibility limits or blocks composition. The graph
never invents an arbitrary join, conversion, transformation, causal relationship, or edge to satisfy
user intent.

### Graph validation and lifecycle

Validation checks exact node/edge references, semantic compatibility, cardinality, grain, time,
unit/currency, transformation, evidence coverage, policy, and provenance. Completed results reference
an immutable graph version; corrections produce a new version.

An absent or unsupported relation remains visible with reasons where useful. No defensible relation
means constrain or refuse downstream composition.

## Deferred implementation detail

F2-C freezes semantic contracts only. Simulation node/edge execution, ordering, scenario behavior,
Trust scoring, persistence tables, API resources, registry discovery mechanics, and package loading
are assigned to later F-002 phases and milestone contract freezes.
