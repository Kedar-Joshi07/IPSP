# IPSP v1.0 — Phase 0 Implementation Plan

**Status**: Phase 0.5 reconciliation complete; corrected plan approved for Phase 1. No production code written.  
**Phase Goal**: Produce concrete architecture blueprint and module/dependency plan for v0.1.0 foundation.  
**Gate**: Plan aligns with locked decisions; no architecture drift; no benchmark contamination; clear violation checks identified.

---

## Executive Summary

IPSP is a **local-first, dataset-agnostic predictive simulation platform** for structured business data. Phase 0 establishes:

1. **Architecture verification** against locked decisions (AGENTS.md, copilot-instructions.md, 00_SCOPE_FREEZE.md)
2. **Module/dependency blueprint** for v0.1.0 (security, configuration, foundation)
3. **Explicit violation checklist** for dataset agnosticism, LLM boundaries, trust validation, RBAC, storage separation
4. **Design system anchor** from canonical reference HTML
5. **Test strategy** for foundation layers

No production code is written in Phase 0. This plan gates Phase 1.

---

## Part A: Architecture Verification

### Locked Decisions Confirmed ✓

| Decision | Rationale | Planned Phase 1 enforcement |
|---|---|---|
| **D-001**: Dataset-agnostic core | IPSP adapts to *any* dataset, not hardcoded domain | No `campaign`, `funnel_stage`, `ROAS`, `budget` fields in core schema; benchmark fixtures only |
| **D-002**: Canonical visual reference | HTML provides design language, not demo business logic | CSS/typography/layout extracted; hardcoded campaign values explicitly removed from production path |
| **D-003**: FastAPI + vanilla JS | No Streamlit; portable backend | FastAPI app factory; no Streamlit imports; vanilla HTML/CSS/Plotly.js |
| **D-004**: SQLite control + Parquet data | Metadata in SQLite; analytical data in files | Schema separates: `users`, `datasets`, `semantic_manifests` (SQLite) from raw/processed data (Parquet/files) |
| **D-005**: Optional LLMs | Full ML-only operation required | `SemanticLLMProvider` interface with `NullLLMProvider` default; no LLM calls required for core flows |
| **D-006**: Trust engine first-class | Every model/simulation independently validated | `TrustValidator` service; runs must pass before display; cannot skip for "obvious" cases |
| **D-007**: Predictive ≠ causal | Observational data cannot claim causality | Language guards in simulation/explainability; "prediction", "association", never "causes", "drives" without causal support |
| **D-008**: Version everything | Reproducibility requires versioning | Dataset version, semantic version, model version, seed tracked in Run Result Object |
| **D-009**: Multi-table v1.0 | Relationships inferred/confirmed, not flattened by default | `relationship_candidates`, `join_validation` tables; no auto-flatten logic in Phase 1-3 |
| **D-010**: Sampling provenance v1.0 | 500-row samples ≠ full-population sufficiency | Sampling metadata distinguishes source population from actual training data; training sample size remains a model-validation input |
| **D-011**: Measurement-unit-aware journey | Ordered journeys not auto-monotonic | Lineage tracks units; journey validation checks measurement consistency, not strict funnel |
| **D-012**: Sensitive feature/remote policy | Column sensitivity + transmission policy explicit | `column_policies` table; `OutboundPolicy` enforced; remote calls blocked by default |
| **D-013**: No universal non-negative rule | Only intrinsic/confirmed constraints hard-block values | Negative values are invalid only under intrinsic or confirmed rules, anomalous only with evidence, and otherwise valid observations |

### Cross-Cutting Architecture Layers ✓

