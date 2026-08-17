# Finance Domain Experience Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.11.0 — Domain Intelligence Completion, with foundations in earlier
registry and simulation milestones

This specification freezes the Finance Domain Experience family, its dynamic activation boundary,
and representative capability contracts. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and the generic
[Domain Experience Pack Specification](47_DOMAIN_EXPERIENCE_PACK_SPEC.md). It does not implement a
Finance engine, impose a source schema, define private formula truth, install a provider, or guarantee
any Finance capability.

## Core boundary

Finance is a registered Domain Experience family that composes with IPSP Core. It is not a separate
hardcoded platform, fixed financial model, mandatory page set, or branch of generic compute logic.

A Finance pack may contribute semantic concepts, objective taxonomy, metric requests, capability and
constraint prerequisites, terminology, explanations, and UI metadata. Numerical truth remains in the
versioned Metric & Formula Registry; providers remain behind generic engine interfaces; execution
remains in validated simulation/model services.

## Dynamic activation

Finance activates for an exact dataset/project version only when deterministic semantic evidence and
confirmed metadata satisfy the relevant pack prerequisites. Activation evaluates:

- Finance concept/entity/measure/state roles and their confirmation state;
- entity and aggregation grain, cardinality, hierarchy, and lineage;
- event/as-of/availability time, period, maturity, restatement, time zone, calendar, and fiscal
  semantics;
- units, scale, currency, rate/ratio denominators, sign conventions, and stock/flow behavior;
- supported plan/actual/forecast/scenario meanings and comparisons;
- metric definitions, accounting relationships, transformations, allocations, and tolerances;
- data coverage, representativeness, freshness, support, privacy, license, evidence access, and
  organization policy;
- requested capability, eligible engines/providers, and Trust requirements.

Missing prerequisites limit, request targeted confirmation, or refuse the capability. A field name,
benchmark schema, Finance-themed narrative, or installed library never activates Finance by itself.

## Semantic prerequisites, not physical columns

Finance contracts reference semantic concepts such as organization/entity, period, scenario/version,
account/classification, measure/value, currency, cash flow, receivable/payable, obligation, exposure,
and decision/constraint. These are examples of semantic roles, not required physical source-column
names or a mandatory chart of accounts.

An eligible capability may require only the subset relevant to its objective. For example, a variance
analysis needs aligned comparable measure/basis/period/grain semantics; it does not require every
Treasury, credit, valuation, or three-statement concept. Similarly, a liquidity stress request cannot
be enabled merely because a dataset supports budget variance.

## Capability families

Capability declarations are proposals evaluated independently by Capability Discovery. Representative
families and prerequisites are:

