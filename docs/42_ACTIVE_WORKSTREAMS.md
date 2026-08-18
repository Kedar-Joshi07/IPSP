# Active Parallel Workstreams

## Purpose and authority

This is the coordination register for active or planned parallel implementation work. It is not an
architecture specification or implementation authorization. The
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and
[Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md)
govern architecture and sequencing. Kedar is the integration owner and final merge authority.

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

## Current state

```text
Accepted application: v0.1.0
Accepted foundation code baseline SHA: cd0dca48ded8d68f18e861f2427dfeb746d52ea7
Active milestone: v0.1.1 — F-002 Architecture Reconciliation
Accepted F2-G input SHA: 0c621a9f70d5568d36a13193f8f14b96c6bd79ff
Current work package: F2-H — documentation/governance reconciliation
Current work-package state: COMPLETE — independent review pending
Next work package: F2-I — NOT AUTHORIZED before independent F2-H PASS
Following capability milestone: v0.2.0 — NOT STARTED
v0.2 contract-freeze state: NOT STARTED
```

No parallel capability implementation workstream is `ACTIVE`. F2-H is documentation/governance-only.
F2-I may reconcile only the minimal v0.1.1 production compatibility surface after F2-H is accepted.
Only F2-J acceptance can complete v0.1.1; v0.2 contract-freeze preparation requires the subsequent
explicit authorization described by the roadmap.

## Current register

| ID | Milestone | Owner | Exact base SHA | Merge target | Scope | Status |
|---|---|---|---|---|---|---|
| F2-H | v0.1.1 | Kedar / Codex work package | `0c621a9f70d5568d36a13193f8f14b96c6bd79ff` | `main` after review by Kedar | Flows, tests, acceptance, governance, instructions | READY_FOR_REVIEW |
| F2-I | v0.1.1 | To be assigned | Accepted F2-H SHA | To be frozen | Minimal production reconciliation only | PLANNED — BLOCKED BY F2-H REVIEW |
| F2-J | v0.1.1 | Independent reviewer | Accepted F2-I SHA | `main` acceptance baseline | Independent final acceptance audit | PLANNED — BLOCKED BY F2-I |

## Future milestone rule

The frozen pre-v1.0 sequence is v0.2.0 through v0.15.0 and then v1.0.0 as defined in the roadmap.
Before any future milestone changes from `NOT STARTED` to `CONTRACT_FREEZE`, the integration owner
must create a new milestone contract that records:

- exact base SHA, owner, branch, and merge target;
- owned, shared/integration-sensitive, and forbidden paths;
- functional contract;
- data/schema contract;
- API/interface contract;
- acceptance contract;
- dependency/license contract;
- migration owner and dependency owner;
- stop conditions;
- branch gate, post-merge integration gate, and milestone acceptance gate.

Only after those contracts are accepted may concrete same-version/different-module workstreams become
`ACTIVE`.

## Superseded v0.2 candidate split

Before F-002, this register listed `V0.2-A` dataset/version/provenance and `V0.2-B` secure-ingestion
candidate workstreams. They were `PLANNED`; their contract freeze never started, and no branch was
authorized. F-002 replaced the old roadmap authority. Those labels, owners, paths, and incomplete
contract checklist are historical planning only and must not be copied into a new v0.2 contract
without fresh review against accepted v0.1.1 and the frozen v0.2 milestone scope.

## Branch handoff

Every workstream reports:

```text
Workstream:
Owner:
Branch:
Base SHA:
Current SHA:
Merge target:
Owned paths:
Shared files changed:
Forbidden-path check:
Functional contract:
Data/schema contract:
API/interface contract:
Acceptance contract:
Dependency/license contract:
Migration state and owner:
Dependency state and owner:
Tests and branch gate:
Post-merge gate responsibility:
Milestone acceptance gate responsibility:
Known deviations:
Contract changes requested:
Ready for review: YES/NO
```

Contributors push only to assigned feature branches. Kedar owns synchronization, merge timing,
conflict resolution, integration tests, milestone finalization, and promotion to `main`.

## Historical register

Completed workstreams are retained here after milestone acceptance.

| ID | Milestone | Final branch SHA | Integration merge SHA | Result |
|---|---|---|---|---|
| — | — | — | — | — |

## Related documents

- [Parallel Development Workflow](41_PARALLEL_DEVELOPMENT_WORKFLOW.md)
- [Workstream Contract Template](43_WORKSTREAM_CONTRACT_TEMPLATE.md)
- [Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md)
- [Implementation Progress](31_IMPLEMENTATION_PROGRESS.md)
