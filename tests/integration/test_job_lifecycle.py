"""Phase 1H persistent job lifecycle, worker, API, recovery, and privacy tests."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from queue import Empty, Queue
from threading import Barrier, Event, Lock, Thread, current_thread
from threading import enumerate as enumerate_threads
from typing import TextIO
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ipsp.config.settings import Settings
from ipsp.database.models import AuditEvent, JobRecord, Role, User
from ipsp.errors.exceptions import IPSPError
from ipsp.jobs.contracts import JobError, JobExecutionContext, JobProgress
from ipsp.jobs.enums import JobStatus, JobType
from ipsp.jobs.executor import (
    JobExecutionAbandoned,
    JobExecutionLifecycle,
    PersistentJobExecutionContext,
)
from ipsp.jobs.local import LocalJobBackend
from ipsp.jobs.service import JobService
from ipsp.main import create_app
from ipsp.observability.context import bind_observability_context, current_observability_context
from ipsp.repositories.jobs import JobRepository, decode_job_metadata
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PASSWORD = "job-test-password-secret"

_BLOCKED_WORKER_CHILD = """
import json
import sys
import threading
import time
from pathlib import Path

from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Environment, Settings
from ipsp.jobs.enums import JobType
from ipsp.jobs.local import LocalJobBackend
from ipsp.jobs.service import JobService

database_path = Path(sys.argv[1])
settings = Settings(
    _env_file=None,
    environment=Environment.TEST,
    database={"url": f"sqlite:///{database_path.as_posix()}"},
    log_dir=database_path.parent / "child-logs",
    frontend_dir=database_path.parent / "missing-frontend",
)
started = threading.Event()
never_release = threading.Event()

def blocked_handler(_context):
    started.set()
    never_release.wait()

services = build_foundation_services(settings, job_handlers={JobType.RESTORE: blocked_handler})
backend = LocalJobBackend(
    services.job_executor,
    worker_count=1,
    shutdown_grace_seconds=0.05,
)
service = JobService(services.database_sessions, backend, services.audit_service)
backend.start()
job = service.submit(JobType.RESTORE, 81, retryable=True, max_attempts=2)
if not started.wait(2):
    raise RuntimeError("handler did not start")
shutdown_started = time.monotonic()
backend.shutdown()
elapsed = time.monotonic() - shutdown_started
snapshot = service.get_internal(job.job_id)
services.database_engine.dispose()
print(json.dumps({
    "job_id": job.job_id,
    "status": snapshot.status.value,
    "elapsed": elapsed,
    "stage": "normal_cleanup_complete",
}), flush=True)
"""

_RECOVERY_CHILD = """
import json
import sys
from pathlib import Path

from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Environment, Settings
from ipsp.jobs.enums import JobType
from ipsp.jobs.local import LocalJobBackend
from ipsp.jobs.service import JobService

