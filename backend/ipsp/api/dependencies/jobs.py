"""Application-state job service dependency."""

from typing import cast

from fastapi import Request

from ipsp.jobs.service import JobService


def get_job_service(request: Request) -> JobService:
    return cast(JobService, request.app.state.foundation_services.job_service)
