import asyncio
from datetime import UTC, datetime
from typing import Sequence

import pytest

from domain.scheduling.models import (
    AuditAction,
    AuditActorType,
    AuditEvent,
    StaffRole,
    StaffRoleName,
    StaffUser,
)
from services.audit.service import (
    AuditActor,
    AuditEntityContext,
    AuditLoggingService,
)
from services.auth.service import StaffAuthorizationService


class InMemoryAuditEventRepository:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    async def append(self, audit_event: AuditEvent) -> AuditEvent:
        self.events.append(audit_event)
        return audit_event


class InMemoryStaffRoleRepository:
    def __init__(self, roles: Sequence[StaffRole]) -> None:
        self.roles_by_id = {role.id: role for role in roles}

    async def get(self, role_id: str) -> StaffRole | None:
        return self.roles_by_id.get(role_id)


def test_audit_logging_records_actor_action_entity_context_and_timestamp() -> None:
    repository = InMemoryAuditEventRepository()
    service = AuditLoggingService(repository)
    occurred_at = datetime(2026, 11, 12, 9, 30, tzinfo=UTC)

    event = asyncio.run(
        service.record(
            actor=AuditActor(
                actor_type=AuditActorType.STAFF,
                actor_id="staff-123",
                display_name="Sam Scheduler",
            ),
            action=AuditAction.SCHEDULE_VIEWED,
            entity_context=AuditEntityContext(appointment_id="appt-456"),
            occurred_at=occurred_at,
        )
    )

    assert repository.events == [event]
    assert event.actor_type is AuditActorType.STAFF
    assert event.actor_id == "staff-123"
    assert event.action is AuditAction.SCHEDULE_VIEWED
    assert event.appointment_id == "appt-456"
    assert event.occurred_at == occurred_at


def test_staff_authorization_service_enforces_role_checks() -> None:
    role_repository = InMemoryStaffRoleRepository(
        [
            StaffRole(
                id="role-scheduler",
                name=StaffRoleName.SCHEDULER,
                permissions=("appointments:write",),
            )
        ]
    )
    service = StaffAuthorizationService(role_repository)
    principal = asyncio.run(
        service.build_principal(
            StaffUser(
                id="staff-123",
                username="sam",
                email="sam@example.test",
                display_name="Sam Scheduler",
                role_ids=("role-scheduler",),
                active=True,
            )
        )
    )

    assert service.require_roles(principal, (StaffRoleName.SCHEDULER,)) is principal

    with pytest.raises(PermissionError):
        service.require_roles(principal, (StaffRoleName.ADMIN,))
