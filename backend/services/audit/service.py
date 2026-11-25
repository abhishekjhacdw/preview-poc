"""Audit logging service for scheduling workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4

from domain.scheduling.models import AuditAction, AuditActorType, AuditEvent
from repositories.interfaces import AuditEventRepository


@dataclass(frozen=True, slots=True)
class AuditActor:
    """The accountable identity responsible for an audited action."""

    actor_type: AuditActorType
    actor_id: str | None = None
    display_name: str | None = None

    def __post_init__(self) -> None:
        if self.actor_type is AuditActorType.STAFF and not self.actor_id:
            raise ValueError("staff audit actors must include a unique actor_id")


@dataclass(frozen=True, slots=True)
class AuditEntityContext:
    """Scheduling entity identifiers affected by an audited action."""

    appointment_id: str | None = None
    appointment_request_id: str | None = None
    patient_contact_id: str | None = None
    staff_user_id: str | None = None
    reminder_link_id: str | None = None

    def __post_init__(self) -> None:
        if not any(
            (
                self.appointment_id,
                self.appointment_request_id,
                self.patient_contact_id,
                self.staff_user_id,
                self.reminder_link_id,
            )
        ):
            raise ValueError("audit entity context must identify at least one entity")


@dataclass(frozen=True, slots=True)
class AuditRequestContext:
    """Optional request metadata that helps reconstruct staff access activity."""

    ip_address: str | None = None
    user_agent: str | None = None
    details: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))


class AuditLoggingService:
    """Creates immutable audit events and delegates persistence to a repository."""

    def __init__(self, repository: AuditEventRepository) -> None:
        self._repository = repository

    async def record(
        self,
        *,
        actor: AuditActor,
        action: AuditAction,
        entity_context: AuditEntityContext,
        occurred_at: datetime | None = None,
        request_context: AuditRequestContext | None = None,
    ) -> AuditEvent:
        """Record one audit event for a scheduling workflow action."""

        timestamp = occurred_at or datetime.now(UTC)
        if timestamp.tzinfo is None:
            raise ValueError("audit timestamps must be timezone-aware")

        context = request_context or AuditRequestContext()
        event = AuditEvent(
            id=str(uuid4()),
            actor_type=actor.actor_type,
            actor_id=actor.actor_id,
            actor_display_name=actor.display_name,
            action=action,
            occurred_at=timestamp,
            appointment_id=entity_context.appointment_id,
            appointment_request_id=entity_context.appointment_request_id,
            patient_contact_id=entity_context.patient_contact_id,
            staff_user_id=entity_context.staff_user_id,
            reminder_link_id=entity_context.reminder_link_id,
            ip_address=context.ip_address,
            user_agent=context.user_agent,
            details=MappingProxyType(dict(context.details)),
        )
        return await self._repository.append(event)