```
┌─────────────────────────────────────────────────────────────────┐
│ HTML/CSS/JS (metadata-driven, no hardcoding)                    │
├─────────────────────────────────────────────────────────────────┤
│ FastAPI Router Layer (thin: validation, auth, response mapping) │
├────────────────────────────────────────────────────────────────┤
│ Auth/RBAC Layer (server-side policy enforcement)               │
├────────────────────────────────────────────────────────────────┤
│ Observability/Logging (trace IDs, audit, no secrets)          │
├────────────────────────────────────────────────────────────────┤
│ Application Services (business logic; repositories injected)   │
├────────────────────────────────────────────────────────────────┤
│ Domain Services (data understanding, semantic, capability...)  │
├────────────────────────────────────────────────────────────────┤
│ Repositories (SQLAlchemy models; portable to PostgreSQL)       │
├────────────────────────────────────────────────────────────────┤
│ Storage Planes:                                                 │
│  - SQLite (control: users, datasets, manifests, runs)         │
│  - Parquet/files (analytical: originals, processed views)      │
├────────────────────────────────────────────────────────────────┤
│ Provider Abstractions (LLM, storage, secrets, outbound policy) │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part B: Module Blueprint for v0.1.0

### Directory Structure

```
ipsp/
├── frontend/
│   ├── index.html                  (modular, no hardcoded domain content)
│   ├── css/
│   │   ├── base.css               (reset + typography + grid)
│   │   ├── components.css         (cards, buttons, form controls)
│   │   ├── tokens.css             (shared semantic design tokens)
│   │   └── themes.css             (complete dark/light tokens + switch support)
│   ├── js/
│   │   ├── app.js                 (router, session, error handling)
│   │   └── api.js                 (REST client, auth headers)
│   └── assets/
│       ├── icons/
│       └── vendor/                (pinned browser assets + version/license inventory)
│
├── backend/ipsp/
│   ├── __init__.py
│   ├── main.py                    (FastAPI app factory)
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── service.py             (login, logout, session mgmt)
│   │   ├── password.py            (Argon2id, pepper handling)
│   │   └── rbac.py                (permission checking)
│   │
│   ├── security/
│   │   ├── __init__.py
│   │   ├── csrf.py                (CSRF token generation/validation)
│   │   ├── policy.py              (OutboundPolicy, SecretProvider interfaces)
│   │   └── redactor.py            (log sanitization)
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            (Pydantic settings from env)
│   │   ├── feature_flags.py       (runtime feature control)
│   │   └── providers.py           (provider registry: LLM, storage, etc.)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── engine.py              (SQLAlchemy engine/session factory)
│   │   └── models/                (sole SQLAlchemy ORM ownership)
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                (BaseRepository mixin)
│   │   ├── users.py               (UserRepository)
│   │   ├── roles.py               (RoleRepository)
│   │   ├── datasets.py            (DatasetRepository)
│   │   └── audit.py               (AuditEventRepository)
│   │
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logging.py             (structured logging, trace ID context)
│   │   ├── audit.py               (audit event recording)
│   │   └── errors.py              (error taxonomy, safe responses)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── project.py             (ProjectService — Phase 2+)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routers.py             (router registration)
│   │   ├── schemas/               (Pydantic request/response contracts)
│   │   └── routes/                (sole thin FastAPI route ownership)
│   │
│   ├── ingestion/                 (Phase 2)
│   ├── profiling/                 (Phase 3)
│   ├── semantics/                 (Phase 4)
│   ├── relationships/             (Phase 3)
│   ├── capabilities/              (Phase 5)
│   ├── llm/                       (Phase 8)
│   ├── models/                    (Phase 5)
│   ├── simulation/                (Phase 6)
│   ├── trust/                     (Phase 6)
│   ├── reports/                   (Phase 6)
│   ├── jobs/                      (foundation contracts; worker later)
│   │
│   └── cli/
│       ├── __init__.py
│       └── admin.py               (admin bootstrap, database init)
│
├── tests/
│   ├── conftest.py                (pytest fixtures)
│   ├── unit/
│   │   ├── test_auth.py
│   │   ├── test_config.py
│   │   ├── test_rbac.py
│   │   ├── test_errors.py
│   │   └── test_logging.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   ├── test_migrations.py
│   │   └── test_session.py
│   └── security/
│       ├── test_password.py
│       ├── test_csrf.py
│       ├── test_policy.py
│       └── test_secrets.py
│
├── database/
│   └── migrations/                (Alembic history)
│
├── config/
│   ├── .env.example
│   ├── .env.local                 (local dev, .gitignored)
│   └── settings-prod.yml          (example production config)
│
├── scripts/
│   ├── create_admin.py            (CLI: bootstrap admin user)
│   ├── init_db.py                 (CLI: init SQLite from migrations)
│   └── seed_fixtures.py           (optional: benchmark test data)
│
├── pyproject.toml                 (dependencies, metadata)
├── requirements-dev.txt           (test, lint, debug deps)
├── pytest.ini                     (test config)
├── .gitignore
└── README.md
```

### Dependency Policy (Phase 1 / v0.1.0)

- Resolve current maintained compatible versions at implementation time.
- Declare direct runtime and development dependencies in `pyproject.toml`; generate a reproducible lock or constraints artifact.
- Use FastAPI, Uvicorn, Pydantic, SQLAlchemy 2.x, Alembic, `pwdlib[argon2]`, the configured structured-logging library, pytest, and the agreed quality tools as direct needs require.
- `sqlite3` comes from the Python standard library and is not a package dependency.
- Ordinary browser login uses opaque server-side sessions, not JWT/python-jose.
- New Argon2id hashes have no bcrypt fallback unless legacy-hash migration is separately approved.
- Browser assets such as Plotly.js are pinned and vendored under `frontend/assets/vendor/`, with version/license inventory and no production public-CDN dependency.

---

## Part C: Proposed Modules & Key Classes

### Phase 1 / v0.1.0 Minimum Viable Foundation

#### 1. Auth & Security

```python
# backend/ipsp/database/models/security.py (canonical ORM ownership)
class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, unique=True, nullable=False)
    display_name: str = Column(String, nullable=False)
    email: Optional[str] = Column(String, unique=True, nullable=True)
    password_hash: str = Column(String, nullable=False)
    role_id: int = Column(ForeignKey("roles.id"), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    must_change_password: bool = Column(Boolean, default=True)
    failed_login_count: int = Column(Integer, default=0)
    locked_until: Optional[datetime] = Column(DateTime(timezone=True))
    last_login_at: Optional[datetime] = Column(DateTime(timezone=True))
    password_changed_at: datetime = Column(DateTime(timezone=True))
    created_at: datetime = Column(DateTime(timezone=True))
    created_by: Optional[int] = Column(ForeignKey("users.id"))
    updated_at: datetime = Column(DateTime(timezone=True))
    
class Role(Base):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True)  # e.g., "admin", "user"
    description: str = Column(String)
    
