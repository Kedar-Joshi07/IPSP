# Active Parallel Workstreams

## Purpose

This is the coordination register for active or planned parallel implementation work.

It is not an architecture specification. It records who owns each workstream, what exact SHA it started from, which branch it uses, what it may modify, what it depends on, and where it will eventually merge.

Kedar is the integration owner and final merge authority.

## Status vocabulary

```text
PLANNED
CONTRACT_FREEZE
ACTIVE
BLOCKED
READY_FOR_REVIEW
CHANGES_REQUIRED
REVIEW_PASS
MERGED_TO_INTEGRATION
INTEGRATION_VALIDATED
CLOSED
```

## Current accepted milestone

```text
Accepted version: v0.1.0
Accepted main SHA: cd0dca48ded8d68f18e861f2427dfeb746d52ea7
Next milestone: v0.2.0 — ingestion / storage / provenance
```

## Planned v0.2 workstream split

The exact start SHA for feature branches should be filled in after the v0.2 contract freeze is committed to the milestone integration branch.

| ID | Workstream | Owner | Planned branch | Merge target | Migration owner | Status |
|---|---|---|---|---|---|---|
| V0.2-A | Dataset / Version / Provenance Control Plane | Kedar | `feature/kedar/v0.2-dataset-versioning` | `integration/v0.2.0` | Kedar | PLANNED |
| V0.2-B | Secure File Ingestion / Validation / Parsing Pipeline | Contributor B | `feature/contributor/v0.2-ingestion-pipeline` | `integration/v0.2.0` | Kedar | PLANNED |

## V0.2-A — Dataset / Version / Provenance Control Plane

### Primary ownership

Expected areas:

```text
dataset logical identity
dataset version identity
dataset table metadata
provenance metadata
version immutability semantics
control-plane repositories
control-plane services
ORM/migrations assigned to Kedar
related tests
```

### Likely shared dependencies

- `docs/20_INGESTION_STORAGE_SPEC.md`
- `docs/21_SAMPLING_PROVENANCE_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- dataset/version contracts needed by V0.2-B

### Integration-sensitive paths likely owned by this workstream

```text
backend/ipsp/database/models/**
database/migrations/**
backend/ipsp/repositories/**
backend/ipsp/config/providers.py
```

Exact path ownership must be frozen in the V0.2-A prompt before implementation.

## V0.2-B — Secure File Ingestion / Validation / Parsing Pipeline

### Primary ownership

Expected areas:

```text
backend/ipsp/ingestion/**
format detection
CSV/TSV validation/parsing
XLSX validation/parsing
Parquet validation/parsing
JSON/JSONL validation/parsing
ZIP inspection
archive/path traversal defense
generated internal naming
hash/checksum support
staging/quarantine decisions
parser validation
canonicalization helpers
source-file metadata
ingestion-specific tests
```

### Default forbidden/integration-owned paths

Unless Kedar explicitly changes the workstream contract:

```text
database/migrations/**
backend/ipsp/database/models/**
backend/ipsp/api/router.py
backend/ipsp/config/providers.py
pyproject.toml
requirements.lock
README.md
AGENTS.md
.github/copilot-instructions.md
docs/31_IMPLEMENTATION_PROGRESS.md
docs/32_DECISION_LOG.md
docs/42_ACTIVE_WORKSTREAMS.md
```

### Shared contract dependency

V0.2-B must consume the frozen dataset/version/storage-reference contracts. It must not invent a competing persistence model.

If a shared contract is insufficient, report `CONTRACT CHANGE REQUIRED` and wait for Kedar's decision.

## Contract freeze checklist before both branches become ACTIVE

Fill these before implementation:

```text
integration branch:
integration/v0.2.0

integration base SHA:
<TODO>

contract freeze SHA:
<TODO>

dataset ID contract:
<TODO>

dataset version ID contract:
<TODO>

dataset table contract:
<TODO>

source/original artifact reference:
<TODO>

canonical analytical data reference:
<TODO>

hash/checksum semantics:
<TODO>

version immutability rule:
<TODO>

provenance object:
<TODO>

ingestion result contract:
<TODO>

validation/staging result contract:
<TODO>
```

## Branch handoff template

Each developer provides:

```text
Workstream:
Branch:
Base SHA:
Current SHA:
Merge target:
Files changed:
Shared files changed:
Migration files changed:
Dependency files changed:
Tests:
Quality gates:
Known deviations:
Contract changes requested:
Ready for review: YES/NO
```

## Merge authority

Contributor B pushes only to the contributor branch.

Kedar decides:

- review outcome;
- synchronization/rebase requirement;
- merge timing;
- conflict resolution;
- integration tests;
- milestone finalization;
- merge to `main`.

## Historical register

Do not delete completed rows. Move them here after the milestone is accepted so the repository retains implementation lineage.

| ID | Milestone | Final branch SHA | Integration merge SHA | Result |
|---|---|---|---|---|
| — | — | — | — | — |

## Related documents

- [Parallel Development Workflow](41_PARALLEL_DEVELOPMENT_WORKFLOW.md)
- [Workstream Contract Template](43_WORKSTREAM_CONTRACT_TEMPLATE.md)
- [Implementation Progress](31_IMPLEMENTATION_PROGRESS.md)
