"""Foundation job-contract validation."""

import pytest
from ipsp.jobs import JobBackend, JobProgress, JobRepository, JobService, JobStatus, JobType


def test_job_enums_are_stable_and_unique() -> None:
    assert JobStatus.QUEUED.value == "QUEUED"
    assert JobStatus.CANCELLED.value == "CANCELLED"
    assert len({item.value for item in JobType}) == len(JobType)


def test_job_progress_enforces_intrinsic_bounds() -> None:
    assert JobProgress(percent=50, phase="profile", message="In progress").percent == 50
    with pytest.raises(ValueError, match="between 0 and 100"):
        JobProgress(percent=101, phase="profile", message="Invalid")


def test_job_interfaces_are_importable_protocols() -> None:
    assert JobBackend.__name__ == "JobBackend"
    assert JobRepository.__name__ == "JobRepository"
    assert JobService.__name__ == "JobService"