| Family | Representative scope | Semantic prerequisites and boundary |
|---|---|---|
| Corporate Performance / FP&A | Performance views, planning, management reporting, scenario comparison | Confirmed measures, entity/aggregation hierarchy, period/calendar, basis/version, units/currency, metric and comparison semantics |
| Actual / Budget / Forecast | Aligned actual-plan-forecast comparisons and versions | Explicit basis/state, comparable grain and periods, version/as-of/maturity, currency/unit alignment; labels alone do not establish comparability |
| Variance | Absolute, relative, volume/rate/mix or other supported decompositions | Versioned metric definitions, comparison direction, denominator/safe-division, signs, grain/time/currency alignment, and supported decomposition relationships |
| Profitability / margin / contribution | Revenue/cost/margin/contribution/unit-economics views | Confirmed economic meaning, allocation and aggregation rules, units/currency, scope, sign and qualification; no universal non-negative rule |
| Rolling and scenario forecasts | Time-aware forecast updates and scenario paths | Target/horizon, point-in-time availability, cadence/calendar, historical support, backtesting, uncertainty, and control/assumption semantics |
| Treasury & Liquidity | Cash position/flows, liquidity horizon, funding or buffer scenarios | Cash/flow/position semantics, dates/maturity, entity/currency, availability/restrictions, supported inflow/outflow and conversion relationships |
| AR/AP and working capital | Receivable/payable exposure, aging, collections/payment timing, working-capital scenarios | Counterparty/obligation/event semantics, amounts, due/as-of/settlement time, state/maturity, entity/currency/grain, and validated identities |
| Debt / interest / FX | Debt service, interest and currency exposure where data supports | Instrument/obligation terms, principal/rate/maturity, currency, rate/fixing/conversion source, cash-flow timing, and provider/license support where specialized |
| Three-statement relationships | Supported income, position, and cash-flow relationships and roll-forwards | Confirmed classifications, stock/flow and period semantics, entity/consolidation scope, mapping, eliminations/allocations where applicable, and reconciliation tolerances |
| Risk & Stress | Sensitivity, scenario, Monte Carlo, and stress paths | Risk factor/exposure, supported dependency/response, shock assumptions, horizons, distributions or scenarios, constraints, uncertainty, and evidence limits |
| Credit / Collections | Risk prediction, exposure segmentation, collections prioritization or scenarios | Defensible outcome, observation maturity, point-in-time features, entity/obligation grain, policy/fairness/privacy constraints, and no causal claim from prediction |
| Valuation / Capital Investment | Cash-flow/return comparison, project evaluation, scenario and sensitivity | Versioned cash-flow and timing semantics, discount/terminal assumptions, currency/inflation/tax treatment where applicable, decision criteria, and sensitivity |
| Optional Quant Finance subpack | Specialized instrument, volatility, pricing, or portfolio methods | Instrument-specific semantics, market-data provenance/as-of state, conventions, calibration, provider/model-weight/dependency license, and specialist validation |

Capability breadth is not activation breadth. Each requested path is separately enabled, limited,
blocked, or refused with evidence-based reasons.

## Separation of analytical authorities

Finance presentation must keep these operations distinct:

| Operation | Governing meaning |
|---|---|
| Prediction / forecasting | Estimates an outcome from information available at the declared horizon; association is not causation |
| Deterministic accounting logic | Evaluates confirmed identities, mappings, allocations, roll-forwards, conversions, or reconciliations from registry definitions |
| Simulation / what-if | Evaluates a versioned ScenarioIntentManifest and CompositeSimulationGraph under controls and assumptions |
| Stress testing | Applies explicit shocks/adverse assumptions with scope, severity, dependencies, constraints, and evidence limits visible |
| Optimization | Selects decision variables against a declared objective and feasible constraints; it requires validated response/accounting relationships and solver eligibility |

No operation silently substitutes for another. A forecast does not repair an accounting imbalance; a
deterministic identity does not establish a predictive response; stress assumptions are not observed
probabilities; optimization does not prove causality.

## Actual, Budget, Forecast, variance, and planning

Actual, Budget, Forecast, Target, Scenario, and related organization-defined states are semantic
values with provenance, versions, as-of dates, maturity, and precedence. `Unknown` is not mapped to
any state. Comparing states requires aligned entity/grain, metric definition, period/calendar,
currency/unit, scope, and qualification.

Variance definitions declare comparison direction, formula, denominator and zero/null behavior,
units, favorable/unfavorable semantics if organization-confirmed, and decomposition dependencies.
Rolling forecasts declare origin/as-of time, horizon, update cadence, frozen observations, and
current assumptions. Revised plans and forecasts create versions; they do not rewrite prior results.

## Profitability, margin, contribution, and unit economics

Metric requests resolve through the Metric & Formula Registry. Definitions must establish economic
scope, components, allocations, exclusions, aggregation, required grain, time, units/currency,
safe-division, and lineage. Directly aggregating a one-side measure after a one-to-many join is
prohibited without a validated grain-safe transformation. Monetary measures are not universally
non-negative.

## Treasury, working capital, debt, interest, and FX

