# LLM Architecture

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.13.0 — Local AI

This specification freezes provider-neutral LLM responsibilities, exact operating modes, Local AI
registry metadata, and the governed learning boundary. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and does not install an LLM package,
download a model, create a runtime provider, or require Internet access.

## Authority boundary

ML, statistical, deterministic, metric, accounting, simulation, and optimization services retain
numerical authority. Dataset Semantic Manifests, registries, deterministic validators, permissions,
policy, Trust, and human confirmation retain their respective approval authority.

An LLM may interpret, propose, rank, plan, clarify, retrieve, or explain. Its text, confidence,
probability, tool call, retrieved passage, or adapted weights never become numerical truth, confirmed
semantics, causal evidence, license approval, Trust approval, or empirical observation without the
separate authoritative validation and governance path.

## Exact LLM modes

The complete set of LLM modes is exactly:

- `ML_ONLY`
- `LOCAL_LLM`
- `REMOTE_LLM`
- `HYBRID_LLM`

`ML_ONLY` uses deterministic/ML services and does not invoke an LLM. `LOCAL_LLM` permits only an
eligible local provider. `REMOTE_LLM` permits an eligible remote provider only after privacy,
outbound, evidence-access, consent, secret, provider, and license gates pass. `HYBRID_LLM` permits a
governed plan across eligible local and remote providers while preserving each provider's payload,
policy, provenance, and validation boundary.

The selected mode does not itself authorize a provider or evidence source. Missing eligibility
limits, disables, or refuses the LLM-assisted path; there is no silent fallback to another mode.
Remote or Hybrid LLM execution is not required for v1.0.

## Provider-neutral interface

Application services depend on a typed semantic-assistance interface rather than vendor APIs.
Conceptual provider roles may include null/ML-only, local, remote, and hybrid adapters. Every request
and response is schema-versioned and records the selected mode, task, provider/model versions,
policy/consent and evidence-access snapshots, input provenance, tool use, validation, limitations,
and audit/trace reference.

Provider examples are architecture candidates, not installed or approved runtimes. Engine/provider
availability and deterministic selection are governed by the
[Engine & License Registry Specification](48_ENGINE_LICENSE_REGISTRY_SPEC.md).

## Allowed assistance responsibilities

Subject to evidence, schema, permission, and policy validation, LLM assistance may support:

- schema and semantic candidate interpretation plus targeted clarification questions;
- Domain Experience reasoning over activated versioned pack metadata without hardcoding domain logic
  into IPSP Core;
- relationship, objective, capability, metric, control, constraint, and assumption proposals;
- intent parsing into a **draft** `ScenarioIntentManifest` that requires deterministic validation and
  confirmation before it becomes frozen authority;
- analog or benchmark candidate ranking using applicability, provenance, population, period, units,
  license, freshness, and support evidence;
- evidence planning that identifies gaps, eligible access modes, queries/tools, validation needs, and
  refusal conditions without treating retrieval as proof;
- scenario, graph, Trust, Evidence Profile, uncertainty, limitation, refusal, and result explanation
  grounded in immutable structured facts;
- governed memory/retrieval and organization terminology assistance;
- optional curated training-event preparation and PEFT/LoRA challenger proposals.

An LLM cannot invent a CrossDomainSemanticGraph or CompositeSimulationGraph edge, formula, metric
value, exchange rate, observed outcome, causal relation, constraint exception, or unsupported
capability to satisfy a request.

## Dataset Intelligence Packet and data minimization

An LLM receives the minimum authorized structured context needed for its task. A compact Dataset
Intelligence Packet may contain descriptions, semantic IDs, types, deterministic profiles,
cardinality, approved minimal examples, associations, candidate grain/relationships/targets/controls,
conflicts, provenance, and limitations.

Millions of rows are never sent to an LLM. Raw dataset rows are not sent to a remote LLM by default.
Field names, examples, aggregates, retrieved evidence, and prior memory are individually subject to
classification, minimization, masking, outbound, consent, license, and retention policy.

## Structured output and deterministic validation

Operational output uses strict versioned schemas, such as Pydantic contracts. Prose is allowed for
human-facing explanation only after the underlying structured facts and citations/references exist.
Validation covers schema/type, semantic/evidence consistency, tool-result grounding, provenance,
policy, conflicts, unsupported claims, and required confirmation. Invalid output is rejected or
repaired through a bounded governed process; it is never silently accepted.

