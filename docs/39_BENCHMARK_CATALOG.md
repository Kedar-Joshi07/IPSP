# Benchmark Catalog

Benchmarks exist to prove **generic discovery**, never to define production logic.

This catalog is governed by the [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and
[Anti-Contamination Rules](40_ANTI_CONTAMINATION.md). Benchmark coverage is acceptance evidence, not
an implementation claim or a runtime catalog.

## B1 — Large aggregated marketing funnel
Stress: cumulative panel semantics, structural missing stage, scale/performance, no spend/exposure controls.

## B2 — New product launch/orders
Stress: Product Master + Order Item Fact + one-row-per-physical-unit table; join multiplication, pricing, fulfilment, returns/refunds, short observation maturity.

## B3 — Email campaign + orders
Stress: recipient identity normalization, event sequence, last-click temporal attribution, qualified completed revenue, attribution-vs-causality.

## B4 — Hospitality/CX journey
500-row random sample from larger data. Stress: dimensioned journey, hierarchy, metric decomposition, confirmed deterministic scenario semantics, raw-data vs narrative conflict.

## B5 — NLN Sales & Finance
500-row random sample from larger data. Stress: measure families (sell-in/sell-through/gross/net), plan-vs-actual, inventory ageing, fiscal periods, negative valid finance values, sentinel values.

## B6 — Direct marketing customer/household intelligence
500-row random sample from larger data. Stress: wide customer profile, geography hierarchy, sensitive/quasi-identifying fields, look-alike, ambiguous positive/unlabelled target, feature lineage and units.

## B7 — Digital ecommerce CX/persona
500-row random sample from larger data. Stress: mixed-unit journey measures, non-monotonic re-entry, clusters/personas, target leakage, prediction horizon, composite segment field.

## Acceptance rule
A benchmark passes only if IPSP discovers the expected generic concepts without source-specific production branches/constants.

## F-002 domain-coverage strategy

The historical benchmark families above remain useful evidence. Future milestone suites should select fixtures across multiple Domain Experience families rather than treating one benchmark or one domain narrative as representative of IPSP.

| Coverage objective | Representative benchmark evidence | Required generic behavior |
|---|---|---|
| Marketing / commercial response | B1, B3 | Discover supported exposure/response/commercial concepts without a fixed funnel, attribution rule, formula, or causal claim |
| Product / Operations | B2 | Reconcile offering, order, return, inventory, entity grain, maturity, and join multiplication without mandatory fields |
| Customer Experience / journeys | B4, B7 | Preserve dimensioned, re-entering journeys; detect persona/target leakage and mixed units without forcing monotonic stages |
| Sales / Finance | B5 | Reconcile measure families, plan/actual states, fiscal time, negative monetary values, units, and sentinel semantics |
| Customer intelligence | B6 | Preserve ambiguous target state, privacy, feature lineage, horizon, and population semantics |
| Generic / Custom | Schema-perturbed and renamed variants of multiple fixtures | Reach equivalent semantic decisions without relying on source labels or column order |

### Composite/Cross-Domain evidence

Cross-domain acceptance uses intentionally related fixture versions or governed synthetic fixture construction whose provenance is explicit. It must test supported and unsupported paths across at least two domain families, including:

- entity identity, entity/aggregation grain, cardinality, deduplication, and join coverage;
- event/as-of time, horizon, time zone, calendar/fiscal period, maturity, and availability;
- unit, scale, denominator, currency, conversion, and stock/flow behavior;
- explicit transformation, relationship evidence, support, assumptions, and refusal reasons;
- no direct aggregation of a one-side measure after a one-to-many join;
- no fabricated relationship when the fixtures do not contain defensible linkage.

Benchmark pairings are test design, not frozen product flows. A passing pair cannot create a generic cross-domain edge, metric definition, Domain Experience activation rule, or preferred provider.

## Anti-memorization variants

Where practical, tests include renamed/reordered fields, changed categories, additional missing/sentinel values, altered table splits, invalid relations, and semantically incompatible units or periods. Expected assertions concern versioned semantic concepts, decisions, limitations, and lineage—not physical names or memorized outputs.