Position and flow concepts remain distinct. Scenario paths align cash availability/restrictions,
receivable/payable states, due and settlement timing, obligation maturity, interest conventions,
currency exposure, conversion/revaluation rules, entity scope, and calendars. Debt, interest, FX, or
specialized instrument paths activate only where data, terms, relationships, and eligible providers
support them.

No exchange rate, yield curve, payment behavior, collection effect, funding access, or refinancing
assumption is invented. External or analog inputs retain provenance, license, freshness, applicability,
consent, and Evidence Profile dependence.

## Three-statement and deterministic reconciliation

Three-statement support is relationship-driven rather than schema-driven. Applicable identities and
roll-forwards reference versioned metrics and validated semantic mappings. Reconciliation covers
entity/consolidation scope, classifications, inter-period stock/flow continuity, signs, units,
currencies, translations, allocations/eliminations where confirmed, rounding/tolerance, and residuals.

Predictive or simulated nodes feed a statement relationship only through an explicit supported edge
and transformation. Material unexplained imbalance produces a limitation or refusal; the system does
not insert an unexplained plug merely to balance an output.

## Risk, stress, Credit/Collections, and valuation

Risk/stress nodes distinguish observed exposure, modeled dependency, user shock, external prior, and
synthetic support. Scenario likelihood is shown only when defensibly estimated. Tail output requires
appropriate support, calibration, uncertainty, and warnings.

Credit/Collections prediction preserves outcome maturity, point-in-time availability, leakage,
population coverage, calibration, privacy, policy, and fairness constraints. Predicted risk or
collection likelihood is not a causal effect of an action and does not by itself authorize adverse
or automated decisions.

Valuation and capital-investment logic exposes cash-flow, discount, terminal, inflation, tax, timing,
currency, and reinvestment assumptions where applicable. Decision rules and sensitivity ranges are
versioned; an LLM or benchmark cannot supply hidden numerical truth.

## Optional Quant Finance subpack

Specialized Quant Finance is optional and isolated from ordinary Finance/FP&A behavior. It requires a
separate compatible Domain Experience subpack, exact instrument/market semantics, current market-data
provenance, conventions, calibration/validation, resource/security review, and Engine/License
eligibility. `arch` or QuantLib may be provider candidates where justified; neither is a required
dependency nor evidence that the capability is implemented.

## Cross-Domain composition

Finance concepts may participate in Composite/Cross-Domain paths only through a validated
`CrossDomainSemanticGraph` and `CompositeSimulationGraph`. Representative commercial-to-cash,
price-to-demand/margin/working-capital, or experience-to-retention/value paths are examples only.
Every edge independently reconciles entity, grain, cardinality, time/calendar, unit/currency,
transformation, evidence, support, license, and Trust. No generic core Finance-specific branch or
arbitrary relationship is permitted.

## Trust, Evidence Profile, provenance, and refusal

Applicable Finance Trust checks include semantic and relationship validity, temporal leakage,
support/extrapolation, constraints, accounting reconciliation, unit/currency/time/calendar consistency,
model/engine validation, simulation support, optimization feasibility, privacy/outbound policy,
licensing, and reproducibility.

The separate Evidence Profile makes dependence on observed first-party values, later observed
outcomes, organization configuration, assumptions, synthetic data, analogs/benchmarks, external
evidence, prior runs, and extrapolation visible. Simulated, predicted, benchmark, synthetic, or
LLM-proposed values never silently become Actual or another observed state.

Unsupported physical/semantic mapping, ambiguous comparison basis, unsafe aggregation, unavailable-at-
decision-time evidence, missing relation, irreconcilable accounting/unit/currency/time state,
permission/license failure, or infeasible optimization causes limitation, clarification, or refusal
with safe reasons.

## Deferred implementation detail

F2-E freezes Finance Domain Experience semantics and boundaries only. Pack serialization/loading,
metric catalogs, provider adapters, persistence, API resources, UI pages, formulas, tolerances,
market-data integrations, and runtime capabilities require their assigned later phases and accepted
milestone contracts.