class Permission(Base):
    __tablename__ = "permissions"
    id: int = Column(Integer, primary_key=True)
    code: str = Column(String, unique=True)  # e.g., "simulation.run"
    description: str = Column(String)
    
class UserSession(Base):
    __tablename__ = "user_sessions"
    id: int = Column(Integer, primary_key=True)
    token_hash: str = Column(String, unique=True, nullable=False)
    session_correlation_id: str = Column(String, unique=True, nullable=False)
    user_id: int = Column(ForeignKey("users.id"))
    created_at: datetime = Column(DateTime(timezone=True))
    last_seen_at: datetime = Column(DateTime(timezone=True))
    expires_at: datetime = Column(DateTime(timezone=True))
    invalidated_at: Optional[datetime] = Column(DateTime(timezone=True))

# backend/ipsp/auth/service.py
class AuthService:
    def __init__(self, user_repo: UserRepository, config: Settings):
        self.user_repo = user_repo
        self.config = config
        
    def login(self, username: str, password: str) -> tuple[UserSession, str]:
        """Throttle/lock failures; issue a new opaque token and persist only its hash."""
        
    def logout(self, bearer_token: str) -> None:
        """Invalidate session."""
        
    def verify_session(self, bearer_token: str) -> User:
        """Hash lookup token; enforce expiry/invalidation and return user."""
        
    def change_password(self, user_id: int, old_pwd: str, new_pwd: str) -> None:
        """Hash password and invalidate all sessions; role changes do the same."""

