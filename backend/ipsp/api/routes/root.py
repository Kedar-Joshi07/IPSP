"""Versioned API root route."""

from fastapi import APIRouter, Request

from ipsp.api.schemas.common import ApiInfoResponse
from ipsp.config.settings import Settings

router = APIRouter()


@router.get("", response_model=ApiInfoResponse, include_in_schema=False)
@router.get("/", response_model=ApiInfoResponse)
def api_root(request: Request) -> ApiInfoResponse:
    """Describe the implemented API foundation without business output."""
    settings: Settings = request.app.state.settings
    return ApiInfoResponse(name=settings.app_name, version=settings.app_version)
