"""Explicit request and safe identity response contracts for authentication."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)

    username: str = Field(min_length=1, max_length=255)
    password: SecretStr


class ChangePasswordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)

    current_password: SecretStr
    new_password: SecretStr


class AuthenticatedIdentityResponse(BaseModel):
    id: int
    username: str
    display_name: str
    email: str | None
    role_id: int
    role_name: str
    must_change_password: bool
    session_correlation_id: str
    session_expires_at: datetime