# backend/ipsp/auth/rbac.py
class RBACService:
    def __init__(self, role_repo, permission_repo):
        ...
        
    def has_permission(self, user_id: int, permission_code: str) -> bool:
        """Check if user role has permission."""
        
    def enforce_permission(self, user_id: int, permission_code: str) -> None:
        """Raise PermissionDeniedException if the resolved permissions deny access."""
```

#### 2. Configuration & Providers

```python
# backend/ipsp/config/settings.py
class Settings(BaseSettings):
    # Database
    database_url: str = Field(default="sqlite:///./ipsp.db")
    
    # Security
    secret_key: str  # Required and stable; production startup fails closed if absent
    password_pepper: Optional[str] = Field(default=None)  # External secret
    session_expiry_hours: int = 8
    
    # Features
    enable_llm: bool = False
    llm_provider: str = "null"  # "null", "local", "remote", "hybrid"
    
    # Storage (Phase 2+)
    data_dir: Path = Field(default="./data")
    artifacts_dir: Path = Field(default="./artifacts")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# backend/ipsp/config/providers.py
class ProviderRegistry:
    """Dependency injection for swappable providers."""
    
    def get_llm_provider(self) -> SemanticLLMProvider:
        if self.config.llm_provider == "null":
            return NullLLMProvider()
        elif self.config.llm_provider == "local":
            return LocalLLMProvider(...)  # Phase 8
        # ...
        
    def get_secret_provider(self) -> SecretProvider:
        """Return interface for accessing API keys, passwords."""
        
    def get_outbound_policy(self) -> OutboundPolicy:
        """Return policy enforcer for remote calls."""
```

#### 3. Observability & Logging

```python
# backend/ipsp/observability/logging.py
import structlog
import contextvars

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.dev.ConsoleRenderer(),
        ],
    )
    
async def attach_trace_ids(request):
    """FastAPI middleware to assign and propagate trace IDs."""
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    trace_id_var.set(trace_id)
    ...

# backend/ipsp/observability/errors.py
class IPSPException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message  # Safe for client
        
class DataValidationException(IPSPException):
    def __init__(self, message: str):
        super().__init__("DATA-001", message)
        
class AuthenticationRequiredException(IPSPException):
    def __init__(self):
        super().__init__("AUTH-001", "Authentication required")
        
class PermissionDeniedException(IPSPException):
    def __init__(self, permission: str):
        super().__init__("AUTHZ-001", f"Permission '{permission}' required")

# backend/ipsp/observability/audit.py (service; ORM is database/models/audit.py)
class AuditService:
    def record(self, event: AuditEventCreate) -> None:
        """Persist a sanitized durable audit event through AuditEventRepository."""
```

The event contract contains `timestamp_utc`, `event_id`, `trace_id`, `request_id`, non-secret `session_correlation_id`, `user_id`, resolved role, relevant project/dataset/version/model/run references, `component`, `action`, `status`, `duration_ms`, `severity`, `error_code`, `resource_type`, `resource_id`, and sanitized metadata as context permits. Durable audit/security events may use SQLite; high-volume runtime logs use structured rotating files or another configured sink.

#### 4. Database & Migrations

```python
# backend/ipsp/database/models/base.py
class Base(DeclarativeBase):
    pass

# Security entities are imported from database/models/security.py;
# they are not redefined in auth, observability, or API modules.

# Workspace/data tables (Phase 2+, stubbed in Phase 1)
class Project(Base):
    __tablename__ = "projects"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    owner_id: int = Column(ForeignKey("users.id"))
    created_at: datetime = Column(DateTime, default=utcnow)
    
class Dataset(Base):
    __tablename__ = "datasets"  # logical identity only
    # Immutable records live in dataset_versions (Phase 2).

# database/migrations/versions/001_initial_schema.py
def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        # ... all columns
    )
    # ... all tables
    
