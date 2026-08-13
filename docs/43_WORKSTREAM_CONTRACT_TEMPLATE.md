# IPSP Parallel Workstream Contract Template

Copy this template into the implementation prompt or workstream planning artifact for every parallel branch.

Do not begin implementation until all required fields are resolved.

---

# Workstream identity

```text
WORKSTREAM ID:
MILESTONE:
OWNER:
AGENT:
BRANCH:
BASE SHA:
MERGE TARGET:
INTEGRATION OWNER: Kedar
STATUS:
```

# Objective

Describe exactly one cohesive module/workstream outcome.

# Scope

## In scope

- ...

## Out of scope

- ...

# Dependencies

```text
UPSTREAM WORKSTREAMS:
FROZEN CONTRACT SHA:
OTHER ACTIVE WORKSTREAMS:
```

# Frozen shared contracts

List the exact contracts this workstream consumes.

For each:

```text
Contract:
Owner:
Source file/module:
Meaning:
Allowed extension:
Forbidden reinterpretation:
```

# Path ownership

## Owned paths

```text
...
```

## Shared / integration-sensitive paths

```text
...
```

Changes require explicit authorization in this workstream.

## Forbidden paths

```text
...
```

# Migration ownership

```text
MIGRATION OWNER:
ALEMBIC BASE/HEAD:
THIS WORKSTREAM MAY CREATE MIGRATIONS: YES/NO
```

If NO, the agent must not create or edit Alembic revisions.

# Dependency ownership

```text
THIS WORKSTREAM MAY MODIFY pyproject.toml: YES/NO
THIS WORKSTREAM MAY MODIFY requirements.lock: YES/NO
```

Default is NO.

# Expected input interfaces

Document the types/services/files this module receives.

# Expected output interfaces

Document the types/services/files this module produces for other modules.

# Security and privacy constraints

- ...

# Observability requirements

- ...

# Error contract

- ...

# Dataset-agnostic / anti-contamination checks

- no benchmark field names in production logic;
- no source-specific KPIs or controls;
- no benchmark-specific model choice;
- no fixed marketing assumptions;
- benchmark knowledge only in fixtures/tests/benchmark documentation.

# Stop conditions

The agent must stop and report rather than silently redesign when:

```text
CONTRACT CHANGE REQUIRED
MIGRATION OWNERSHIP REQUIRED
DEPENDENCY CHANGE REQUIRED
SHARED FILE OWNERSHIP REQUIRED
ARCHITECTURE CHANGE REQUIRED
SECURITY AUTHORITY CHANGE REQUIRED
```

# Implementation sequence

1. ...
2. ...
3. ...

# Tests

## Unit

- ...

## Integration

- ...

## Security

- ...

## Architecture / anti-contamination

- ...

# Quality gates

At minimum, as applicable:

```text
python -m compileall -q backend tests
pytest
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
```

Add Alembic checks only when relevant.

# Synchronization rule

Before final review, compare the feature branch against the latest milestone integration branch.

If the integration branch has advanced in a way that can affect this workstream:

```text
git fetch origin
git rebase origin/integration/vX.Y.Z
```

or use the explicitly selected merge policy.

After synchronization:

- rerun all required gates;
- provide the new exact SHA;
- do not reuse pre-synchronization review evidence.

# Required final report

```text
A. Workstream identity
B. Starting SHA / branch
C. Files created
D. Files modified
E. Contract usage
F. Shared-file changes
G. Migration state
H. Dependency state
I. Implementation summary
J. Security/privacy
K. Observability
L. Tests
M. Quality gates
N. Integration assumptions
O. Runtime artifacts
P. Git status
Q. Contract changes requested
R. Deviations/unresolved issues
S. Gate result
```

End with exactly one:

```text
WORKSTREAM PASS — ready for Kedar review
```

or

```text
WORKSTREAM FAIL — integration blocked
```
