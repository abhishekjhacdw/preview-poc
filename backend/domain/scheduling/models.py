"""Storage-neutral scheduling domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping


class AppointmentStatus(StrEnum):
    """Lifecycle states shown in booking, rescheduling, and schedule views."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class AppointmentRequestStatus(StrEnum):
    """Staff-review states for new-patient appointment requests."""

    PENDING = "pending"
    APPROVED = "approved"
    MODIFICATION_PROPOSED = "modification_proposed"
    MODIFIED = "modified"
    DECLINED = "declined"
    CANCELLED = "cancelled"


class PatientType(StrEnum):
    EXISTING = "existing"
    NEW = "new"


class ReminderConsentStatus(StrEnum):
    NOT_ASKED = "not_asked"
    CONSENTED = "consented"
    DECLINED = "declined"
    REVOKED = "revoked"


class ReminderLinkStatus(StrEnum):
    ACTIVE = "active"
    USED = "used"
    EXPIRED = "expired"
    REVOKED = "revoked"


class ReminderLinkPurpose(StrEnum):
    RESCHEDULE = "reschedule"


class StaffRoleName(StrEnum):
    SCHEDULER = "scheduler"
    CLINICIAN = "clinician"
    ADMIN = "admin"
    READ_ONLY = "read_only"


class AuditActorType(StrEnum):
    PATIENT = "patient"
    STAFF = "staff"
    REMINDER_LINK = "reminder_link"
    SYSTEM = "system"


class AuditAction(StrEnum):
    BOOKING_CREATED = "booking_created"
    REQUEST_SUBMITTED = "request_submitted"
    REQUEST_APPROVED = "request_approved"
    REQUEST_MODIFICATION_PROPOSED = "request_modification_proposed"
    REQUEST_MODIFIED = "request_modified"
    REQUEST_DECLINED = "request_declined"
    APPOINTMENT_RESCHEDULED = "appointment_rescheduled"
    APPOINTMENT_STATUS_UPDATED = "appointment_status_updated"
    SCHEDULE_VIEWED = "schedule_viewed"
    APPOINTMENT_TYPE_UPDATED = "appointment_type_updated"
    REMINDER_CONSENT_RECORDED = "reminder_consent_recorded"
    REMINDER_LINK_CREATED = "reminder_link_created"
    REMINDER_LINK_USED = "reminder_link_used"
    REMINDER_DELIVERY_BLOCKED = "reminder_delivery_blocked"


@dataclass(frozen=True, slots=True)
class PatientContact:
    id: str
    patient_type: PatientType
    first_name: str
    last_name: str
    date_of_birth: date | None
    email: str | None
    phone: str | None
    reminder_consent_status: ReminderConsentStatus
    external_patient_id: str | None = None
    consent_recorded_at: datetime | None = None
    consent_recorded_by: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class AppointmentType:
    id: str
    name: str
    duration_minutes: int
    online_booking_enabled: bool
    new_patient_requests_enabled: bool
    active: bool
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class Provider:
    id: str
    display_name: str
    active: bool = True
    external_provider_id: str | None = None


@dataclass(frozen=True, slots=True)
class Appointment:
    id: str
    patient_contact_id: str
    appointment_type_id: str
    provider_id: str
    provider_display_name: str
    visit_type: str
    start_at: datetime
    end_at: datetime
    timezone: str
    status: AppointmentStatus
    reminder_consent_status: ReminderConsentStatus
    external_appointment_id: str | None = None
    source_request_id: str | None = None
    previous_appointment_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class AppointmentRequest:
    id: str
    patient_contact_id: str
    appointment_type_id: str
    visit_type: str
    status: AppointmentRequestStatus
    requested_start_at: datetime | None = None
    requested_end_at: datetime | None = None
    requested_provider_id: str | None = None
    patient_notes: str | None = None
    staff_decision_by: str | None = None
    staff_decision_at: datetime | None = None
    staff_decision_notes: str | None = None
    proposed_start_at: datetime | None = None
    proposed_end_at: datetime | None = None
    approved_appointment_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ReminderLink:
    id: str
    appointment_id: str
    patient_contact_id: str
    token_hash: str
    purpose: ReminderLinkPurpose
    status: ReminderLinkStatus
    expires_at: datetime
    created_at: datetime
    used_at: datetime | None = None
    revoked_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class StaffRole:
    id: str
    name: StaffRoleName
    permissions: tuple[str, ...]
    description: str | None = None


@dataclass(frozen=True, slots=True)
class StaffUser:
    id: str
    username: str
    email: str
    display_name: str
    role_ids: tuple[str, ...]
    active: bool
    password_hash_reference: str | None = None
    last_login_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class AuditEvent:
    id: str
    actor_type: AuditActorType
    action: AuditAction
    occurred_at: datetime
    actor_id: str | None = None
    actor_display_name: str | None = None
    appointment_id: str | None = None
    appointment_request_id: str | None = None
    patient_contact_id: str | None = None
    staff_user_id: str | None = None
    reminder_link_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    details: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
