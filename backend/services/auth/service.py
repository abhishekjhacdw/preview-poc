"""Pluggable staff authentication and role authorization helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from domain.scheduling.models import StaffRole, StaffRoleName, StaffUser
from repositories.interfaces import StaffRoleRepository


class AuthenticationNotConfiguredError(RuntimeError):
    """Raised when a staff-auth dependency is used before credentials are wired."""


class StaffAuthenticationProvider(Protocol):
    """Swappable staff identity provider.

    MFA, password policy, session timeout, recovery, and lockout controls remain
    outside this foundation and can be implemented behind this protocol.
    """

    async def authenticate_request(self, authorization_header: str | None) -> StaffUser | None:
        """Return the staff user represented by the incoming request, if any."""


@dataclass(frozen=True, slots=True)
class StaffPrincipal:
    """The individual staff account acting on staff-only workflows."""

    user_id: str
    username: str
    display_name: str
    email: str
    roles: tuple[StaffRoleName, ...]
    permissions: frozenset[str]

    @classmethod
    async def from_user(
        cls, user: StaffUser, role_repository: StaffRoleRepository
    ) -> "StaffPrincipal":
        roles: list[StaffRoleName] = []
        permissions: set[str] = set()

        for role_id in user.role_ids:
            role = await role_repository.get(role_id)
            if role is None:
                continue
            roles.append(role.name)
            permissions.update(role.permissions)

        return cls(
            user_id=user.id,
            username=user.username,
            display_name=user.display_name,
            email=user.email,
            roles=tuple(roles),
            permissions=frozenset(permissions),
        )


class StaffAuthorizationService:
    """Authorizes staff principals against role and permission requirements."""

    def __init__(self, role_repository: StaffRoleRepository) -> None:
        self._role_repository = role_repository

    async def build_principal(self, staff_user: StaffUser) -> StaffPrincipal:
        if not staff_user.active:
            raise PermissionError("inactive staff users cannot access staff workflows")
        return await StaffPrincipal.from_user(staff_user, self._role_repository)

    def require_roles(
        self, principal: StaffPrincipal, allowed_roles: Sequence[StaffRoleName]
    ) -> StaffPrincipal:
        allowed_role_set = set(allowed_roles)
        if not allowed_role_set:
            raise ValueError("at least one allowed staff role is required")
        if allowed_role_set.isdisjoint(principal.roles):
            raise PermissionError("staff role is not authorized for this workflow")
        return principal

    def require_permissions(
        self, principal: StaffPrincipal, required_permissions: Sequence[str]
    ) -> StaffPrincipal:
        missing = set(required_permissions).difference(principal.permissions)
        if missing:
            raise PermissionError("staff permissions are not authorized for this workflow")
        return principal