def downgrade() -> None:
    op.drop_table('users')
    # ... etc
```

#### 5. API Routers (Thin Layer)

```python
# backend/ipsp/api/routes/auth.py
from fastapi import APIRouter, Depends, Request, Response

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login")
def login(payload: LoginRequest, auth_service: AuthService = Depends()):
    session, bearer_token = auth_service.login(payload.username, payload.password)
    
    response = JSONResponse({"status": "success"})
    response.set_cookie(
        "session_token",
        bearer_token,
        httponly=True,
        secure=config.production_or_https,
        samesite="strict",
        max_age=config.session_expiry_hours * 3600
    )
    return response

@router.post("/logout")
def logout(session_token: str = Cookie(), auth_service: AuthService = Depends()):
    auth_service.logout(session_token)
    response = JSONResponse({"status": "success"})
    response.delete_cookie("session_token")
    return response

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.name,
    }

# backend/ipsp/api/routes/health.py
# Infrastructure probes are intentionally outside the /api/v1 application namespace.
@router.get("/health/live")
def liveness(): ...

@router.get("/health/ready")
def readiness(readiness_service: ReadinessService = Depends()): ...

@router.get("/api/v1/admin/system/health")
def admin_health(admin_health_service: AdminHealthService = Depends()): ...
```

Authentication and RBAC/domain services raise typed `IPSPException` subclasses. A shared FastAPI exception handler maps those exceptions to HTTP status codes and the stable safe envelope (`error_code`, safe `message`, `trace_id`, and optional recoverability details); routes do not construct ad-hoc authentication/authorization errors. State-changing browser routes validate CSRF. `/health/live` and `/health/ready` are intentionally unversioned infrastructure probes, while `/api/v1/admin/system/health` is the versioned authorized diagnostic route. Health services use explicit exception handling, stable `SYS-*` codes, and sanitized output.

#### 6. Repositories

```python
# backend/ipsp/repositories/base.py
class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model
        
    def get_by_id(self, id: int) -> Optional[T]:
        result = self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
        
    def list(self, skip: int = 0, limit: int = 100) -> list[T]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.session.scalars(statement))

# backend/ipsp/repositories/users.py
class UserRepository(BaseRepository[User]):
    def get_by_username(self, username: str) -> Optional[User]:
        result = self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
        
    def create(self, create: UserCreate) -> User:
        user = User(**create.model_dump())
        self.session.add(user)
        self.session.commit()
        return user
```

#### 7. Job Foundation Contracts

```python
# backend/ipsp/jobs/contracts.py
class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class JobType(str, Enum):
    UPLOAD_PROCESSING = "UPLOAD_PROCESSING"
    PROFILING = "PROFILING"
    MODEL_TRAINING = "MODEL_TRAINING"
    SIMULATION = "SIMULATION"
    REPORT_GENERATION = "REPORT_GENERATION"

