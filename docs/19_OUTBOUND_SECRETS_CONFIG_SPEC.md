# Outbound Access, Secrets & Configuration

## Outbound Access Policy Manager
Backend-enforced controls:
- global internet on/off
- remote LLM on/off
- allowed providers
- model download/update check permission
- dataset/project remote-transmission policy

UI state alone is never enforcement.

## SecretProvider
SQLite stores provider metadata and secret references, not ordinary plaintext API keys. Define a `SecretProvider` abstraction from v0.1.0 for local protected storage and future vault/cloud providers.

Required production secrets must be stable and supplied through `SecretProvider`, environment injection, or protected operating-system storage. Production startup fails closed when a required secret is absent; it never silently generates a replacement. Any development bootstrap is explicit and development-only. Secrets are never written to ordinary SQLite fields or logs.

## AI configuration
Local provider: endpoint/runtime/model/context/timeout/structured-output/health.  
Remote provider: provider/model/credential ref/token budget/timeout/data policy/fallback.

## Feature flags
Examples: `local_llm_enabled`, `remote_llm_enabled`, `sdv_enabled`, `optimization_enabled`, `causal_engine_enabled`, `experimental_rag_enabled`.
