# Benchmark Catalog

Benchmarks exist to prove **generic discovery**, never to define production logic.

## B1 — Large aggregated marketing funnel
Stress: cumulative panel semantics, structural missing stage, scale/performance, no spend/exposure controls.

## B2 — New product launch/orders
Stress: Product Master + Order Item Fact + one-row-per-physical-unit table; join multiplication, pricing, fulfilment, returns/refunds, short observation maturity.

## B3 — Email campaign + orders
Stress: recipient identity normalization, event sequence, last-click temporal attribution, qualified completed revenue, attribution-vs-causality.

## B4 — Hospitality/CX journey
500-row random sample from larger data. Stress: dimensioned journey, hierarchy, metric decomposition, deterministic benchmark scenarios, raw-data vs narrative conflict.

## B5 — NLN Sales & Finance
500-row random sample from larger data. Stress: measure families (sell-in/sell-through/gross/net), plan-vs-actual, inventory ageing, fiscal periods, negative valid finance values, sentinel values.

## B6 — Direct marketing customer/household intelligence
500-row random sample from larger data. Stress: wide customer profile, geography hierarchy, sensitive/quasi-identifying fields, look-alike, ambiguous positive/unlabelled target, feature lineage and units.

## B7 — Digital ecommerce CX/persona
500-row random sample from larger data. Stress: mixed-unit journey measures, non-monotonic re-entry, clusters/personas, target leakage, prediction horizon, composite segment field.

## Acceptance rule
A benchmark passes only if IPSP discovers the expected generic concepts without source-specific production branches/constants.
