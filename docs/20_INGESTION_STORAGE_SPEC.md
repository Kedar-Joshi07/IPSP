# Ingestion & Storage Specification

## Status and boundary

**Owning milestone:** v0.2.0 — Data Ingestion, Storage & Provenance

**Runtime implementation:** NOT STARTED

This specification remains compatible with F-002 but does not implement v0.2.0, create a migration,
or require later analytical/simulation/learning provenance stores during the ingestion milestone.

## Secure upload pipeline

Authorization → size/type allowlist → generated internal name → MIME/signature checks where practical
→ archive/path-traversal checks → staging/quarantine → parser validation → canonicalization →
original preservation → Parquet/metadata registration.

## Supported structured inputs

CSV/TSV, XLSX, Parquet, JSON/JSONL, and ZIP containing supported files, subject to the accepted v0.2
contract/dependency/security freeze. This list is target scope, not current implementation.

## Spreadsheet handling

A workbook may contain multiple tables/sheets, descriptions, calculations, and narrative below or
alongside data. Detect actual tabular regions; narrative/commentary is not automatically treated as
records.

## Data and control planes

Prefer an immutable original upload plus canonical processed Parquet. Keep processed views versioned
and linked to exact source dataset versions. SQLite stores control/governance/operational metadata;
source and Parquet files remain the analytical plane. SQLite is not the mandatory large analytical
warehouse.

## Multi-table behavior

Store table-level grain and relationships. Do not flatten by default. Materialized analytical views
require a validated join plan, cardinality/grain safety, time/unit/currency compatibility where
applicable, transformations, and lineage. A one-side measure is never directly aggregated after a
one-to-many join without a validated safe transformation.

## Dataset-version provenance compatibility

Each future dataset/source/table version retains stable identity, source artifact/version and
checksum, acquisition/upload actor and time, format/parser/canonicalizer versions, sampling/extraction
metadata, transformations, table/region/grain references, parent/supersession lineage, classification,
policy/retention/license references, quality/validation, and audit trace as applicable.

The identity/lineage model allows later immutable references from all F-002 provenance classes in the
[Sampling & Provenance Specification](21_SAMPLING_PROVENANCE_SPEC.md). v0.2.0 is responsible only for
provenance required by its accepted ingestion/storage contracts; it does not have to persist every
future `DOMAIN_CATALOG`, assumption, simulation, observed outcome, external evidence, LLM, synthetic,
or learning artifact prematurely.

Later milestones add their own conceptual/control-plane records and reference exact dataset versions.
They do not overload a dataset version or ordinary analytical row to collapse different provenance
authorities. Source/Parquet analytical data remains separate from SimulationLearningStore experience
and control/governance metadata.

## Integrity, policy, and lifecycle

Dataset versions are immutable once referenced; corrections create a new version. Ingestion records
permission, project/dataset policy, classification, retention, validation, safe failure, and audit/
trace context. Deletion and retention are dependency-aware and do not leave a historical result
claiming reproducibility when required data is gone.

Exact persistence schemas, routes, parsers, jobs, migrations, and dependencies arrive only through
the accepted v0.2 and later owning-milestone contracts.