class JobBackend(Protocol): ...
class JobRepository(Protocol): ...
class JobService: ...
```

The contracts include owner, trace ID, progress/phase/message, cancellation, retryability, artifact references, and sanitized error details. The foundation stores job metadata in SQLite; it does not require a distributed worker.

---

## Part D: Phase 1 / v0.1.0 Implementation Conformance Checklist

### ✅ Dataset Agnosticism

- [ ] No column `campaign_id`, `funnel_stage`, `ROAS`, `CPA`, `budget`, `channel` hardcoded in core schema
- [ ] No special-case routing for "marketing" datasets
- [ ] `Project` and `Dataset` are generic containers; no domain metadata in v0.1.0
- [ ] Benchmark fixtures may use these names for test data only
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: Schema review confirms zero benchmark-specific fields outside fixtures

### ✅ LLM Authority Boundaries

- [ ] `SemanticLLMProvider` interface exists with `NullLLMProvider` default
- [ ] No LLM called for numerical predictions in v0.1.0
- [ ] All LLM outputs validated against schema before use
- [ ] Config flag `enable_llm=False` by default; app fully functional without LLM
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: App boots and basic flows work with `enable_llm=False`

### ✅ Trust Validation

- [ ] `TrustValidator` service interface defined (implementation in Phase 6)
- [ ] No simulation result bypasses validation logic, even if it "looks obvious"
- [ ] Trust gate enforced as immovable architectural layer
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: TrustValidator contract defined; placeholder implementation

### ✅ RBAC & Security

- [ ] `User`, `Role`, `Permission` tables present
- [ ] `User.role_id → Role → RolePermission → Permission` is the only authorization authority
- [ ] `enforce_permission(user_id, permission_code)` called by all protected endpoints
- [ ] Passwords hashed with maintained `pwdlib[argon2]`; no plaintext in database
- [ ] Opaque session bearer tokens rotate on login and only token hashes are persisted
- [ ] Sessions expire and invalidate on logout, password changes, and role/privilege changes
- [ ] HttpOnly/Secure production cookies, explicit localhost behavior, suitable SameSite, and CSRF for POST/PUT/PATCH/DELETE
- [ ] Failed logins are throttled and temporarily locked out
- [ ] Required production secrets fail closed and raw session tokens are never logged
- [ ] Audit events logged for all authentication/authorization actions
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: Auth tests pass; RBAC enforced; secrets not logged

### ✅ SQLite-Control / Parquet-Analytical Separation

- [ ] SQLite stores control/knowledge/governance metadata only, including applicable auth/RBAC, project, dataset/version, semantic, capability/model registry, simulation/run, job, configuration-reference, preference, durable audit/security, notification/backup, and other control-plane state defined by `27_SQLITE_SCHEMA_SPEC.md`.
- [ ] Parquet/file storage directory initialized (Phase 2 populates)
- [ ] Raw analytical dataset rows remain outside SQLite in the file/Parquet analytical data plane
- [ ] Repository pattern enforces separation of concerns
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: Schema review confirms control-plane/analytical-plane separation

### ✅ Canonical UI Contract

- [ ] CSS design tokens match reference HTML (colors, typography, spacing)
- [ ] No hardcoded campaign/funnel/ROAS content in production HTML
- [ ] Component library skeleton (cards, buttons, form controls) based on reference
- [ ] Shared tokens, complete dark/light token sets, switching, and persisted preference created in v0.1.0
- [ ] Pinned browser assets vendored locally with version/license inventory and no runtime CDN
- [ ] Dark theme from reference HTML adopted as default
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: Frontend review against reference HTML; design consistency confirmed

### ✅ Reproducibility / Versioning

- [ ] `datasets` represents logical identity and `dataset_versions` stores immutable versions (Phase 2)
- [ ] Semantic manifest, capability, and model version records are immutable once referenced
- [ ] Simulation runs reference exact immutable version records and persist seed plus effective non-secret configuration snapshot/hash
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: Version schemas reviewed; no mutable label is the sole reproducibility reference

### ✅ Multi-Table Support (Foundational)

- [ ] `DatasetTable` and `Relationship` tables stubbed (fully implemented Phase 3-4)
- [ ] Multi-table status derives from `dataset_tables` count; no duplicate persisted Boolean
- [ ] No forced flattening assumption in base schema
- [ ] **Phase 1 / v0.1.0 Pass Criteria**: Schema supports multi-table extension

---

## Part E: Testing Strategy for Phase 1 / v0.1.0

### Unit Tests

```
tests/unit/
├── test_auth.py
│   ├── test_password_hashing
│   ├── test_password_verification
│   └── test_pepper_handling
├── test_rbac.py
│   ├── test_permission_check_granted
│   ├── test_permission_check_denied
│   └── test_role_permissions_loaded
├── test_config.py
│   ├── test_env_var_loading
│   ├── test_feature_flags
│   └── test_provider_registry
├── test_errors.py
│   ├── test_error_response_no_stacktrace
│   ├── test_validation_error_detail
│   └── test_error_code_mapping
└── test_logging.py
    ├── test_trace_id_propagation
    ├── test_audit_event_recording
    └── test_secret_redaction