database_path = Path(sys.argv[1])
job_id = sys.argv[2]
settings = Settings(
    _env_file=None,
    environment=Environment.TEST,
    database={"url": f"sqlite:///{database_path.as_posix()}"},
    log_dir=database_path.parent / "recovery-logs",
    frontend_dir=database_path.parent / "missing-frontend",
)
services = build_foundation_services(
    settings,
    job_handlers={JobType.RESTORE: lambda _context: None},
)
backend = LocalJobBackend(
    services.job_executor,
    worker_count=1,
    shutdown_grace_seconds=0.05,
)
service = JobService(services.database_sessions, backend, services.audit_service)
backend.start()
snapshot = service.get_internal(job_id)
print(json.dumps({
    "status": snapshot.status.value,
    "error_code": snapshot.error.error_code if snapshot.error else None,
    "retryable": snapshot.retryable,
}))
backend.shutdown()
services.database_engine.dispose()
"""


class _GateBeforeAuthorityLifecycle(JobExecutionLifecycle):
    """Deterministically pause one request before it acquires lifecycle authority."""

    def __init__(self, *, gate_start: bool = False, gate_persistence: bool = False) -> None:
        super().__init__()
        self._gate_start = gate_start
        self._gate_persistence = gate_persistence
        self.authority_requested = Event()
        self.release_authority = Event()

    @contextmanager
    def start_authority(self) -> Iterator[bool]:
        if self._gate_start:
            self._gate_start = False
            self.authority_requested.set()
            assert self.release_authority.wait(2)
        with super().start_authority() as allowed:
            yield allowed

    @contextmanager
    def persistence_authority(self) -> Iterator[bool]:
        if self._gate_persistence:
            self._gate_persistence = False
            self.authority_requested.set()
            assert self.release_authority.wait(2)
        with super().persistence_authority() as allowed:
            yield allowed


def _upgrade(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")


def _record(
    *,
    job_id: str | None = None,
    status: JobStatus = JobStatus.QUEUED,
    job_type: JobType = JobType.PROFILING,
    owner_user_id: int | None = None,
    retryable: bool = True,
    attempt_count: int = 1,
    max_attempts: int = 2,
    trace_id: str | None = None,
    request_id: str | None = None,
) -> JobRecord:
    now = datetime.now(UTC)
    return JobRecord(
        job_id=job_id or str(uuid4()),
        job_type=job_type.value,
        status=status.value,
        progress_percent=0,
        progress_phase="queued",
        progress_message="Queued.",
        owner_user_id=owner_user_id,
        trace_id=trace_id or str(uuid4()),
        request_id=request_id,
        attempt_count=attempt_count,
        max_attempts=max_attempts,
        retryable=retryable,
        cancel_requested=False,
        error_code=None,
        error_message=None,
        artifact_refs_json="[]",
        metadata_json="{}",
        created_at=now,
        queued_at=now,
        started_at=now if status is JobStatus.RUNNING else None,
        finished_at=None,
        updated_at=now,
    )


def _wait_for_status(
    app: FastAPI,
    job_id: str,
    statuses: set[JobStatus],
    *,
    timeout: float = 3.0,
):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        snapshot = app.state.foundation_services.job_service.get_internal(job_id)
        if snapshot.status in statuses:
            return snapshot
        time.sleep(0.01)
    raise AssertionError(f"Job {job_id} did not reach {statuses}")


def _add_user(app: FastAPI, username: str) -> int:
    services = app.state.foundation_services
    now = datetime.now(UTC)
    with services.database_sessions.transaction() as session:
        role = session.scalar(select(Role).where(Role.name == "User"))
        assert role is not None
        user = User(
            username=username,
            display_name=username.title(),
            email=None,
            password_hash=services.password_service.hash(PASSWORD),
            role_id=role.id,
            is_active=True,
            must_change_password=False,
            failed_login_count=0,
            locked_until=None,
            last_login_at=None,
            password_changed_at=now,
            created_at=now,
            created_by=None,
            updated_at=now,
        )
        session.add(user)
        session.flush()
        return user.id


def _read_pipe(
    pipe: TextIO,
    lines: list[str],
    marker_queue: Queue[dict[str, object]] | None = None,
) -> None:
    for line in pipe:
        lines.append(line)
        if marker_queue is None:
            continue
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict) and candidate.get("stage") == "normal_cleanup_complete":
            marker_queue.put(candidate)


def _start_pipe_readers(
    process: subprocess.Popen[str],
    marker_queue: Queue[dict[str, object]],
) -> tuple[list[str], list[str], tuple[Thread, Thread]]:
    assert process.stdout is not None
    assert process.stderr is not None
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    readers = (
        Thread(
            target=_read_pipe,
            args=(process.stdout, stdout_lines, marker_queue),
            name="blocked-worker-stdout-reader",
            daemon=True,
        ),
        Thread(
            target=_read_pipe,
            args=(process.stderr, stderr_lines),
            name="blocked-worker-stderr-reader",
            daemon=True,
        ),
    )
    for reader in readers:
        reader.start()
    return stdout_lines, stderr_lines, readers


def _reap_with_pipe_readers(
    process: subprocess.Popen[str],
    readers: tuple[Thread, Thread],
) -> None:
    if process.poll() is None:
        process.kill()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    for reader in readers:
        reader.join(timeout=2)
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()


def _communicate_and_reap(
    process: subprocess.Popen[str],
    *,
    timeout: float,
    timeout_message: str,
) -> tuple[str, str]:
    try:
        return process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        pytest.fail(f"{timeout_message}\nstdout:\n{stdout}\nstderr:\n{stderr}")
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()


def test_jobs_schema_is_exact_bounded_indexed_and_utc(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    inspector = inspect(services.database_engine)
    columns = {column["name"]: column for column in inspector.get_columns("jobs")}
    checks = {constraint["sqltext"] for constraint in inspector.get_check_constraints("jobs")}
    indexes = {
        index["name"]: tuple(index["column_names"]) for index in inspector.get_indexes("jobs")
    }
    expected_columns = {
        "id",
        "job_id",
        "job_type",
        "status",
        "progress_percent",
        "progress_phase",
        "progress_message",
        "owner_user_id",
        "trace_id",
        "request_id",
        "attempt_count",
        "max_attempts",
        "retryable",
        "cancel_requested",
        "error_code",
        "error_message",
        "artifact_refs_json",
        "metadata_json",
        "created_at",
        "queued_at",
        "started_at",
        "finished_at",
        "updated_at",
    }
    try:
        assert set(columns) == expected_columns
        assert all(
            not columns[name]["nullable"]
            for name in expected_columns
            - {
                "owner_user_id",
                "request_id",
                "error_code",
                "error_message",
                "started_at",
                "finished_at",
            }
        )
        assert indexes == {
            "ix_jobs_job_id": ("job_id",),
            "ix_jobs_job_type": ("job_type",),
            "ix_jobs_owner_user_id_created_at": ("owner_user_id", "created_at"),
            "ix_jobs_status": ("status",),
        }
        assert any("progress_percent >= 0" in check for check in checks)
        assert any("attempt_count >= 1" in check for check in checks)
        assert any("attempt_count <= max_attempts" in check for check in checks)
        assert any("status IN" in check for check in checks)
        assert any("job_type IN" in check for check in checks)
        assert {
            "password",
            "password_hash",
            "token",
            "cookie",
            "csrf_token",
            "request_body",
            "traceback",
            "payload",
            "callable",
            "module_path",
        }.isdisjoint(columns)

        valid = _record()
        with services.database_sessions.transaction() as session:
            session.add(valid)
            session.flush()
            valid_id = valid.id
        with services.database_sessions.session() as session:
            persisted = session.get(JobRecord, valid_id)
            assert persisted is not None
            assert persisted.created_at.tzinfo is UTC
            assert persisted.queued_at.tzinfo is UTC
            assert persisted.updated_at.tzinfo is UTC

        invalid = _record()
        invalid.progress_percent = 101
        with pytest.raises(IntegrityError), services.database_sessions.transaction() as session:
            session.add(invalid)
    finally:
        services.database_engine.dispose()


def test_persisted_metadata_and_artifact_corruption_decodes_safely(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    record = _record()
    marker = "DO_NOT_RETURN_TAMPERED_JOB_SECRET"
    try:
        with services.database_sessions.transaction() as session:
            session.add(record)
            session.flush()
            record.artifact_refs_json = json.dumps(
                [
                    "reports/safe-id",
                    "/absolute/path",
                    "C:/absolute/path",
                    "reports/../secret",
                    "reports/./secret",
                    "reports//secret",
                    "reports/has space",
                    "x" * 256,
                    17,
                ]
            )
            record.metadata_json = json.dumps({"safe": ["value", 1, True], "password": marker})

        snapshot = services.job_service.get_internal(record.job_id)
        assert snapshot.artifact_refs == ("reports/safe-id",)
        with services.database_sessions.session() as session:
            persisted = session.scalar(select(JobRecord).where(JobRecord.job_id == record.job_id))
            assert persisted is not None
            assert decode_job_metadata(persisted.metadata_json) == {
                "password": "[REDACTED]",
                "safe": ["value", 1, True],
            }

        with services.database_sessions.transaction() as session:
            persisted = session.scalar(select(JobRecord).where(JobRecord.job_id == record.job_id))
            assert persisted is not None
            persisted.artifact_refs_json = "not-json"
            persisted.metadata_json = "not-json"

        assert services.job_service.get_internal(record.job_id).artifact_refs == ()
        assert decode_job_metadata("not-json") == {}
        assert marker not in str(decode_job_metadata("not-json"))
    finally:
        services.database_engine.dispose()


def test_noncooperative_daemon_worker_cannot_hold_child_process_and_recovers(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    database_path = Path(settings.database.url.removeprefix("sqlite:///"))

    blocked = subprocess.Popen(
        [sys.executable, "-c", _BLOCKED_WORKER_CHILD, str(database_path)],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    marker_queue: Queue[dict[str, object]] = Queue(maxsize=1)
    stdout_lines, stderr_lines, readers = _start_pipe_readers(blocked, marker_queue)
    try:
        try:
            blocked_result = marker_queue.get(timeout=30)
        except Empty:
            pytest.fail(
                "Blocked-worker child did not complete setup and normal cleanup within 30 seconds"
            )
        assert blocked_result["stage"] == "normal_cleanup_complete"
        assert blocked_result["status"] == JobStatus.RUNNING.value
        assert isinstance(blocked_result["elapsed"], (int, float))
        assert blocked_result["elapsed"] < 0.5
        try:
            blocked.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail("Blocked daemon worker prevented process exit after normal cleanup")
    finally:
        _reap_with_pipe_readers(blocked, readers)
    assert blocked.returncode == 0, "".join(stderr_lines)
    assert stdout_lines
    assert blocked_result["status"] == JobStatus.RUNNING.value
    assert isinstance(blocked_result["job_id"], str)

    recovered = subprocess.Popen(
        [
            sys.executable,
            "-c",
            _RECOVERY_CHILD,
            str(database_path),
            str(blocked_result["job_id"]),
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    recovery_stdout, recovery_stderr = _communicate_and_reap(
        recovered,
        timeout=10,
        timeout_message="Fresh worker recovery child did not terminate",
    )
    assert recovered.returncode == 0, recovery_stderr
    recovery_result = json.loads(recovery_stdout.strip().splitlines()[-1])
    assert recovery_result == {
        "status": JobStatus.FAILED.value,
        "error_code": "JOB-WORKER-INTERRUPTED",
        "retryable": True,
    }


def test_repository_enforces_state_machine_and_atomic_claim_retry(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    queued = _record()
    failed = _record()
    cancelled = _record()
    competing_claim = _record()
    competing_retry = _record(status=JobStatus.FAILED)
    now = datetime.now(UTC)
    try:
        with services.database_sessions.transaction() as session:
            session.add_all((queued, failed, cancelled, competing_claim, competing_retry))

        with services.database_sessions.transaction() as session:
            repository = JobRepository(session)
            assert repository.mark_running(queued.job_id, now)
            assert not repository.mark_running(queued.job_id, now)
            assert repository.update_progress(
                queued.job_id, JobProgress(45, "work", "Working."), now
            )
            assert repository.mark_succeeded(queued.job_id, now)
            assert not repository.prepare_retry(queued.job_id, now)
            assert not repository.mark_running(queued.job_id, now)
            assert not repository.mark_failed(
                queued.job_id,
                JobError("JOB-EXECUTION-FAILED", "Job execution failed.", True),
                now,
            )

            assert repository.mark_running(failed.job_id, now)
            assert repository.mark_failed(
                failed.job_id,
                JobError("JOB-EXECUTION-FAILED", "Job execution failed.", True),
                now,
            )
            assert repository.prepare_retry(failed.job_id, now)
            assert not repository.prepare_retry(failed.job_id, now)

            result = repository.request_cancel(cancelled.job_id, now)
            assert result == (JobStatus.CANCELLED, True)
            assert repository.prepare_retry(cancelled.job_id, now)

        claim_results: list[bool] = []
        claim_lock = Lock()
        claim_barrier = Barrier(2)

        def claim() -> None:
            claim_barrier.wait()
            with services.database_sessions.transaction() as session:
                result = JobRepository(session).mark_running(
                    competing_claim.job_id, datetime.now(UTC)
                )
            with claim_lock:
                claim_results.append(result)

        threads = [Thread(target=claim) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=3)
        assert sorted(claim_results) == [False, True]

        retry_results: list[bool] = []
        retry_barrier = Barrier(2)

        def retry() -> None:
            retry_barrier.wait()
            with services.database_sessions.transaction() as session:
                result = JobRepository(session).prepare_retry(
                    competing_retry.job_id, datetime.now(UTC)
                )
            with claim_lock:
                retry_results.append(result)

        threads = [Thread(target=retry) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=3)
        assert sorted(retry_results) == [False, True]
    finally:
        services.database_engine.dispose()


def test_terminal_persistence_request_loses_deterministically_to_abandonment(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    _upgrade(settings, monkeypatch)
    handler_returned = Event()

    def handler(_: JobExecutionContext) -> None:
        handler_returned.set()

    app = create_app(settings, job_handlers={JobType.RESTORE: handler})
    services = app.state.foundation_services
    record = _record(status=JobStatus.QUEUED, job_type=JobType.RESTORE)
    lifecycle = _GateBeforeAuthorityLifecycle(gate_persistence=True)
    try:
        with services.database_sessions.transaction() as session:
            session.add(record)
        worker = Thread(target=services.job_executor.execute, args=(record.job_id, lifecycle))
        worker.start()
        assert handler_returned.wait(2)
        assert lifecycle.authority_requested.wait(2)
        lifecycle.abandon()
        lifecycle.release_authority.set()
        worker.join(timeout=2)
        assert not worker.is_alive()

        snapshot = services.job_service.get_internal(record.job_id)
        assert snapshot.status is JobStatus.RUNNING
        assert snapshot.error is None
        assert not snapshot.cancel_requested
        assert {getattr(item, "ipsp_action", None) for item in caplog.records}.isdisjoint(
            {"job.succeeded", "job.failed", "job.cancelled"}
        )
    finally:
        lifecycle.release_authority.set()
        services.database_engine.dispose()


def test_progress_after_abandonment_is_rejected_without_persistence(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    record = _record(status=JobStatus.RUNNING)
    lifecycle = JobExecutionLifecycle()
    context = PersistentJobExecutionContext(
        services.database_sessions,
        job_id=record.job_id,
        job_type=JobType.PROFILING,
        attempt=1,
        lifecycle=lifecycle,
    )
    try:
        with services.database_sessions.transaction() as session:
            session.add(record)
        lifecycle.abandon()
        with pytest.raises(JobExecutionAbandoned):
            context.update_progress(JobProgress(75, "late", "Late update."))
        snapshot = services.job_service.get_internal(record.job_id)
        assert snapshot.progress == JobProgress(0, "queued", "Queued.")
        assert snapshot.status is JobStatus.RUNNING
    finally:
        services.database_engine.dispose()


def test_artifact_after_abandonment_is_rejected_without_persistence(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    record = _record(status=JobStatus.RUNNING)
    lifecycle = JobExecutionLifecycle()
    context = PersistentJobExecutionContext(
        services.database_sessions,
        job_id=record.job_id,
        job_type=JobType.PROFILING,
        attempt=1,
        lifecycle=lifecycle,
    )
    try:
        with services.database_sessions.transaction() as session:
            session.add(record)
        lifecycle.abandon()
        with pytest.raises(JobExecutionAbandoned):
            context.add_artifact_reference("reports/late-artifact")
        snapshot = services.job_service.get_internal(record.job_id)
        assert snapshot.artifact_refs == ()
        assert snapshot.status is JobStatus.RUNNING
    finally:
        services.database_engine.dispose()


def test_start_claim_request_loses_deterministically_to_stop_starting(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings, job_handlers={JobType.RESTORE: lambda _: None})
    services = app.state.foundation_services
    record = _record(status=JobStatus.QUEUED, job_type=JobType.RESTORE)
    lifecycle = _GateBeforeAuthorityLifecycle(gate_start=True)
    try:
        with services.database_sessions.transaction() as session:
            session.add(record)
        worker = Thread(target=services.job_executor.execute, args=(record.job_id, lifecycle))
        worker.start()
        assert lifecycle.authority_requested.wait(2)
        lifecycle.stop_starting()
        lifecycle.release_authority.set()
        worker.join(timeout=2)
        assert not worker.is_alive()
        assert services.job_service.get_internal(record.job_id).status is JobStatus.QUEUED
    finally:
        lifecycle.release_authority.set()
        services.database_engine.dispose()


def test_authorized_short_persistence_completes_before_abandonment_revokes_authority(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    record = _record(status=JobStatus.RUNNING)
    lifecycle = JobExecutionLifecycle()
    authority_acquired = Event()
    abandonment_requested = Event()
    release_persistence = Event()
    try:
        with services.database_sessions.transaction() as session:
            session.add(record)

        def persist() -> None:
            with lifecycle.persistence_authority() as allowed:
                assert allowed
                authority_acquired.set()
                assert release_persistence.wait(2)
                with services.database_sessions.transaction() as session:
                    assert JobRepository(session).update_progress(
                        record.job_id,
                        JobProgress(35, "authorized", "Authorized update."),
                        datetime.now(UTC),
                    )

        persistence_thread = Thread(target=persist)
        persistence_thread.start()
        assert authority_acquired.wait(2)

        def abandon() -> None:
            abandonment_requested.set()
            lifecycle.abandon()

        abandonment_thread = Thread(target=abandon)
        abandonment_thread.start()
        assert abandonment_requested.wait(2)
        assert abandonment_thread.is_alive()
        release_persistence.set()
        persistence_thread.join(timeout=2)
        abandonment_thread.join(timeout=2)
        assert not persistence_thread.is_alive()
        assert not abandonment_thread.is_alive()
        assert services.job_service.get_internal(record.job_id).progress == JobProgress(
            35, "authorized", "Authorized update."
        )
        assert lifecycle.is_abandoned()
    finally:
        release_persistence.set()
        services.database_engine.dispose()


def test_worker_success_progress_artifact_audit_and_context_isolation(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    contexts: list[tuple[str, int | None, str | None]] = []
    daemon_flags: list[bool] = []
    barrier = Barrier(2)

    def handler(context: JobExecutionContext) -> None:
        barrier.wait(timeout=3)
        active = current_observability_context()
        contexts.append((active.trace_id, active.user_id, active.resource_id))
        daemon_flags.append(current_thread().daemon)
        context.update_progress(JobProgress(60, "work", "Processing."))
        context.add_artifact_reference(f"reports/{context.job_id}")

    app = create_app(settings, job_handlers={JobType.PROFILING: handler})
    services = app.state.foundation_services
    try:
        with TestClient(app):
            with bind_observability_context(request_id="request-one", trace_id="trace-one"):
                first = services.job_service.submit(JobType.PROFILING, 11)
            with bind_observability_context(request_id="request-two", trace_id="trace-two"):
                second = services.job_service.submit(JobType.PROFILING, 22)
            first_done = _wait_for_status(app, first.job_id, {JobStatus.SUCCEEDED})
            second_done = _wait_for_status(app, second.job_id, {JobStatus.SUCCEEDED})

        assert first_done.progress.percent == second_done.progress.percent == 100
        assert first_done.artifact_refs == (f"reports/{first.job_id}",)
        assert second_done.artifact_refs == (f"reports/{second.job_id}",)
        assert set(contexts) == {
            ("trace-one", 11, first.job_id),
            ("trace-two", 22, second.job_id),
        }
        assert daemon_flags == [True, True]
        with services.database_sessions.session() as session:
            actions = list(session.scalars(select(AuditEvent.action).order_by(AuditEvent.id)))
        assert actions == ["job.submit", "job.submit"]
        runtime = (settings.log_dir / "ipsp-runtime.jsonl").read_text(encoding="utf-8")
        assert "job.started" in runtime and "job.progress" in runtime and "job.succeeded" in runtime
        assert first.job_id in runtime and second.job_id in runtime
        events = [json.loads(line) for line in runtime.splitlines()]
        for snapshot, trace_id, request_id in (
            (first_done, "trace-one", "request-one"),
            (second_done, "trace-two", "request-two"),
        ):
            correlated = [
                event
                for event in events
                if event.get("resource_id") == snapshot.job_id
                and event.get("action") in {"job.submitted", "job.started", "job.succeeded"}
            ]
            assert {event["trace_id"] for event in correlated} == {trace_id}
            assert {event["request_id"] for event in correlated} == {request_id}
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_worker_failure_is_private_and_manual_retry_succeeds(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    marker = "DO_NOT_LEAK_JOB_EXCEPTION_PASSWORD_TOKEN_SQL_PATH_BODY"

    def handler(context: JobExecutionContext) -> None:
        if context.attempt == 1:
            raise RuntimeError(marker)
        context.update_progress(JobProgress(80, "retry", "Retrying safely."))

    app = create_app(settings, job_handlers={JobType.MODEL_TRAINING: handler})
    services = app.state.foundation_services
    try:
        with TestClient(app):
            failed = services.job_service.submit(
                JobType.MODEL_TRAINING,
                31,
                retryable=True,
                max_attempts=2,
                metadata={"password": marker, "safe": "retained"},
            )
            failed_snapshot = _wait_for_status(app, failed.job_id, {JobStatus.FAILED})
            assert failed_snapshot.error == JobError(
                "JOB-EXECUTION-FAILED", "Job execution failed.", True
            )
            retried = services.job_service.retry(failed.job_id, 31)
            assert retried.attempt_count == 2
            succeeded = _wait_for_status(app, failed.job_id, {JobStatus.SUCCEEDED})
            assert succeeded.error is None
            assert succeeded.progress.percent == 100
            with pytest.raises(IPSPError) as exhausted:
                services.job_service.retry(failed.job_id, 31)
            assert exhausted.value.error_code == "JOB-RETRY-NOT-ALLOWED"

        database_path = Path(settings.database.url.removeprefix("sqlite:///"))
        runtime_path = settings.log_dir / "ipsp-runtime.jsonl"
        assert marker.encode() not in database_path.read_bytes()
        assert marker not in runtime_path.read_text(encoding="utf-8")
        with services.database_sessions.session() as session:
            actions = list(session.scalars(select(AuditEvent.action).order_by(AuditEvent.id)))
        assert actions == ["job.submit", "job.retry"]
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_submission_fails_fast_without_handler_and_persisted_enqueue_failure_is_safe(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    no_handler_app = create_app(settings)
    no_handler_services = no_handler_app.state.foundation_services
    try:
        no_handler_services.job_backend.start()
        with pytest.raises(IPSPError) as unavailable_handler:
            no_handler_services.job_service.submit(JobType.PROFILING, 71)
        assert unavailable_handler.value.error_code == "JOB-HANDLER-UNAVAILABLE"
        assert no_handler_services.job_service.list(71) == []
    finally:
        no_handler_services.job_backend.shutdown()
        no_handler_services.database_engine.dispose()

    app = create_app(settings, job_handlers={JobType.PROFILING: lambda _: None})
    services = app.state.foundation_services
    try:
        services.job_backend.start()

        def reject_enqueue(_: str) -> None:
            raise RuntimeError("DO_NOT_LEAK_ENQUEUE_FAILURE")

        monkeypatch.setattr(services.job_backend, "enqueue", reject_enqueue)
        with pytest.raises(IPSPError) as unavailable_worker:
            services.job_service.submit(JobType.PROFILING, 71, retryable=True, max_attempts=2)
        assert unavailable_worker.value.error_code == "JOB-WORKER-UNAVAILABLE"
        persisted = services.job_service.list(71)
        assert len(persisted) == 1
        assert persisted[0].status is JobStatus.FAILED
        assert persisted[0].error == JobError(
            "JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.", True
        )
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_running_and_queued_cancellation_are_cooperative_and_race_safe(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    running_started = Event()
    cancellation_poll = Event()

    def cancellable(context: JobExecutionContext) -> None:
        running_started.set()
        while True:
            context.raise_if_cancelled()
            if cancellation_poll.wait(0.01) and context.is_cancel_requested():
                context.raise_if_cancelled()

    app = create_app(settings, job_handlers={JobType.SIMULATION: cancellable})
    services = app.state.foundation_services
    try:
        with TestClient(app):
            running = services.job_service.submit(JobType.SIMULATION, 41, retryable=True)
            assert running_started.wait(2)
            requested = services.job_service.cancel(running.job_id, 41)
            assert requested.cancel_requested is True
            cancelled = _wait_for_status(app, running.job_id, {JobStatus.CANCELLED})
            assert cancelled.status is JobStatus.CANCELLED

        calls = 0
        calls_lock = Lock()
        workers_blocked = Event()
        release = Event()

        def blocker(_: JobExecutionContext) -> None:
            nonlocal calls
            with calls_lock:
                calls += 1
                if calls == 2:
                    workers_blocked.set()
            release.wait(3)

        second_app = create_app(settings, job_handlers={JobType.BACKUP: blocker})
        second_services = second_app.state.foundation_services
        with TestClient(second_app):
            first = second_services.job_service.submit(JobType.BACKUP, 41)
            second_services.job_service.submit(JobType.BACKUP, 41)
            assert workers_blocked.wait(2)
            queued = second_services.job_service.submit(JobType.BACKUP, 41, retryable=True)
            assert second_services.job_backend.health().queue_depth == 1
            queued_cancelled = second_services.job_service.cancel(queued.job_id, 41)
            assert queued_cancelled.status is JobStatus.CANCELLED
            release.set()
            _wait_for_status(second_app, first.job_id, {JobStatus.SUCCEEDED})
            time.sleep(0.05)
            assert calls == 2
            assert (
                second_services.job_service.get_internal(queued.job_id).status
                is JobStatus.CANCELLED
            )
        second_services.database_engine.dispose()
    finally:
        running_started.set()
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_startup_recovers_running_and_executes_registered_queued_work(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    executed: list[str] = []

    def handler(context: JobExecutionContext) -> None:
        executed.append(context.job_id)

    app = create_app(settings, job_handlers={JobType.REPORT_GENERATION: handler})
    services = app.state.foundation_services
    interrupted = _record(
        status=JobStatus.RUNNING,
        job_type=JobType.REPORT_GENERATION,
        owner_user_id=61,
        trace_id="recovery-trace",
        request_id="recovery-request",
    )
    queued = _record(job_type=JobType.REPORT_GENERATION)
    try:
        with services.database_sessions.transaction() as session:
            session.add_all((interrupted, queued))
        services.job_backend.start()
        recovered = _wait_for_status(app, interrupted.job_id, {JobStatus.FAILED})
        queued_done = _wait_for_status(app, queued.job_id, {JobStatus.SUCCEEDED})
        assert recovered.error == JobError(
            "JOB-WORKER-INTERRUPTED", "Job execution was interrupted.", True
        )
        assert queued_done.job_id in executed
        assert interrupted.job_id not in executed
        retried = services.job_service.retry(interrupted.job_id, 61)
        assert retried.attempt_count == 2
        _wait_for_status(app, interrupted.job_id, {JobStatus.SUCCEEDED})
        assert interrupted.job_id in executed
        with services.database_sessions.session() as session:
            audit = session.scalar(
                select(AuditEvent).where(AuditEvent.action == "job.recovered_interrupted")
            )
            assert audit is not None
            assert audit.trace_id == "recovery-trace"
            assert audit.request_id == "recovery-request"
            assert audit.resource_id == interrupted.job_id
        runtime = (settings.log_dir / "ipsp-runtime.jsonl").read_text(encoding="utf-8")
        recovered_event = next(
            json.loads(line)
            for line in runtime.splitlines()
            if json.loads(line).get("action") == "job.recovered_interrupted"
        )
        assert recovered_event["trace_id"] == "recovery-trace"
        assert recovered_event["resource_id"] == interrupted.job_id
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_shutdown_does_not_falsely_succeed_running_job_and_lifecycle_is_idempotent(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    started = Event()
    finished = Event()
    release = Event()

    def handler(_: JobExecutionContext) -> None:
        started.set()
        release.wait(3)
        finished.set()

    app = create_app(settings, job_handlers={JobType.RESTORE: handler})
    services = app.state.foundation_services
    backend = LocalJobBackend(
        services.job_executor,
        worker_count=1,
        shutdown_grace_seconds=0.05,
    )
    service = JobService(services.database_sessions, backend, services.audit_service)
    try:
        backend.start()
        backend.start()
        job = service.submit(JobType.RESTORE, 51, retryable=True, max_attempts=2)
        assert started.wait(2)
        shutdown_started = time.monotonic()
        backend.shutdown()
        assert time.monotonic() - shutdown_started < 0.5
        backend.shutdown()
        assert backend.health().accepting_jobs is False
        with pytest.raises(IPSPError) as unavailable:
            backend.enqueue(str(uuid4()))
        assert unavailable.value.error_code == "JOB-WORKER-UNAVAILABLE"
        with pytest.raises(IPSPError) as overlapping_generation:
            backend.start()
        assert overlapping_generation.value.error_code == "JOB-WORKER-UNAVAILABLE"
        release.set()
        assert finished.wait(2)
        deadline = time.monotonic() + 2
        assert service.get_internal(job.job_id).status is JobStatus.RUNNING
        while True:
            try:
                backend.start()
                break
            except IPSPError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.01)
        recovered = service.get_internal(job.job_id)
        assert recovered.error is not None
        assert recovered.error.error_code == "JOB-WORKER-INTERRUPTED"
    finally:
        release.set()
        backend.shutdown()
        services.database_engine.dispose()


def test_handler_finishing_within_shutdown_grace_succeeds(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    started = Event()
    release = Event()

    def handler(_: JobExecutionContext) -> None:
        started.set()
        release.wait(2)

    app = create_app(settings, job_handlers={JobType.BACKUP: handler})
    services = app.state.foundation_services
    backend = LocalJobBackend(
        services.job_executor,
        worker_count=1,
        shutdown_grace_seconds=0.5,
    )
    service = JobService(services.database_sessions, backend, services.audit_service)
    try:
        backend.start()
        job = service.submit(JobType.BACKUP, 91)
        assert started.wait(2)
        shutdown_thread = Thread(target=backend.shutdown)
        shutdown_thread.start()
        time.sleep(0.02)
        release.set()
        shutdown_thread.join(timeout=2)
        assert not shutdown_thread.is_alive()
        assert service.get_internal(job.job_id).status is JobStatus.SUCCEEDED
    finally:
        release.set()
        backend.shutdown()
        services.database_engine.dispose()


def test_repeated_app_lifespan_does_not_leave_worker_infrastructure(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    try:
        for _ in range(2):
            with TestClient(app) as client:
                assert client.get("/health/live").status_code == 200
                assert services.job_backend.health().running is True
            assert services.job_backend.health().running is False
            assert not any(
                thread.is_alive() and thread.name.startswith("ipsp-job-")
                for thread in enumerate_threads()
            )
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_owner_only_job_api_auth_csrf_and_safe_errors(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)

    def handler(_: JobExecutionContext) -> None:
        return

    app = create_app(settings, job_handlers={JobType.REPORT_GENERATION: handler})
    services = app.state.foundation_services
    alice_id = services.auth_service.bootstrap_admin("alice-jobs", "Alice", None, PASSWORD)
    bob_id = _add_user(app, "bob-jobs")
    own = _record(owner_user_id=alice_id, retryable=True)
    other = _record(owner_user_id=bob_id)
    failed = _record(
        owner_user_id=alice_id,
        status=JobStatus.FAILED,
        job_type=JobType.REPORT_GENERATION,
        retryable=True,
    )
    system_owned = _record(owner_user_id=None)
    with services.database_sessions.transaction() as session:
        session.add_all((own, other, failed, system_owned))
    try:
        with TestClient(
            app, base_url="https://testserver", raise_server_exceptions=False
        ) as client:
            assert client.get("/api/v1/jobs").status_code == 401
            assert client.post(f"/api/v1/jobs/{own.job_id}/cancel").status_code == 401
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "alice-jobs", "password": PASSWORD},
            )
            assert login.status_code == 200
            own_response = client.get(f"/api/v1/jobs/{own.job_id}")
            hidden = client.get(f"/api/v1/jobs/{other.job_id}")
            absent = client.get(f"/api/v1/jobs/{uuid4()}")
            assert own_response.status_code == 200
            assert hidden.status_code == absent.status_code == 404
            assert hidden.json()["error_code"] == absent.json()["error_code"] == "JOB-NOT-FOUND"
            listed = client.get("/api/v1/jobs").json()["jobs"]
            assert {item["job_id"] for item in listed} == {own.job_id, failed.job_id}
            assert "metadata" not in own_response.text

            assert client.post(f"/api/v1/jobs/{own.job_id}/cancel").status_code == 403
            csrf = client.cookies.get(settings.auth.csrf_cookie_name)
            assert csrf
            cancelled = client.post(
                f"/api/v1/jobs/{own.job_id}/cancel",
                headers={settings.auth.csrf_header_name: csrf},
            )
            assert cancelled.status_code == 200
            assert cancelled.json()["status"] == "CANCELLED"
            assert (
                client.post(
                    f"/api/v1/jobs/{other.job_id}/cancel",
                    headers={settings.auth.csrf_header_name: csrf},
                ).status_code
                == 404
            )
            assert client.post(f"/api/v1/jobs/{failed.job_id}/retry").status_code == 403
            retried = client.post(
                f"/api/v1/jobs/{failed.job_id}/retry",
                headers={settings.auth.csrf_header_name: csrf},
            )
            assert retried.status_code == 200
            _wait_for_status(app, failed.job_id, {JobStatus.SUCCEEDED})
            rejected = client.post(
                f"/api/v1/jobs/{failed.job_id}/retry",
                headers={settings.auth.csrf_header_name: csrf},
            )
            assert rejected.status_code == 409
            assert rejected.json()["error_code"] == "JOB-RETRY-NOT-ALLOWED"
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()
