# Configuration

`ipsp.config.Settings` is the sole process-configuration source. It loads validated, non-secret
values from `IPSP_`-prefixed environment variables or a local, ignored `.env` file.

Phase 1B separates three concepts:

- runtime settings such as environment, bind address, paths, logging, and theme;
- `features`, which describe platform feature availability and never grant permission;
- `outbound`, which independently enforces Internet, remote-LLM, provider, download, update-check,
  and remote-transmission policy.

Nested settings use `__` as the environment delimiter. Canonical examples include:

```text
IPSP_FEATURES__REMOTE_LLM_ENABLED=false
IPSP_OUTBOUND__INTERNET_ENABLED=false
IPSP_OUTBOUND__REMOTE_LLM_ENABLED=false
IPSP_OUTBOUND__ALLOWED_REMOTE_PROVIDERS=[]
IPSP_OUTBOUND__DEFAULT_REMOTE_TRANSMISSION=remote_disabled
IPSP_SECRETS__PROVIDER=environment
```

The Phase 1A variables `IPSP_INTERNET_ENABLED` and `IPSP_REMOTE_LLM_ENABLED` are retired. Use the
nested canonical variables above; remote feature availability and remote outbound permission must
be configured independently.

## Secrets

Secret values are never fields on `Settings`. A safe `SecretRef` identifies provider metadata and a
specific external key, while `EnvironmentSecretProvider` resolves only that requested environment
entry into a redacted `SecretValue`. Required lookups fail closed and no fallback credential is
generated.

Environment injection is the approved production source implemented in Phase 1B. Protected OS,
vault, and cloud providers remain future implementations behind the same `SecretProvider` contract;
no unfrozen keychain or vault technology is selected here.

`.env.example` contains non-secret defaults only. Never commit a real `.env`, credential, bearer
token, cookie, or resolved secret value.