```

### Integration Tests

```
tests/integration/
├── test_auth_flow.py
│   ├── test_login_creates_session
│   ├── test_login_rotates_opaque_token_and_stores_hash_only
│   ├── test_logout_invalidates_session
│   ├── test_session_expiry
│   ├── test_password_change_invalidates_sessions
│   ├── test_role_change_invalidates_sessions
│   ├── test_failed_login_throttling_and_lockout
│   └── test_invalid_credentials
├── test_migrations.py
│   ├── test_migration_up
│   ├── test_migration_down
│   ├── test_migration_idempotent
│   └── test_schema_integrity
├── test_session.py
│   ├── test_cookie_httponly
│   ├── test_cookie_secure_flag
│   ├── test_samesite_policy
│   └── test_csrf_token_validation
└── test_api.py
    ├── test_liveness_endpoint
    ├── test_readiness_endpoint
    ├── test_admin_health_requires_permission
    ├── test_profile_endpoint_requires_auth
    └── test_admin_endpoint_requires_permission
```

### Security Tests

```
tests/security/
├── test_password.py
│   ├── test_argon2id_hashing
│   ├── test_password_not_reversible
│   └── test_pepper_integration
├── test_policy.py
│   ├── test_outbound_policy_blocks_disallowed_call
│   └── test_secret_provider_redacts_logs
├── test_secrets.py
│   ├── test_no_plaintext_secrets_in_db
│   ├── test_no_plaintext_secrets_in_logs
│   └── test_secret_reference_only_in_code
└── test_rbac.py
    ├── test_protected_endpoint_enforces_permission
    ├── test_admin_only_endpoint
    └── test_dataset_permission_checks
