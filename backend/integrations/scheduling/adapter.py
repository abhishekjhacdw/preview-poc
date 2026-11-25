"""Scheduling-system adapter contract.

The final EHR or practice-management dependency is intentionally undecided.
Implementations should keep vendor-specific records, payloads, and exceptions
behind this boundary and return normalized scheduling domain objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Protocol, Sequence, runtime_checkable

from domain.scheduling.models import Appointment, AppointmentRequest, AppointmentType


class SchedulingAdapterError(Exception):
    """Base error for failures inside a scheduling-system adapter."""


class SchedulingAdapterUnavailableError(SchedulingAdapterError):
    """Raised when the scheduling system cannot be reached."""


class SchedulingAdapterConflictError(SchedulingAdapterError):
    """Raised when an appointment command conflicts with schedule capacity."""


class SchedulingAdapterValidationError(SchedulingAdapterError):
    """Raised when an adapter rejects a normalized scheduling command."""


@dataclass(frozen=True, slots=True)
class AvailabilityQuery:
    appointment_type_id: str
    start_at: datetime
    end_at: datetime
    timezone: str
    provider_id: str | None = None


@dataclass(frozen=True, slots=True)
class AvailableSlot:
    start_at: datetime
    end_at: datetime
    provider_id: str
    provider_display_name: str
    appointment_type_id: str
    timezone: str


@dataclass(frozen=True, slots=True)
class AvailabilityResult:
    query: AvailabilityQuery
    slots: Sequence[AvailableSlot] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class AppointmentUpdate:
    appointment_id: str
    start_at: datetime | None = None
    end_at: datetime | None = None
    provider_id: str | None = None
    status: str | None = None


@dataclass(frozen=True, slots=True)
class DaySchedule:
    schedule_date: date
    timezone: str | None
    appointments: Sequence[Appointment] = field(default_factory=tuple)
    appointment_requests: Sequence[AppointmentRequest] = field(default_factory=tuple)


@runtime_checkable
class SchedulingAdapter(Protocol):
    """Replaceable scheduling-system operations used by the domain service."""

    async def availability(self, query: AvailabilityQuery) -> AvailabilityResult:
        """Return normalized available slots for an appointment type."""

    async def create_appointment(self, appointment: Appointment) -> Appointment:
        """Create or reserve an appointment in the active scheduling system."""

    async def update_appointment(self, update: AppointmentUpdate) -> Appointment:
        """Update appointment details in the active scheduling system."""

    async def get_day_schedule(
        self, schedule_date: date, timezone: str | None = None
    ) -> DaySchedule:
        """Return the normalized staff-facing schedule for one day."""

    async def set_appointment_type_online_availability(
        self, appointment_type_id: str, enabled: bool
    ) -> AppointmentType:
        """Change future online availability for an appointment type."""
