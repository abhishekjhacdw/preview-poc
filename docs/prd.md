# Product Requirements Document (PRD)

> Requirement IDs should remain stable after approval so downstream ARD and feature specifications retain traceability.

## Document Metadata

- **Product/Application:** Online Patient Scheduling and Reminders
- **Document ID:** PRD-OPS
- **Version:** 0.1
- **Status:** Draft
- **Owner:** TBD
- **Contributors:** TBD
- **Last Updated:** 2026-11-12

---

## 1. Executive Summary

The clinic needs an online scheduling experience because patients can currently book only by phone during office hours, causing lost bookings when patients cannot reach staff. The product will let patients book selected appointment types online, allow existing patients to reschedule through secure email reminder links, send email reminders with consent, and give staff a single view of the day’s schedule.

The initial launch approach will start with a staff-only internal rollout, then extend to patient-facing booking and rescheduling. For launch, new patients will submit appointment requests for staff approval, while existing patients can book directly into available selected appointment types.

The expected value is increased completed bookings outside office hours, reduced scheduling friction, and a more modern mobile-first experience for patients and staff while respecting HIPAA obligations.

## 2. Problem Statement

The clinic loses bookings because patients can only book by phone during office hours. Staff report missed calls and voicemail backlog during closed hours, creating friction for patients and administrative work for staff. Existing and new adult patients who want to schedule selected services online are affected, while staff lack a consolidated day schedule view in one place.

## 3. Product Vision

Create a HIPAA-aware, mobile-first online scheduling system where patients can manage selected appointment types without needing to call during office hours, and staff can efficiently review requests, monitor the day’s schedule, and manage appointment status from one place.

## 4. Goals and Success Measures

### 4.1 Goals

- Increase completed bookings outside office hours.
- Reduce patient friction for booking and rescheduling selected appointment types.
- Provide staff with a consolidated day schedule view.
- Send patient email reminders with consent to reduce missed appointments.
- Deliver a modern, mobile-first interface for patients and staff.

### 4.2 Success Measures

| ID | Measure | Baseline | Target | Measurement Method |
|---|---|---:|---:|---|
| KPI-001 | Completed bookings outside office hours | TBD | TBD | Scheduling analytics comparing bookings submitted outside office hours before and after launch |
| KPI-002 | Phone scheduling workload | TBD | TBD | Staff-reported call volume or phone scheduling logs |
| KPI-003 | Email reminder consent capture rate | TBD | TBD | Percentage of online booking or rescheduling flows with recorded reminder consent |

## 5. Scope

### 5.1 In Scope

- Online booking for a limited set of standard appointment types selected by staff.
- Hybrid booking model: new patients submit requests for approval; existing patients book directly.
- Online rescheduling for existing patients up to 24 hours before the appointment through unique email reminder links.
- Email reminders sent only with patient consent.
- Staff approval workflow for new patient appointment requests.
- Staff day schedule view showing patient name, appointment time, provider, visit type, and status.
- Mobile-first responsive UI for patients and staff.
- HIPAA-aligned role-based staff access and scheduling audit logging.

### 5.2 Out of Scope

- Clinical diagnosis, triage, or treatment recommendations.
- Patient self-service for appointment types not selected by staff for launch.
- Online rescheduling less than 24 hours before the appointment.
- Patient account login for launch.
- Final integration model with the current scheduling system until that dependency is decided.

## 6. Personas and Users

### PERSONA-001 — Existing Adult Patient

- **Description:** An adult patient already known to the clinic who wants to schedule or reschedule selected services online.
- **Primary Need:** Book or reschedule without calling during office hours.
- **Key Pain Point:** Phone-only scheduling creates delays when the clinic is closed or lines are busy.

### PERSONA-002 — New Adult Patient

- **Description:** An adult patient seeking care from the clinic for the first time.
- **Primary Need:** Request a selected appointment type online and receive confirmation after staff review.
- **Key Pain Point:** New patients cannot complete scheduling outside office hours today.

### PERSONA-003 — Clinic Scheduling Staff

- **Description:** Clinic staff responsible for managing appointment requests, schedules, and appointment statuses.
- **Primary Need:** See the day’s schedule in one place and process new patient requests efficiently.
- **Key Pain Point:** Missed calls and voicemail backlog create manual follow-up work and lost booking opportunities.

## 7. Assumptions and Dependencies

### Assumptions

