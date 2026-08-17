# Privacy & Remote LLM Policy

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** PUBLIC_WEB, APPROVED_CONNECTORS, Remote LLM, and Hybrid LLM are NOT
IMPLEMENTED in v0.1.1

This specification freezes evidence-access modes, effective permission, data minimization, and
privacy/provenance requirements for LLM, retrieval, memory, and learning artifacts. It does not
enable Internet access, connectors, remote providers, or model downloads.

## Data classification

Policy supports at least:

- ordinary business data;
- direct identifier;
- quasi-identifier;
- financial/sensitive;
- sensitive demographic;
- confidential/restricted dataset classification.

Classification applies to source values, source/semantic names, derived profiles, aggregates,
examples, prompts, retrieved evidence, model responses, logs, memory, training events, embeddings or
indexes, adapted weights, and exports. Derived or de-identified material is re-evaluated for
re-identification and inference risk.

## Exact evidence-access modes

The complete set of evidence-access modes is exactly:

- `OFF`
- `INTERNAL_ONLY`
- `PUBLIC_WEB`
- `APPROVED_CONNECTORS`

`OFF` disables optional evidence retrieval beyond the already authorized inputs attached to the
current operation. `INTERNAL_ONLY` permits only authorized IPSP/project/organization sources and
local knowledge that pass scope, provenance, privacy, license, freshness, and retention checks.
`PUBLIC_WEB` permits governed retrieval from public-web sources allowed by policy. `APPROVED_CONNECTORS`
permits only explicitly registered and approved connectors, destinations, scopes, credentials, and
source classes.

These modes govern evidence retrieval and are independent from the four LLM modes. For example, a
Local LLM does not automatically gain internal retrieval, and a remote provider does not automatically
gain PUBLIC_WEB or connector access. PUBLIC_WEB and APPROVED_CONNECTORS are architecture contracts,
not v0.1.1 implementation claims.

## Effective permission

Effective permission is exactly:

```text
Admin policy ∩ project/dataset policy ∩ runtime user consent
```

Every component must allow the specific operation, source/destination, purpose, data classes,
fields/payload, provider/connector, and time/scope. The intersection can only narrow access. Silence,
missing state, stale/expired consent, or ambiguity fails closed. Runtime consent is captured as a
versioned snapshot with actor, purpose, scope, disclosures, expiry/withdrawal state, and policy
references; it is not a substitute for Admin or project/dataset permission.

Revocation stops new access and follows retention/deletion policy for previously materialized
artifacts. It does not rewrite an historical audit record or falsely claim that an earlier authorized
access did not occur.

## Remote transmission default and tiers

Raw dataset rows are not sent remotely by default. Admin policy may define increasingly permissive
transmission profiles such as:

1. remote disabled;
2. sanitized schema only;
3. original column names but no values;
4. sanitized aggregate statistics or anonymized examples;
5. explicitly approved sample rows.

The least-disclosing eligible profile is used. Restricted datasets default to local-only processing
unless Admin, project/dataset policy, and runtime consent all explicitly permit the exact remote use.
No profile authorizes millions of rows, unrestricted fields, or reuse for provider training.

## Column, row, and artifact policy

A field may be allowed, masked, transformed, aggregated, or denied independently for view, modelling,
retrieval, prompt/tool use, memory, training, export, and remote transmission. Row/population and
purpose restrictions also apply. A user's permission to view a result does not imply permission to
send its inputs, explanations, evidence, or lineage to an LLM or connector.

Outbound packets are built from allowlisted fields, minimized, size-bounded, scanned for secrets and
sensitive leakage, and recorded by stable references/checksums rather than indiscriminately copied to
logs. Provider responses receive the same classification and policy enforcement as inputs.

## Sensitive-feature and quasi-identifier governance

Models involving people support feature exclusion, declared sensitive attributes, segment-performance
checks, and basic proxy/correlation warnings. Remote explanation or training does not waive fairness,
purpose, or adverse-decision constraints.

Removing a direct identifier does not automatically anonymize a row. Combinations of geography,
age, financial/property, event-time, organizational, or other quasi-identifiers may identify or
narrow individuals. Sanitization evaluates combinations, small groups, uniqueness, linkability, and
context rather than applying name-only redaction.

## Retrieval and memory privacy

Each retrievable item and index/embedding entry retains source/version, provenance, classification,
permitted purpose/scope, consent/policy, license, freshness/validity, retention/deletion, and access
control. Query-time filtering occurs before retrieval results reach an LLM. Retrieved material cannot
cross project/dataset/organization boundaries merely because vector similarity is high.

Memory stores confirmed facts, governed decisions, or proposals with their original authority class.
It excludes secrets and denied payloads, honors correction/supersession/deletion, and does not turn a
prior simulation, LLM proposal, external claim, or synthetic record into observed truth.

## Learning and adaptation artifacts

Training-event candidates, datasets, evaluation sets, embeddings/indexes, prompts/responses, and
PEFT/LoRA artifacts preserve:

- source provenance and immutable source/version references;
- privacy/sensitivity classification and de-identification transformations;
- effective Admin, project/dataset, and runtime-consent snapshots plus purpose and retention;
- source-data, evidence, dependency, and model-weight/adapter license decisions;
- training/evaluation snapshot, builder/configuration/code versions, exclusions, and checksums;
- evaluation results, limitations, Trust/promotion decision, owner, and audit lineage.

Content is eligible for adaptation only when its original collection/use permissions and licenses
cover that purpose. Withdrawal, correction, expiry, or policy change produces a governed remediation
decision; weights are never claimed to forget data without verified evidence.

## Provider and external-evidence boundary

Remote providers, public sites, and connectors are individually registered and policy-scoped. Their
terms, training/retention behavior, region, security, authentication, rate/resource limits, evidence
licenses, and model-weight/dependency licenses are evaluated independently. An approved provider does
not approve every model, source, connector, or payload.

Public availability does not establish accuracy, legal reuse, or permission to train. Retrieved
content remains `EXTERNAL_EVIDENCE` or another applicable provenance class and must pass evidence,
schema, deterministic, and Trust checks. LLM output remains `LLM_PROPOSAL` until separately validated.

## Enforcement, refusal, and audit

Backend policy enforcement occurs before retrieval, tool access, packet construction, transmission,
retention, training-dataset inclusion, and artifact promotion. A denial produces a safe reason and
audit/trace reference without revealing a secret or inaccessible source. UI state, prompt instruction,
provider capability, or user intent never overrides policy.

Audit records include actor/purpose, requested/effective modes, policy/consent versions, source and
destination/provider/connector references, payload classification and minimization profile, allow/
deny reason, artifact references, validation, timestamps, and trace ID. Ordinary logs do not contain
raw sensitive payloads, credentials, or model secrets.

## Deferred implementation detail

Exact policy schemas, consent APIs/UI, sanitizers, classifiers, connector/provider registry,
retrieval/index implementation, deletion workflows, and remote execution require later contract
freezes and accepted milestones. No Internet connection is required by this contract.
