# Configuration

Phase 1A settings are defined by `ipsp.config.Settings` and loaded from `IPSP_`-prefixed environment variables or a local `.env` file. `.env.example` contains non-secret examples only.

This folder is reserved for validated, non-secret templates. Production-critical secrets have no generated defaults and future provider credentials will be resolved through SecretProvider references rather than ordinary configuration files.
