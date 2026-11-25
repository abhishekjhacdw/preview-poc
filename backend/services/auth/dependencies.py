"""FastAPI dependencies for future staff-protected endpoints."""

from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, Request, status

from domain.scheduling.models import StaffRoleName
from services.auth.service import (
    AuthenticationNotConfiguredError,
    StaffAuthenticationProvider,
    StaffAuthorizationService,
    StaffPrincipal,
)


def get_staff_authentication_provider(request: Request) -> StaffAuthenticationProvider:
    provider = getattr(request.app.state, "staff_authentication_provider", None)
    if provider is None:
        raise AuthenticationNotConfiguredError("staff authentication provider is not configured")
    return provider


def get_staff_authorization_service(request: Request) -> StaffAuthorizationService:
    service = getattr(request.app.state, "staff_authorization_service", None)
    if service is None:
        raise AuthenticationNotConfiguredError("staff authorization service is not configured")
    return service


async def get_current_staff_principal(
    authorization: str | None = Header(default=None),
    provider: StaffAuthenticationProvider = Depends(get_staff_authentication_provider),
    authorization_service: StaffAuthorizationService = Depends(get_staff_authorization_service),
) -> StaffPrincipal:
    staff_user = await provider.authenticate_request(authorization)
    if staff_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Staff authentication is required",
        )

    try:
        return await authorization_service.build_principal(staff_user)
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


def require_staff_roles(
    *allowed_roles: StaffRoleName,
) -> Callable[[StaffPrincipal, StaffAuthorizationService], StaffPrincipal]:
    if not allowed_roles:
        raise ValueError("at least one allowed staff role is required")

    def dependency(
        principal: StaffPrincipal = Depends(get_current_staff_principal),
        authorization_service: StaffAuthorizationService = Depends(
            get_staff_authorization_service
        ),
    ) -> StaffPrincipal:
        try:
            return authorization_service.require_roles(principal, allowed_roles)
        except PermissionError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(exc),
            ) from exc

    return dependency