## Constrained evidence tools

An eligible LLM may request allowlisted, typed tools such as column/profile summaries, category
distribution, correlation or mutual information, functional dependency, time/missingness patterns,
metric formula validation, candidate target/control lookup, registry lookup, internal retrieval, or
approved evidence retrieval. Tools enforce authorization independently and return structured,
provenance-bearing results. The LLM cannot expand evidence access, call arbitrary code, or bypass a
denied tool.

## Memory and retrieval

Retrieval/memory is preferred over weight adaptation. Eligible memory may include confirmed semantic
decisions, organization vocabulary/configuration, curated Domain Experience material, validated
metric/relationship knowledge, prior IPSP learning events, and authorized evidence. Each item retains
source/version, provenance class, privacy classification, consent/policy, license, validity/freshness,
scope, and supersession/deletion state.

Retrieval is filtered by current actor, project/dataset, purpose, evidence-access mode, consent,
privacy, outbound, retention, and license policy. Retrieved content remains evidence, context, or a
proposal according to its provenance; retrieval does not elevate authority. Conflicting or stale
memory is surfaced and cannot silently override a higher-precedence confirmed source.

## Local LLM registry metadata and model-weight license gate

An eligible Local LLM registry record conceptually includes:

- stable model/provider/adapter identity and versions, artifact format, checksum, source, and
  provenance;
- base model and optional adapter identities, architecture/context/token limits, structured-output
  and tool capabilities, quantization, determinism/seed behavior, and compatibility;
- runtime/library versions, loadability/health facts, CPU/GPU/memory/disk/resource requirements, and
  isolation/security metadata;
- data locality, payload and logging behavior, privacy classification eligibility, retention, and
  outbound behavior;
- independent dependency, base-model-weight, tokenizer, adapter, and bundled-resource license
  references plus approved-use decisions;
- training/adaptation snapshot and configuration where applicable, evaluation evidence, Trust,
  limitations, owner/approval, and audit history.

Model-weight and dependency licenses are independent mandatory gates. Missing, unknown, conflicting,
expired, or incompatible terms block use. A model file being present or loadable never proves that it
is licensed, secure, eligible, or validated.

## Governed Local AI adaptation

The preferred order is exactly:

1. retrieval and memory;
2. curated training-event preparation;
3. optional PEFT/LoRA challenger;
4. evaluation;
5. promotion or rejection.

Training events are built only through a governed eligibility and dataset-building process. They
preserve source provenance, privacy classification, consent/policy snapshot, purpose, model-weight
and source-data licenses, training snapshot/version, transformations, exclusions, evaluation, and
audit lineage. Secrets, denied content, raw restricted rows, simulated output presented as truth,
and unverified proposals are excluded.

An optional PEFT/LoRA artifact is a challenger, not an automatic replacement. Evaluation covers task
quality, structured-output validity, grounding, privacy/security, memorization/data leakage,
robustness, regression, bias/segment behavior where applicable, latency/resources, license, and
reproducibility. Promotion/rejection is explicit and versioned. Fine-tuning never grants numerical,
semantic, evidence, causal, Trust, or policy authority.

Continuous governed retrieval and memory are sufficient for the bounded v1.0 architecture; automatic
fine-tuning is not a v1.0 requirement.

## Privacy, provenance, and reproducibility

Every prompt/input packet, retrieved item, tool result, structured response, explanation, memory
item, training example, and adapted artifact retains the applicable source provenance, privacy
classification, consent/effective policy, license references, versions, validation/evaluation, and
audit/trace linkage. Credential values and secrets are never embedded in these artifacts.

Reproduction resolves exact provider/model/adapter/runtime versions, model-weight/dependency license
decisions, prompt/schema/tool versions, evidence and memory snapshots, policy/consent context,
non-secret configuration, seeds where meaningful, structured output, and validation evidence. An
unavailable historical provider is reported honestly and never silently substituted.

## Deferred implementation detail

Exact provider APIs, prompts, schemas, tool catalogs, registries, vector/index storage, retrieval
ranking, memory lifecycle, model download, inference runtime, PEFT/LoRA pipeline, evaluation suite,
and UI require later contract freezes and accepted milestones.
