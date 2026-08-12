"""Bounded standard-library single-process local job backend."""

from __future__ import annotations

import logging
import threading
import time
from queue import Empty, Queue
from typing import Final, cast

from ipsp.errors.exceptions import IPSPError
from ipsp.jobs.contracts import JobBackendHealth
from ipsp.jobs.enums import JobType
from ipsp.jobs.executor import JobExecutionLifecycle, JobExecutor

logger = logging.getLogger("ipsp.jobs")

DEFAULT_SHUTDOWN_GRACE_SECONDS: Final[float] = 1.0
_STOP: Final[object] = object()


class LocalJobBackend:
    """Run persisted job IDs on bounded daemon workers in one application process."""

    def __init__(
        self,
        executor: JobExecutor,
        *,
        worker_count: int = 2,
        shutdown_grace_seconds: float = DEFAULT_SHUTDOWN_GRACE_SECONDS,
    ) -> None:
        if not 1 <= worker_count <= 32:
            raise ValueError("Worker count must be between 1 and 32")
        if not 0 <= shutdown_grace_seconds <= 60:
            raise ValueError("Shutdown grace must be between 0 and 60 seconds")
        self._job_executor = executor
        self._worker_count = worker_count
        self._shutdown_grace_seconds = shutdown_grace_seconds
        self._lock = threading.Lock()
        self._queue: Queue[object] | None = None
        self._threads: tuple[threading.Thread, ...] = ()
        self._stop_requested: threading.Event | None = None
        self._lifecycle: JobExecutionLifecycle | None = None
        self._abandoned_threads: tuple[threading.Thread, ...] = ()
        self._accepting = False
        self._shutting_down = False
        self._generation = 0

    def can_handle(self, job_type: JobType) -> bool:
        return self._job_executor.can_handle(job_type)

    def start(self) -> None:
        with self._lock:
            if self._accepting:
                return
            self._abandoned_threads = tuple(
                thread for thread in self._abandoned_threads if thread.is_alive()
            )
            if self._abandoned_threads:
                raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
            if self._queue is not None or self._shutting_down:
                raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
            self._generation += 1
            work_queue: Queue[object] = Queue()
            stop_requested = threading.Event()
            lifecycle = JobExecutionLifecycle()
            threads = tuple(
                threading.Thread(
                    target=self._worker_loop,
                    args=(work_queue, stop_requested, lifecycle),
                    name=f"ipsp-job-{self._generation}-{index + 1}",
                    daemon=True,
                )
                for index in range(self._worker_count)
            )
            self._queue = work_queue
            self._threads = threads
            self._stop_requested = stop_requested
            self._lifecycle = lifecycle
            self._accepting = True
            for thread in threads:
                thread.start()
        try:
            for job_id in self._job_executor.recover_interrupted():
                self.enqueue(job_id)
        except Exception:
            self.shutdown()
            raise

    def enqueue(self, job_id: str) -> None:
        with self._lock:
            if not self._accepting or self._queue is None:
                raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
            self._queue.put_nowait(job_id)

    def shutdown(self) -> None:
        with self._lock:
            if self._queue is None or self._shutting_down:
                return
            self._accepting = False
            self._shutting_down = True
            work_queue = self._queue
            threads = self._threads
            stop_requested = self._stop_requested
            lifecycle = self._lifecycle
            if stop_requested is None or lifecycle is None:
                self._clear_generation(work_queue)
                return
            stop_requested.set()
            lifecycle.stop_starting()

        self._discard_queued_work(work_queue)
        for _ in threads:
            work_queue.put_nowait(_STOP)

        deadline = time.monotonic() + self._shutdown_grace_seconds
        for thread in threads:
            remaining = max(0.0, deadline - time.monotonic())
            thread.join(remaining)
        if any(thread.is_alive() for thread in threads):
            lifecycle.abandon()

        with self._lock:
            self._abandoned_threads = tuple(thread for thread in threads if thread.is_alive())
            self._clear_generation(work_queue)

    def health(self) -> JobBackendHealth:
        with self._lock:
            queue_depth = self._queue.qsize() if self._accepting and self._queue is not None else 0
            return JobBackendHealth(
                running=self._queue is not None and not self._shutting_down,
                accepting_jobs=self._accepting,
                worker_count=self._worker_count,
                queue_depth=queue_depth,
            )

    def _worker_loop(
        self,
        work_queue: Queue[object],
        stop_requested: threading.Event,
        lifecycle: JobExecutionLifecycle,
    ) -> None:
        while True:
            item = work_queue.get()
            try:
                if item is _STOP:
                    return
                if stop_requested.is_set():
                    continue
                self._execute_safely(cast(str, item), lifecycle)
            finally:
                work_queue.task_done()

    def _execute_safely(self, job_id: str, lifecycle: JobExecutionLifecycle) -> None:
        try:
            self._job_executor.execute(job_id, lifecycle)
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

    @staticmethod
    def _discard_queued_work(work_queue: Queue[object]) -> None:
        while True:
            try:
                work_queue.get_nowait()
            except Empty:
                return
            else:
                work_queue.task_done()

    def _clear_generation(self, work_queue: Queue[object]) -> None:
        if self._queue is work_queue:
            self._queue = None
            self._threads = ()
            self._stop_requested = None
            self._lifecycle = None
        self._accepting = False
        self._shutting_down = False
