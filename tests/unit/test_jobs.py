"""Foundation job-contract validation."""

import pytest
from ipsp.jobs import JobBackend, JobError, JobProgress, JobStatus, JobType
from ipsp.jobs.service import JobService
from ipsp.repositories.jobs import JobRepository, decode_artifact_references


def test_job_enums_are_stable_and_unique() -> None:
    assert JobStatus.QUEUED.value == "QUEUED"
    assert JobStatus.CANCELLED.value == "CANCELLED"
    assert len({item.value for item in JobType}) == len(JobType)


def test_job_progress_enforces_intrinsic_bounds() -> None:
    assert JobProgress(percent=50, phase="profile", message="In progress").percent == 50
    with pytest.raises(ValueError, match="between 0 and 100"):
        JobProgress(percent=101, phase="profile", message="Invalid")
    with pytest.raises(ValueError):
        JobProgress(percent=1, phase="line\nbreak", message="Invalid")
    with pytest.raises(ValueError):
        JobProgress(percent=1, phase="profile", message="x" * 513)


def test_job_errors_use_safe_bounded_job_taxonomy() -> None:
    assert JobError("JOB-EXECUTION-FAILED", "Job execution failed.", True).retryable is True
    with pytest.raises(ValueError, match="JOB"):
        JobError("SYS-FAILED", "Invalid taxonomy.", False)
    with pytest.raises(ValueError):
        JobError("JOB-FAILED", "unsafe\nmultiline", False)


def test_job_json_helpers_are_deterministic_sanitized_and_fail_closed() -> None:
    assert JobRepository.encode_metadata({"z": 1, "password": "hidden", "a": 2}) == (
        '{"a":2,"password":"[REDACTED]","z":1}'
    )
    assert decode_artifact_references('["reports/example-id"]') == ("reports/example-id",)
    assert decode_artifact_references("not-json") == ()
    assert decode_artifact_references('{"not":"a-list"}') == ()


def test_job_interfaces_have_canonical_ownership() -> None:
    assert JobBackend.__name__ == "JobBackend"
    assert JobRepository.__name__ == "JobRepository"
    assert JobService.__name__ == "JobService"