```

### Test Fixtures

```python
# tests/conftest.py
@pytest.fixture
def test_db():
    """In-memory SQLite for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

@pytest.fixture
def test_admin_user(test_db, admin_role):
    """Create test admin user."""
    user = User(
        username="admin",
        display_name="Test Admin",
        email="admin@test.local",
        password_hash=hash_password("password123"),
        role_id=admin_role.id,
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    return user

@pytest.fixture
def test_regular_user(test_db, user_role):
    """Create test regular user."""
    user = User(
        username="user",
        display_name="Test User",
        email="user@test.local",
        password_hash=hash_password("password123"),
        role_id=user_role.id,
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    return user

@pytest.fixture
def client(test_db):
    """FastAPI test client."""
    return TestClient(app)
```

---

## Part F: Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Benchmark contamination creep** | High | Critical | Code review checklist; no benchmark fields in core; fixtures isolated; AGENTS.md enforcement |
| **LLM called without validation** | Medium | High | Interface contract; NullLLMProvider default; tests verify no LLM calls in base flow |
| **Trust validation skipped** | Medium | High | Architectural layer; test enforces validation gate on all runs |
| **Secrets leaked in logs** | Medium | High | Redactor middleware; test scans logs for credentials |
| **SQLite bloat** | Low (v0.1.0) | High (later) | Repository pattern; no raw data rows; Parquet separation strict |
| **RBAC bypass via missing checks** | Medium | High | Centralized `enforce_permission` call; endpoint review checklist |
| **Session fixation** | Low | High | New opaque token on login; hash-only storage; lifecycle invalidation; secure cookie and CSRF controls |
| **Hardcoded UI domain content** | Medium | High | Design review; all controls metadata-driven; hardcoded demo content removed |
| **Database migration conflicts** | Medium | Medium | Linear migration sequence; git history preserved; no manual SQL edits |
| **Inconsistent error responses** | Low | Low | Error taxonomy; response envelope; client-safe messages |

---

## Part G: Dependencies & Tooling

### Backend Stack
- **Framework**: Current maintained compatible FastAPI and Uvicorn resolved at implementation time
- **ORM**: Current maintained compatible SQLAlchemy 2.x and Alembic; synchronous control-plane execution
- **Database**: SQLite (stdlib)
- **Security**: `pwdlib[argon2]`, cryptography where directly required, opaque server sessions
- **Configuration**: pydantic-settings, python-dotenv
- **Observability**: structlog, contextvars
- **Testing**: pytest, pytest-asyncio, httpx
- **Code Quality**: mypy, pylint, black, isort, ruff

### Frontend Stack
- **HTML/CSS/JS**: Vanilla (no build step for v0.1.0)
- **Charts** (Phase 6+): pinned Plotly.js vendored under `frontend/assets/vendor/`
- **No npm/Node.js** (v0.1.0)

### DevOps / Deployment (Phase 9+)
- Docker, docker-compose (scaffolding placeholder)
- PostgreSQL migration path (schema portable)
- Redis session store (Phase 2+, optional)
- Celery job worker (Phase 2+, optional)

Redis and Celery remain future optional implementations behind abstractions and are not v0.1.0 requirements.

---

## Part H: Planned Success Criteria for Phase 1 / v0.1.0

- [ ] All locked decisions are traceable to the implemented code/schema.
- [ ] Core production logic contains zero benchmark-specific fields; fixtures remain isolated.
- [ ] The LLM provider interface exists and the app boots without an LLM enabled.
- [ ] SQLite control-plane and Parquet analytical-plane separation is verified.
- [ ] The RBAC/auth foundation is complete with passing tests.
- [ ] The Trust Validation contract is architecturally present for later implementation.
- [ ] Audit logging and trace propagation are implemented and tested.
- [ ] The design system follows the reference language without hardcoded domain content.
- [ ] The database migration framework is implemented and tested.
- [ ] Subsystem-prefixed error taxonomy and safe centralized responses are implemented.
- [ ] All implementation conformance checks in Part D pass.
- [ ] Implementation progress and handoff documentation are updated with test evidence.

---

## Part I: Handoff to Phase 1

**Phase 1 implements v0.1.0 complete foundation** with:
1. FastAPI app factory with all middleware
2. SQLAlchemy models/repositories + Alembic migrations
3. Auth service + RBAC enforcement on all endpoints
4. Session management + CSRF protection
5. Password hashing with Argon2id
6. Audit logging + trace ID propagation
7. Error taxonomy + structured error responses
8. Feature flags + provider registry
9. CLI admin bootstrap script
10. 40+ tests covering auth, RBAC, config, logging, migrations, security
11. Foundation job contracts/schema and separate liveness/readiness/Admin-health contracts
12. Shared dark/light theme foundation and locally vendored browser-asset policy

**Acceptance gate**: All Phase 1 / v0.1.0 tests pass; no benchmark contamination; schema reviewed; design language extracted.

---

## Appendix: Architectural Principles Summary

```
IPSP v1.0 is built on these non-negotiable principles:

1. Dataset agnosticism: Metadata-driven, not domain-hardcoded
2. Trust-first: Every result passes independent validation
3. Reproducible: Dataset/semantic/model versions tracked
4. Secure: Argon2id passwords, server sessions, RBAC-enforced
5. Observable: Trace IDs, audit logs, no secret leaks
6. Separated: SQLite (metadata) ≠ Parquet (data)
7. LLM-optional: Full ML-only operation without LLM
8. Multi-table ready: Relationships inferred, not flattened
9. Causal-aware: No "causality" without causal evidence
10. Extensible: Interfaces + providers for future modes/features

Violating any principle requires:
  - Explicit decision log entry (docs/32_DECISION_LOG.md)
  - Approval from core team
  - Updated AGENTS.md
  - Tests demonstrating safety
```

---

**Phase 0 Status**: ✅ COMPLETE — Specification and plan generation complete.  
**Phase 0.5 Status**: ✅ PASS — Corrections, verification searches, and progress/report sign-off complete.  
**Next Action**: Phase 1 may implement the v0.1.0 foundation under this corrected plan.
