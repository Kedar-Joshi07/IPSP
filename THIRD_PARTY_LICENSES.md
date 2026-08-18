# Third-Party License Inventory

IPSP project code is proprietary as stated in [LICENSE](LICENSE). The packages below are the exact
Python environment snapshot recorded in `requirements.lock`; they are not relicensed by IPSP.
License identifiers are taken from installed package metadata and upstream project declarations.
The upstream license text and notices remain authoritative, and redistributable builds must retain
all notices required by those licenses.

This is a current inventory, not approval or installation of any F-002 candidate engine, model,
solver, synthetic-data provider, or AI dependency.

| Package | Locked version | Declared license |
|---|---|---|
| alembic | 1.19.1 | MIT |
| annotated-doc | 0.0.5 | MIT |
| annotated-types | 0.8.0 | MIT |
| anyio | 4.14.2 | MIT |
| argon2-cffi | 25.1.0 | MIT |
| argon2-cffi-bindings | 25.1.0 | MIT |
| ast_serialize | 0.8.0 | MIT |
| cffi | 2.1.1 | MIT-0 |
| click | 8.4.2 | BSD-3-Clause |
| colorama | 0.4.6 | BSD-3-Clause |
| fastapi | 0.139.2 | MIT |
| greenlet | 3.5.5 | MIT AND PSF-2.0 |
| h11 | 0.16.0 | MIT |
| httpcore2 | 2.7.0 | BSD-3-Clause |
| httpx2 | 2.7.0 | BSD-3-Clause |
| idna | 3.18 | BSD-3-Clause |
| iniconfig | 2.3.0 | MIT |
| librt | 0.15.0 | MIT |
| Mako | 1.4.1 | MIT |
| MarkupSafe | 3.0.3 | BSD-3-Clause |
| mypy | 2.3.0 | MIT |
| mypy_extensions | 1.1.0 | MIT |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause |
| pathspec | 1.1.1 | MPL-2.0 |
| pluggy | 1.6.0 | MIT |
| pwdlib | 0.3.0 | MIT |
| pycparser | 3.0 | BSD-3-Clause |
| pydantic | 2.13.4 | MIT |
| pydantic-settings | 2.15.0 | MIT |
| pydantic_core | 2.46.4 | MIT |
| Pygments | 2.20.0 | BSD-2-Clause |
| pytest | 9.1.1 | MIT |
| python-dotenv | 1.2.2 | BSD-3-Clause |
| ruff | 0.15.22 | MIT |
| setuptools | 84.0.0 | MIT |
| SQLAlchemy | 2.0.51 | MIT |
| starlette | 1.6.0 | BSD-3-Clause |
| truststore | 0.10.4 | MIT |
| typing-inspection | 0.4.3 | MIT |
| typing_extensions | 4.16.0 | PSF-2.0 |
| uvicorn | 0.51.0 | BSD-3-Clause |

The GitHub Actions workflow also invokes `actions/checkout@v4` and `actions/setup-python@v5`, both
published under the MIT License. Those automation actions are CI tooling, not IPSP runtime or
Python-package dependencies.

## Governance

- Update this file whenever `requirements.lock` changes.
- Review the exact dependency, transitive dependency, model-weight, dataset/evidence, solver, and
  hosted-service licenses independently; approval in one category does not approve another.
- Do not infer runtime availability from an architecture candidate list or this inventory.
- Unknown, incompatible, or unreviewed mandatory license facts fail closed for provider selection.
