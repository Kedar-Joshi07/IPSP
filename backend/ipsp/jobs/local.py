"""Bounded standard-library in-process job backend."""

from __future__ import annotations

import logging
import threading
from concurrent.futures import Future, ThreadPoolExecutor

from ipsp.errors.exceptions import IPSPError
from ipsp.jobs.contracts import JobBackendHealth
from ipsp.jobs.enums import JobType
from ipsp.jobs.executor import JobExecutor

logger = logging.getLogger("ipsp.jobs")


class LocalJobBackend:
    """Schedule persisted job IDs without owning database sessions or handler loading."""

    def __init__(self, executor: JobExecutor, *, worker_count: int = 2) -> None:
        if not 1 <= worker_count <= 32:
            raise ValueError("Worker count must be between 1 and 32")
        self._job_executor = executor
        self._worker_count = worker_count
        self._lock = threading.Lock()
        self._pool: ThreadPoolExecutor | None = None
        self._futures: set[Future[None]] = set()
        self._active_count = 0
        self._accepting = False

    def can_handle(self, job_type: JobType) -> bool:
        return self._job_executor.can_handle(job_type)

    def start(self) -> None:
        with self._lock:
            if self._accepting:
                return
            if any(not future.done() for future in self._futures):
                raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
            self._pool = ThreadPoolExecutor(
                max_workers=self._worker_count,
                thread_name_prefix="ipsp-job",
            )
            self._job_executor.prepare_start()
            self._accepting = True
        try:
            for job_id in self._job_executor.recover_interrupted():
                self.enqueue(job_id)
        except Exception:
            self.shutdown()
            raise

    def enqueue(self, job_id: str) -> None:
        with self._lock:
            if not self._accepting or self._pool is None:
                raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
            future = self._pool.submit(self._execute_safely, job_id)
            self._futures.add(future)
        future.add_done_callback(self._discard_future)

    def shutdown(self) -> None:
        with self._lock:
            if not self._accepting and self._pool is None:
                return
            self._accepting = False
            self._job_executor.begin_shutdown()
            pool = self._pool
            self._pool = None
        if pool is not None:
            pool.shutdown(wait=False, cancel_futures=True)

    def health(self) -> JobBackendHealth:
        with self._lock:
            pending = sum(not future.done() for future in self._futures)
            return JobBackendHealth(
                running=self._pool is not None,
                accepting_jobs=self._accepting,
                worker_count=self._worker_count,
                queue_depth=max(0, pending - self._active_count),
            )

    def _execute_safely(self, job_id: str) -> None:
        with self._lock:
            self._active_count += 1
        try:
            self._job_executor.execute(job_id)
        except Exception:
            logger.exception(
                "Job executor boundary failed",
                extra={
                    "ipsp_action": "job.failed",
                    "ipsp_stream": "errors",
                    "ipsp_component": "jobs",
                    "ipsp_status": "failure",
                    "ipsp_error_code": "JOB-EXECUTION-FAILED",
                    "ipsp_resource_type": "job",
                    "ipsp_resource_id": job_id,
                },
            )
        finally:
            with self._lock:
                self._active_count -= 1

    def _discard_future(self, future: Future[None]) -> None:
        with self._lock:
            self._futures.discard(future)
