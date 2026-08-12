"""Thin authenticated owner-only generic job routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ipsp.api.dependencies.auth import require_authenticated_session, require_csrf
from ipsp.api.dependencies.jobs import get_job_service
from ipsp.api.schemas.jobs import JobListResponse, JobResponse
from ipsp.auth.service import AuthPrincipal
from ipsp.jobs.service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=JobListResponse)
def list_jobs(
    principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
    service: Annotated[JobService, Depends(get_job_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0, le=10000)] = 0,
) -> JobListResponse:
    return JobListResponse(
        jobs=[
            JobResponse.from_snapshot(snapshot)
            for snapshot in service.list(principal.user_id, limit=limit, offset=offset)
        ]
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: str,
    principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
    service: Annotated[JobService, Depends(get_job_service)],
) -> JobResponse:
    return JobResponse.from_snapshot(service.get(job_id, principal.user_id))


@router.post("/{job_id}/cancel", response_model=JobResponse)
def cancel_job(
    job_id: str,
    principal: Annotated[AuthPrincipal, Depends(require_csrf)],
    service: Annotated[JobService, Depends(get_job_service)],
) -> JobResponse:
    return JobResponse.from_snapshot(service.cancel(job_id, principal.user_id))


@router.post("/{job_id}/retry", response_model=JobResponse)
def retry_job(
    job_id: str,
    principal: Annotated[AuthPrincipal, Depends(require_csrf)],
    service: Annotated[JobService, Depends(get_job_service)],
) -> JobResponse:
    return JobResponse.from_snapshot(service.retry(job_id, principal.user_id))
