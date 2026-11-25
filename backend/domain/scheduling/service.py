"""Scheduling domain service boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from integrations.scheduling.adapter import (
    AppointmentUpdate,
    AvailabilityQuery,
    AvailabilityResult,
    DaySchedule,
    SchedulingAdapter,
    SchedulingAdapterConflictError,
    SchedulingAdapterError,
    SchedulingAdapterUnavailableError,
    SchedulingAdapterValidationError,
)
from domain.scheduling.models import Appointment, AppointmentType
from repositories.interfaces import (
    AppointmentRepository,
    AppointmentRequestRepository,
    AppointmentTypeRepository,
    PatientContactRepository,
)


class SchedulingServiceError(Exception):
    """Base domain-safe scheduling service error."""


class SchedulingServiceUnavailableError(SchedulingServiceError):
    """Raised when scheduling operations are temporarily unavailable."""


class SchedulingConflictError(SchedulingServiceError):
    """Raised when a scheduling command conflicts with current availability."""


class SchedulingValidationError(SchedulingServiceError):
    """Raised when a scheduling command cannot be accepted."""


@dataclass(frozen=True, slots=True)
class SchedulingServiceRepositories:
    patient_contacts: PatientContactRepository
    appointment_types: AppointmentTypeRepository
    appointments: AppointmentRepository
    appointment_requests: AppointmentRequestRepository


class SchedulingService:
    """Coordinates scheduling workflows through repositories and an adapter."""

    def __init__(
        self,
        repositories: SchedulingServiceRepositories,
        scheduling_adapter: SchedulingAdapter,
    ) -> None:
        self._repositories = repositories
        self._scheduling_adapter = scheduling_adapter

    async def availability(self, query: AvailabilityQuery) -> AvailabilityResult:
        try:
            return await self._scheduling_adapter.availability(query)
        except SchedulingAdapterError as exc:
            raise self._to_domain_error(exc) from None

    async def create_appointment(self, appointment: Appointment) -> Appointment:
        try:
            created = await self._scheduling_adapter.create_appointment(appointment)
        except SchedulingAdapterError as exc:
            raise self._to_domain_error(exc) from None

        return await self._repositories.appointments.save(created)

    async def update_appointment(self, update: AppointmentUpdate) -> Appointment:
        try:
            updated = await self._scheduling_adapter.update_appointment(update)
        except SchedulingAdapterError as exc:
            raise self._to_domain_error(exc) from None

        return await self._repositories.appointments.save(updated)

    async def get_day_schedule(
        self, schedule_date: date, timezone: str | None = None
    ) -> DaySchedule:
        try:
            return await self._scheduling_adapter.get_day_schedule(
                schedule_date, timezone=timezone
            )
        except SchedulingAdapterError as exc:
            raise self._to_domain_error(exc) from None

    async def set_appointment_type_online_availability(
        self, appointment_type_id: str, enabled: bool
    ) -> AppointmentType:
        try:
            await self._scheduling_adapter.set_appointment_type_online_availability(
                appointment_type_id, enabled
            )
        except SchedulingAdapterError as exc:
            raise self._to_domain_error(exc) from None

        return await self._repositories.appointment_types.set_online_booking_enabled(
            appointment_type_id, enabled
        )

    @staticmethod
    def _to_domain_error(error: SchedulingAdapterError) -> SchedulingServiceError:
        if isinstance(error, SchedulingAdapterUnavailableError):
            return SchedulingServiceUnavailableError(
                "Scheduling is temporarily unavailable."
            )
        if isinstance(error, SchedulingAdapterConflictError):
            return SchedulingConflictError(
                "The requested scheduling change is no longer available."
            )
        if isinstance(error, SchedulingAdapterValidationError):
            return SchedulingValidationError(
                "The requested scheduling change could not be accepted."
            )
        return SchedulingServiceError("Scheduling could not be completed.")
