---
applyTo: "backend/**/{auth,security,api,storage,reports,observability}/**/*.py"
---
# Security Instructions

- Argon2id password hashing; never plaintext or reversible password storage.
- Server-side authenticated sessions; secure cookie flags; CSRF protection for state-changing browser requests.
- Enforce permissions server-side on every protected operation.
- Enforce dataset and column policies on view/export/model/remote transmission.
- Remote access is backend-policy controlled, not merely hidden in UI.
- Effective evidence/provider access is Admin policy ∩ project/dataset policy ∩ runtime user consent;
  evidence-access and consent snapshots are versioned for audit and reproduction.
- Secrets are referenced through `SecretProvider`; do not store ordinary plaintext API keys in SQLite.
- Redact credentials, auth headers, sensitive records, and raw secret-bearing prompts from logs.
- Dependency, provider, solver, dataset/evidence, and model-weight licenses are separate gates;
  unavailable or unknown approval fails closed without an ungoverned fallback.
