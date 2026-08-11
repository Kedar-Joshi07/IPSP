# Flow 14 — Reporting / Export
```mermaid
flowchart TD
  RUN[Persisted Run Result Object] --> PERM[Export/column policy]
  PERM --> PDF[PDF generator]
  PERM --> XLSX[Excel generator]
  PDF --> ART[Versioned report artifact]
  XLSX --> ART
  ART --> AUD[Audit/export log]
```
