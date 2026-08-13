# Flow 21 — Parallel Development

```mermaid
flowchart TD
    MAIN[Accepted main milestone] --> INT[Create milestone integration branch]
    INT --> CF[Freeze shared contracts]
    CF --> A[Workstream A feature branch]
    CF --> B[Workstream B feature branch]

    A --> AT[Branch-local tests]
    B --> BT[Branch-local tests]

    AT --> AR[Independent branch review]
    BT --> BR[Independent branch review]

    AR -->|PASS| AM[Kedar merges A]
    BR -->|PASS| BM[Kedar merges B]

    AM --> IM[Milestone integration branch]
    BM --> IM

    IM --> ORCH[Cross-module orchestration]
    ORCH --> IT[Integration + security + architecture tests]
    IT --> IR[Independent integration review]
    IR --> AUD[Milestone acceptance audit]

    AUD -->|PASS| PROMOTE[Kedar merges accepted milestone to main]
    AUD -->|FAIL| FIX[Focused correction workstream]
    FIX --> IM
```

## Authority

- Contributors push only to their assigned feature branches.
- Kedar owns merges, conflict resolution, integration ordering, milestone finalization, and promotion to `main`.
- `main` contains accepted milestone states only.

See [Parallel Development Workflow](../docs/41_PARALLEL_DEVELOPMENT_WORKFLOW.md).
