# IPSP Parallel Development Workflow

## Purpose

This document defines the repository-wide process for **same-version, different-module parallel development**.

IPSP is intentionally modular. Parallel development is allowed when workstreams are separated by clear module ownership, share frozen contracts, begin from the same accepted milestone baseline, and are integrated through a controlled owner-managed branch.

This workflow applies to humans and coding agents, including Codex, GitHub Copilot agents, and other repository-aware implementation tools.

## Governance model

### Final integration authority

**Kedar is the integration owner.**

Only the integration owner may:

- merge contributor work into a milestone integration branch;
- resolve cross-workstream merge conflicts;
- approve changes to shared contracts;
- approve migrations or migration ordering;
- finalize milestone integration;
- merge an accepted milestone into `main`;
- decide when a milestone acceptance audit may begin.

A contributor may:

- create or use their assigned feature branch;
- implement only the assigned workstream;
- push commits to that branch;
- open or update a PR if desired;
- report exact branch/SHA/test evidence.

A contributor must **not** merge their branch into `integration/*` or `main`.

## Branch model

```text
main
  │
  └── integration/vX.Y.Z
         │
         ├── feature/kedar/<milestone>-<workstream>
         └── feature/<contributor>/<milestone>-<workstream>
```

### `main`

`main` means **accepted milestone state only**.

Rules:

- no experimental or partial milestone work;
- no direct contributor development;
- no force-push;
- no unreviewed merge;
- milestone acceptance must pass before promotion to `main`.

### `integration/vX.Y.Z`

A temporary milestone candidate branch owned by Kedar.

Purpose:

- receives individually reviewed feature workstreams;
- is the only place where parallel modules are combined;
- owns final cross-module orchestration and integration corrections;
- runs milestone-wide tests before acceptance;
- is deleted or archived after the milestone is accepted into `main`.

### `feature/...`

One workstream per branch.

Recommended naming:

```text
feature/kedar/v0.2-dataset-versioning
feature/contributor/v0.2-ingestion-pipeline
```

A feature branch must have:

- one owner;
- one workstream ID;
- one exact base SHA;
- one merge target;
- explicit path ownership;
- explicit forbidden/shared paths;
- an acceptance gate.

## Parallel-development principle

Parallelize by **module boundary**, not by speculative dependency.

Preferred:

```text
same milestone
├── module/workstream A
└── module/workstream B
```

Avoid by default:

```text
developer A → v0.2
developer B → v0.3
```

A later-version workstream may begin early only when all of its upstream contracts are already frozen and merged into the integration baseline.

## Milestone workflow

```text
ACCEPTED MAIN
    ↓
MILESTONE SPEC
    ↓
CONTRACT FREEZE
    ↓
WORKSTREAM SPLIT
    ↓
┌────────────────────────┐
│                        │
▼                        ▼
WORKSTREAM A          WORKSTREAM B
SPEC                  SPEC
IMPLEMENT             IMPLEMENT
TEST                  TEST
DIFF                  DIFF
BRANCH GATE           BRANCH GATE
│                        │
└──────────┬─────────────┘
           ↓
  KEDAR-OWNED INTEGRATION
           ↓
  CROSS-MODULE ORCHESTRATION
           ↓
  FULL INTEGRATION TESTS
           ↓
  INDEPENDENT REVIEW
           ↓
  MILESTONE ACCEPTANCE
           ↓
          MAIN
```

## Contract freeze

Before parallel implementation begins, shared interfaces must be explicit enough that separate branches do not invent incompatible meanings.

A contract freeze may include:

- typed domain identifiers;
- Pydantic/domain contracts;
- repository interfaces;
- service interfaces;
- version/immutability semantics;
- storage references;
- error contracts;
- lifecycle/state values;
- inputs/outputs expected between workstreams.

A contract freeze is **not permission to over-design future milestones**. Freeze only what parallel branches actually need.

If a workstream discovers that a frozen shared contract must change, the agent/contributor must stop that portion of implementation and report:

```text
CONTRACT CHANGE REQUIRED
```

with:

- contract affected;
- reason;
- impact on other active workstreams;
- proposed minimal change;
- files affected.

Kedar decides whether the shared contract changes.

## Path ownership

Each workstream has three path classes.

### Owned

The workstream may change these paths without additional coordination, within its prompt/spec.

### Shared / integration-sensitive

The workstream may change these only when the workstream contract explicitly authorizes the change.

Typical integration-sensitive paths:

```text
database/migrations/**
backend/ipsp/database/models/**
backend/ipsp/api/router.py
backend/ipsp/config/providers.py
backend/ipsp/api/schemas/common.py
backend/ipsp/main.py
pyproject.toml
requirements.lock
README.md
AGENTS.md
.github/copilot-instructions.md
docs/31_IMPLEMENTATION_PROGRESS.md
docs/32_DECISION_LOG.md
docs/42_ACTIVE_WORKSTREAMS.md
```

### Forbidden

The workstream must not change these paths.

The exact list is defined in the workstream contract.

## Migration ownership

Each milestone has exactly one **Migration Owner** at a time.

Default: **Kedar** unless explicitly reassigned.

Rules:

- contributors do not create Alembic revisions unless their workstream contract explicitly assigns migration ownership;
- parallel branches must not create competing Alembic heads from the same baseline;
- ORM and migration ordering are integrated by the migration owner;
- after migration changes merge into the integration branch, other active branches synchronize before final review if they depend on that schema.