- ASM-001 — Patients in launch scope are existing and new adult patients booking selected appointment types.
- ASM-002 — Staff will select the appointment types available for online booking at launch.
- ASM-003 — Patients must consent before receiving email reminders.
- ASM-004 — No patient account login is required for launch; rescheduling access is via unique email reminder links.
- ASM-005 — The initial rollout is staff-only before patient-facing booking is enabled.

### Dependencies

- DEP-001 — Final scheduling system integration approach is TBD.
- DEP-002 — Email delivery capability that can send reminders and support unique rescheduling links.
- DEP-003 — Staff process for approving, modifying, or declining new patient appointment requests.
- DEP-004 — Analytics or reporting capability to measure outside-office-hours completed bookings.

## 8. Functional Requirements

### PRD-FR-001 — Existing Patient Direct Booking

- **Priority:** Must
- **Feature:** FEAT-001
- **Persona:** PERSONA-001

**Requirement**

The system shall allow existing adult patients to directly book available appointment slots for staff-selected appointment types online.

**Business Rationale**

Direct online booking reduces dependence on phone scheduling during office hours and supports the primary goal of increasing completed bookings outside office hours.

**Acceptance Criteria**

1. Existing patients can view available slots only for appointment types selected by staff for online booking.
2. An existing patient can submit a booking outside office hours without staff intervention.
3. A successful booking creates or records an appointment with patient, time, provider, visit type, and status.
4. Appointment types not selected by staff are not available for patient self-booking.

---

### PRD-FR-002 — New Patient Appointment Requests

- **Priority:** Must
- **Feature:** FEAT-001
- **Persona:** PERSONA-002

**Requirement**

The system shall allow new adult patients to submit appointment requests for staff-selected appointment types for staff approval, modification, or decline.

**Business Rationale**

New patients may require staff review before confirmation, while still allowing the clinic to capture demand outside office hours.

**Acceptance Criteria**

1. A new patient can submit a request for a staff-selected appointment type.
2. Submitted new patient requests appear in a pending state for staff review.
3. Staff can approve, modify, or decline a pending new patient request.
4. A new patient request does not become a confirmed appointment until staff approves it.

---

### PRD-FR-003 — Online Rescheduling Through Email Link

- **Priority:** Must
- **Feature:** FEAT-002
- **Persona:** PERSONA-001

**Requirement**

The system shall allow existing patients to reschedule appointments online up to 24 hours before the appointment through unique email reminder links.

**Business Rationale**

Patients need a low-friction way to manage appointments without creating accounts, while HIPAA risk requires controlled access rather than open rescheduling by appointment details alone.

**Acceptance Criteria**

1. A patient can access the rescheduling flow only through a unique appointment-specific email link.
2. Rescheduling is available when the appointment start time is at least 24 hours away.
3. Rescheduling is blocked when the appointment start time is less than 24 hours away.
4. A successful reschedule updates the appointment time while preserving patient, provider, visit type, and status history.

---

### PRD-FR-004 — Email Appointment Reminders

- **Priority:** Must
- **Feature:** FEAT-003
- **Persona:** PERSONA-001

**Requirement**

The system shall send email appointment reminders only to patients who have provided reminder consent.

**Business Rationale**

Email reminders support appointment attendance while respecting patient consent requirements in a healthcare context.

**Acceptance Criteria**

1. The system records whether a patient has consented to email reminders.
2. The system sends appointment reminder emails only when email consent is recorded.
3. Reminder emails include a unique rescheduling link when online rescheduling is allowed.
4. Patients without recorded email reminder consent do not receive reminder emails.

---

### PRD-FR-005 — Staff Day Schedule View

- **Priority:** Must
- **Feature:** FEAT-004
- **Persona:** PERSONA-003

**Requirement**

The system shall provide staff with a single day schedule view showing all appointments for the day with patient name, time, provider, visit type, and status.

**Business Rationale**

Staff need a consolidated operational view to manage the day’s schedule and reduce manual coordination.

**Acceptance Criteria**

1. Staff can view all appointments scheduled for a selected day in one place.
2. Each appointment row shows patient name, appointment time, provider, visit type, and status.
3. Staff can distinguish pending new patient requests from confirmed appointments.
4. The day schedule view is usable on mobile and desktop screen sizes.

---

### PRD-FR-006 — Staff Appointment Type Selection

- **Priority:** Must
- **Feature:** FEAT-005
- **Persona:** PERSONA-003

**Requirement**

The system shall allow staff to define which appointment types are available for online patient booking.

**Business Rationale**

The clinic wants online booking at launch for a limited set of standard visit types selected by staff, not all appointment types.

