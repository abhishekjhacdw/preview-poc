"""Persistence protocols for scheduling data.

These interfaces intentionally avoid ORM, engine, table, and vendor concepts so
the database decision can remain open behind the repository layer.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Protocol, Sequence

from domain.scheduling.models import (
    Appointment,
    AppointmentRequest,
    AppointmentRequestStatus,
    AppointmentStatus,
    AppointmentType,
    AuditAction,
    AuditEvent,
    PatientContact,
    ReminderConsentStatus,
    ReminderLink,
    ReminderLinkStatus,
    StaffRole,
    StaffRoleName,
    StaffUser,
)


class PatientContactRepository(Protocol):
    async def get(self, patient_contact_id: str) -> PatientContact | None:
        """Return one patient contact record by identifier."""

    async def find_by_email(self, email: str) -> Sequence[PatientContact]:
        """Return matching contacts for patient identification workflows."""

    async def save(self, patient_contact: PatientContact) -> PatientContact:
        """Create or update patient contact and reminder consent fields."""

    async def record_reminder_consent(
        self,
        patient_contact_id: str,
        status: ReminderConsentStatus,
        recorded_at: datetime,
        recorded_by: str | None = None,
    ) -> PatientContact:
        """Persist the latest patient email reminder consent decision."""


class AppointmentTypeRepository(Protocol):
    async def get(self, appointment_type_id: str) -> AppointmentType | None:
        """Return one appointment type by identifier."""

    async def list_active(self) -> Sequence[AppointmentType]:
        """Return appointment types available to staff workflows."""

    async def list_online_bookable(self) -> Sequence[AppointmentType]:
        """Return appointment types enabled for patient self-booking."""

    async def save(self, appointment_type: AppointmentType) -> AppointmentType:
        """Create or update appointment type configuration."""

    async def set_online_booking_enabled(
        self, appointment_type_id: str, enabled: bool
    ) -> AppointmentType:
        """Update whether future patient booking may use this visit type."""


class AppointmentRepository(Protocol):
    async def get(self, appointment_id: str) -> Appointment | None:
        """Return one appointment by identifier."""

    async def get_by_external_id(self, external_appointment_id: str) -> Appointment | None:
        """Return an appointment linked to a future scheduling-system record."""

    async def list_for_day(
        self, schedule_date: date, timezone: str | None = None
    ) -> Sequence[Appointment]:
        """Return appointments for staff day schedule views."""

    async def list_by_patient(self, patient_contact_id: str) -> Sequence[Appointment]:
        """Return appointments associated with one patient contact."""

    async def save(self, appointment: Appointment) -> Appointment:
        """Create or update booked appointment details."""

    async def update_status(
        self,
        appointment_id: str,
        status: AppointmentStatus,
        updated_at: datetime,
    ) -> Appointment:
        """Persist status changes shown in schedule workflows."""

    async def reschedule(
        self,
        appointment_id: str,
        start_at: datetime,
        end_at: datetime,
        updated_at: datetime,
    ) -> Appointment:
        """Move an appointment while preserving patient, provider, and visit type."""


class AppointmentRequestRepository(Protocol):
    async def get(self, appointment_request_id: str) -> AppointmentRequest | None:
        """Return one new-patient appointment request by identifier."""

    async def list_by_status(
        self, status: AppointmentRequestStatus
    ) -> Sequence[AppointmentRequest]:
        """Return appointment requests for staff review queues."""

    async def list_for_day(
        self, schedule_date: date, timezone: str | None = None
    ) -> Sequence[AppointmentRequest]:
        """Return pending or decided requests relevant to a schedule date."""

    async def save(self, appointment_request: AppointmentRequest) -> AppointmentRequest:
        """Create or update an appointment request."""

    async def set_status(
        self,
        appointment_request_id: str,
        status: AppointmentRequestStatus,
        decided_by_staff_user_id: str,
        decided_at: datetime,
        notes: str | None = None,
    ) -> AppointmentRequest:
        """Persist approve, modify, decline, and cancellation decisions."""


class ReminderLinkRepository(Protocol):
    async def get(self, reminder_link_id: str) -> ReminderLink | None:
        """Return one reminder link record by identifier."""

    async def get_active_by_token_hash(self, token_hash: str) -> ReminderLink | None:
        """Return an active link without exposing the raw token."""

    async def list_for_appointment(self, appointment_id: str) -> Sequence[ReminderLink]:
        """Return links tied to one appointment."""

    async def save(self, reminder_link: ReminderLink) -> ReminderLink:
        """Create or update appointment-specific reminder link metadata."""

    async def mark_used(
        self, reminder_link_id: str, used_at: datetime
    ) -> ReminderLink:
        """Record successful one-link appointment access or rescheduling."""

    async def set_status(
        self,
        reminder_link_id: str,
        status: ReminderLinkStatus,
        changed_at: datetime,
    ) -> ReminderLink:
        """Expire or revoke a reminder link."""


class StaffRoleRepository(Protocol):
    async def get(self, role_id: str) -> StaffRole | None:
        """Return one staff role by identifier."""

    async def get_by_name(self, name: StaffRoleName) -> StaffRole | None:
        """Return one staff role by stable role name."""

    async def list_all(self) -> Sequence[StaffRole]:
        """Return roles available for role-based access checks."""

    async def save(self, role: StaffRole) -> StaffRole:
        """Create or update a role definition."""


class StaffUserRepository(Protocol):
    async def get(self, staff_user_id: str) -> StaffUser | None:
        """Return one staff user by identifier."""

    async def get_by_username(self, username: str) -> StaffUser | None:
        """Return staff account data for application-managed authentication."""

    async def list_active(self) -> Sequence[StaffUser]:
        """Return active staff users for administration workflows."""

    async def save(self, staff_user: StaffUser) -> StaffUser:
        """Create or update staff account and role assignment metadata."""


class AuditEventRepository(Protocol):
    async def get(self, audit_event_id: str) -> AuditEvent | None:
        """Return one audit event by identifier."""

    async def append(self, audit_event: AuditEvent) -> AuditEvent:
        """Persist an immutable scheduling activity audit event."""

    async def list_for_appointment(self, appointment_id: str) -> Sequence[AuditEvent]:
        """Return audit events linked to an appointment."""

    async def list_for_appointment_request(
        self, appointment_request_id: str
    ) -> Sequence[AuditEvent]:
        """Return audit events linked to an appointment request."""

    async def list_by_action(
        self,
        action: AuditAction,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> Sequence[AuditEvent]:
        """Return audit events for a scheduling action and optional time range."""