## Dependency ownership

Changes to:

```text
pyproject.toml
requirements.lock
```

require explicit Kedar approval.

A contributor/agent that believes a dependency is required must stop and report:

```text
DEPENDENCY CHANGE REQUIRED
```

with the package, reason, alternatives considered, runtime impact, and security/offline implications.

## Documentation ownership

Feature workstreams update documentation that belongs specifically to their module when requested.

The following are integration-owner documents unless explicitly assigned:

- root `README.md`;
- `docs/31_IMPLEMENTATION_PROGRESS.md`;
- `docs/32_DECISION_LOG.md`;
- `docs/42_ACTIVE_WORKSTREAMS.md`;
- milestone acceptance reports;
- repository-wide agent instructions.

This avoids concurrent status/documentation conflicts.

## Agent prompt contract

Every parallel implementation prompt must state:

```text
WORKSTREAM ID
OWNER
BRANCH
BASE SHA
MERGE TARGET
MILESTONE
DEPENDENCIES
FROZEN CONTRACTS
OWNED PATHS
SHARED / INTEGRATION-SENSITIVE PATHS
FORBIDDEN PATHS
MIGRATION OWNER
DEPENDENCY OWNER
EXPECTED INPUT INTERFACES
EXPECTED OUTPUT INTERFACES
OTHER ACTIVE WORKSTREAMS
STOP CONDITIONS
TEST GATE
FINAL REPORT FORMAT
```

Agents must not infer missing ownership.

## Synchronization rule

Before final branch review, each feature branch must be synchronized with the latest milestone integration state if another workstream has already merged and the new integration state can affect it.

Preferred policy for the human developer:

```text
git fetch origin
git rebase origin/integration/vX.Y.Z
```

or an explicit merge from the integration branch if rebase is not appropriate.

After synchronization:

- rerun relevant tests;
- rerun full required branch gate;
- provide the new exact SHA;
- review the synchronized diff before merge.

Do not treat a previously reviewed pre-rebase SHA as the final reviewed SHA.

## Review and merge sequence

For each workstream:

1. implement on assigned feature branch;
2. run branch-local quality gates;
3. push branch;
4. provide branch name + exact SHA + workstream ID + base SHA;
5. independently review the diff;
6. correct issues on the same feature branch if required;
7. synchronize with current integration branch when required;
8. rerun gates;
9. Kedar merges into `integration/vX.Y.Z`;
10. run integration tests.

When all workstreams are integrated:

1. implement only the missing cross-module orchestration;
2. run milestone-wide suite;
3. run architecture/security/anti-contamination checks;
4. perform independent integration review;
5. perform milestone acceptance audit;
6. Kedar merges accepted integration branch into `main`.

## Merge strategy

For IPSP, normal PR merge commits are preferred when practical because reviewed feature SHAs remain visible in history and the integration merge receives its own auditable SHA.

Squash/rebase merging is not prohibited, but if commit SHAs change, the post-merge integration SHA becomes the authoritative review target.

## Conflict-resolution authority

Merge conflicts are resolved by Kedar.

An agent must not automatically choose one branch's meaning over another when the conflict touches:

- shared contracts;
- ORM entities;
- migrations;
- permissions;
- security;
- API schemas;
- cross-workstream lifecycle semantics;
- dependency versions;
- architecture decisions.

Such conflicts require semantic resolution, not merely textual conflict resolution.

## Testing model

A feature branch passing tests is necessary but not sufficient.

There are three gates:

```text
BRANCH GATE
    ↓
POST-MERGE INTEGRATION GATE
    ↓
MILESTONE ACCEPTANCE GATE
```

### Branch gate

Tests the workstream and protects frozen architecture.

### Integration gate

Tests combined behavior after all merged workstreams.

### Milestone acceptance gate

Determines whether the milestone can become the new `main` baseline.

## Recommended GitHub protection

When repository permissions allow:

### `main`

- require pull request;
- prohibit force push;
- prohibit deletion;
- require CI;
- restrict direct pushes.

### `integration/*`

- Kedar-controlled merge authority;
- contributors may push only to their own feature branches;
- CI required before merge.

## Current accepted baseline

At creation of this workflow:

```text
v0.1.0 accepted baseline:
cd0dca48ded8d68f18e861f2427dfeb746d52ea7
```

Later documentation should update the active milestone/base without rewriting accepted history.

## Related documents

- [Scope Freeze](00_SCOPE_FREEZE.md)
- [Architecture](03_ARCHITECTURE.md)
- [Project Structure](04_PROJECT_STRUCTURE.md)
- [Test Strategy](29_TEST_STRATEGY.md)
- [Implementation Progress](31_IMPLEMENTATION_PROGRESS.md)
- [Decision Log](32_DECISION_LOG.md)
- [Coding Standards](34_CODING_STANDARDS.md)
- [Anti-Contamination Rules](40_ANTI_CONTAMINATION.md)
- [Active Workstreams](42_ACTIVE_WORKSTREAMS.md)
- [Workstream Contract Template](43_WORKSTREAM_CONTRACT_TEMPLATE.md)
- [Parallel Development Flow](../flows/21_PARALLEL_DEVELOPMENT.md)