**Acceptance Criteria**

1. Staff can mark appointment types as available or unavailable for online booking.
2. Patient booking flows display only appointment types marked available for online booking.
3. Changes to appointment type availability affect future patient booking options.

## 9. Non-Functional Requirements

### PRD-NFR-001 — HIPAA-Aligned Access Control and Audit Logging

- **Category:** Compliance
- **Priority:** Must

**Requirement**

The system shall enforce role-based staff access and maintain audit logs for scheduling activity involving patient appointment information.

**Acceptance Criteria**

1. Staff users can access scheduling information only through assigned roles.
2. The system records audit events for booking, rescheduling, approval, modification, decline, and schedule-view access.
3. Audit events include actor, action, affected appointment or request, and timestamp.

### PRD-NFR-002 — Secure Reminder Link Handling

- **Category:** Security
- **Priority:** Must

**Requirement**

The system shall use unique appointment-specific email links for no-login rescheduling and prevent unauthorized reuse beyond the intended appointment context.

**Acceptance Criteria**

1. Each reminder email contains a unique link tied to a specific appointment.
2. A rescheduling link cannot be used to access appointments other than the linked appointment.
3. Attempts to use an invalid or expired link do not expose patient appointment details.

### PRD-NFR-003 — Mobile-First Responsive UI

- **Category:** Accessibility
- **Priority:** Must

**Requirement**

The system shall provide a mobile-first responsive interface for patient and staff scheduling workflows.

**Acceptance Criteria**

1. Patient booking, rescheduling, and reminder consent flows can be completed on mobile screen sizes.
2. Staff can view the day schedule on mobile and desktop screen sizes without losing required appointment fields.
3. UI layout adapts to screen size without horizontal scrolling in primary workflows.

### PRD-NFR-004 — Email Reminder Privacy

- **Category:** Privacy
- **Priority:** Must

**Requirement**

The system shall minimize patient information exposed in reminder emails while still enabling appointment reminder and rescheduling functionality.

**Acceptance Criteria**

1. Reminder emails do not include diagnosis, triage, or treatment recommendation content.
2. Reminder emails include only the information needed to identify the appointment and access the rescheduling flow.
3. Reminder emails are sent only to the email address associated with the consenting patient record or appointment request.

## 10. User Journeys

### JOURNEY-001 — Existing Patient Books Online

1. Existing adult patient opens the online scheduling experience.
2. Patient selects an appointment type available for online booking.
3. Patient selects an available appointment slot.
4. System confirms the booking and records appointment details.
5. Patient can receive email reminders if consent is recorded.

**Related Requirements:** PRD-FR-001, PRD-FR-004, PRD-FR-006, PRD-NFR-003

### JOURNEY-002 — New Patient Requests Appointment

1. New adult patient opens the online scheduling experience.
2. Patient selects an appointment type available for new patient requests.
3. Patient submits an appointment request.
4. Staff reviews the pending request.
5. Staff approves, modifies, or declines the request.

**Related Requirements:** PRD-FR-002, PRD-FR-005, PRD-FR-006, PRD-NFR-001

### JOURNEY-003 — Existing Patient Reschedules Through Reminder Email

1. Patient receives an email reminder after giving consent.
2. Patient opens the unique rescheduling link.
3. System verifies the link is valid for the appointment.
4. Patient selects a new available appointment time at least 24 hours before the original appointment.
5. System updates the appointment and records the scheduling activity.

**Related Requirements:** PRD-FR-003, PRD-FR-004, PRD-NFR-001, PRD-NFR-002, PRD-NFR-004

### JOURNEY-004 — Staff Reviews Day Schedule

1. Staff opens the staff scheduling interface.
2. Staff selects the current day or another date.
3. System displays all appointments with patient name, time, provider, visit type, and status.
4. Staff uses appointment status and pending request information to manage the day.

**Related Requirements:** PRD-FR-005, PRD-NFR-001, PRD-NFR-003

## 11. Feature Breakdown

### FEAT-001 — Patient Online Booking and Requests

- **Summary:** Enables existing patients to book directly and new patients to submit staff-reviewed appointment requests for selected appointment types.
- **Priority:** Must
- **Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-006, PRD-NFR-003
- **Expected Spec File:** `specs/FEAT-001-patient-online-booking-and-requests.spec.md`

### FEAT-002 — Patient Online Rescheduling

- **Summary:** Enables existing patients to reschedule through unique email reminder links up to 24 hours before the appointment.
- **Priority:** Must
- **Related Requirements:** PRD-FR-003, PRD-NFR-002, PRD-NFR-004
- **Expected Spec File:** `specs/FEAT-002-patient-online-rescheduling.spec.md`

### FEAT-003 — Email Appointment Reminders

- **Summary:** Sends email reminders to patients who have provided consent and includes secure rescheduling access when eligible.
- **Priority:** Must
- **Related Requirements:** PRD-FR-004, PRD-NFR-002, PRD-NFR-004
- **Expected Spec File:** `specs/FEAT-003-email-appointment-reminders.spec.md`

### FEAT-004 — Staff Day Schedule View

- **Summary:** Gives staff a consolidated daily appointment view with required operational appointment details.
- **Priority:** Must
- **Related Requirements:** PRD-FR-005, PRD-NFR-001, PRD-NFR-003
- **Expected Spec File:** `specs/FEAT-004-staff-day-schedule-view.spec.md`

### FEAT-005 — Appointment Type Controls

- **Summary:** Allows staff to control which appointment types appear in online patient booking flows.
- **Priority:** Must
- **Related Requirements:** PRD-FR-006, PRD-FR-001, PRD-FR-002
- **Expected Spec File:** `specs/FEAT-005-appointment-type-controls.spec.md`

## 12. Constraints

- CON-001 — The company is a small business, so the solution should avoid unnecessary operational complexity.
- CON-002 — The clinic operates in healthcare and must account for HIPAA compliance obligations.
- CON-003 — Email reminders require patient consent before sending.
- CON-004 — Existing patients may reschedule online only up to 24 hours before the appointment.
- CON-005 — Patient-facing launch depends on the staff-only internal rollout completing first.
- CON-006 — The final dependency on the clinic’s scheduling system is not decided.

## 13. Risks

| ID | Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| RISK-001 | No-login rescheduling could expose patient appointment information if links are mishandled | High | Medium | Use unique appointment-specific email links, restrict access to the linked appointment, and audit scheduling activity |
| RISK-002 | Scheduling system integration approach is undecided | High | Medium | Track as an open dependency and design workflows that can support either integration or manual reconciliation until decided |
| RISK-003 | Staff-only rollout may delay patient-facing booking benefits | Medium | Medium | Define staff rollout as a release phase and require patient-facing readiness criteria before full launch |
| RISK-004 | Success metrics cannot be validated until analytics baseline and targets are defined | Medium | High | Establish analytics setup and baseline measurement before evaluating launch success |

## 14. Open Questions

| ID | Question | Owner | Status | Decision/Due Date |
|---|---|---|---|---|
| OQ-001 | What are the baseline and target values for completed bookings outside office hours? | Product Owner | Open | TBD |
| OQ-002 | What are the baseline and target values for phone scheduling workload reduction? | Product Owner | Open | TBD |
| OQ-003 | What are the baseline and target values for email reminder consent capture rate? | Product Owner | Open | TBD |
| OQ-004 | What scheduling system, EHR, practice management system, or manual process will the product depend on at launch? | Product Owner | Open | TBD |
| OQ-005 | What is the target release date for staff-only rollout and patient-facing launch? | Product Owner | Open | TBD |
| OQ-006 | Which exact appointment types and providers are included in the initial staff-only and patient-facing launch? | Clinic Operations | Open | TBD |
| OQ-007 | Are caregivers, minors, or proxy schedulers in scope after adult patient launch? | Product Owner | Open | TBD |

## 15. Release and Rollout Considerations

- **Target Release:** TBD
- **Rollout Approach:** Staff-only internal rollout first, then patient booking and rescheduling later.
- **Migration Considerations:** Existing scheduling data migration or synchronization approach is TBD because the current scheduling system dependency is not decided.
- **Training/Support Considerations:** Staff need training for the day schedule view, appointment type controls, and approval/modification/decline workflow for new patient requests.

## 16. Definition of Product Success

The product is successful when:

- Completed bookings outside office hours increase against the clinic-defined baseline and target.
- Existing adult patients can directly book selected appointment types online.
- New adult patients can submit appointment requests that staff can approve, modify, or decline.
- Staff can view the day’s schedule in one place with patient name, time, provider, visit type, and status.
- Email reminders are sent only with patient consent.
- All Must-priority requirements are accepted.
- Required quality, security, and compliance outcomes are evidenced.

## 17. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Product Owner | TBD | Pending | TBD |
| Business Sponsor | TBD | Pending | TBD |