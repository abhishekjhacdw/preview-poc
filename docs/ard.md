# Architecture Requirements Document (ARD)

> Every material architecture decision or constraint has a stable ID that feature specifications can reference.

## Document Metadata

- **Product/Application:** Online Patient Scheduling and Reminders
- **Document ID:** ARD-OPS
- **Version:** 0.1
- **Status:** Draft
- **Architecture Owner:** TBD
- **Contributors:** TBD
- **Last Updated:** 2026-11-12
- **Reference PRD:** `PRD.md`

---

## 1. Architecture Summary

The architecture is a mobile-first React single-page application backed by a Python/FastAPI REST API. The backend separates presentation APIs, scheduling orchestration, domain rules, integration adapters, repository interfaces, reminder generation, staff access control, and audit logging.

The design is adapter-based because the clinic’s final scheduling/EHR/practice-management dependency is not yet decided. The system supports a standalone launch path first, while preserving a migration path to a future scheduling-system integration without rewriting booking, request, rescheduling, reminder, and staff schedule workflows.

Because the clinic is in healthcare and subject to HIPAA obligations, the architecture requires HIPAA-eligible managed hosting with a signed BAA, role-based staff access, scheduling audit logs, privacy-minimized reminder content, unique appointment-specific rescheduling links, and a release gate that blocks reminder sending until a compliant email sending mechanism is selected.

## 2. Architecture Drivers

- PRD-FR-001 — Existing adult patients must directly book staff-selected appointment types online.
- PRD-FR-002 — New adult patients must submit appointment requests for staff approval, modification, or decline.
- PRD-FR-003 — Existing patients must reschedule through unique email reminder links up to 24 hours before the appointment.
- PRD-FR-004 — Email reminders must be sent only with patient consent.
- PRD-FR-005 — Staff must see the day’s schedule with patient name, time, provider, visit type, and status.
- PRD-FR-006 — Staff must control which appointment types are available for online booking.
- PRD-NFR-001 — Staff access must be role-based and scheduling activity must be audit logged.
- PRD-NFR-002 — Reminder links must be unique, appointment-specific, and resistant to unauthorized reuse.
- PRD-NFR-003 — Patient and staff workflows must be mobile-first and responsive.
- PRD-NFR-004 — Reminder emails must minimize exposed patient information.
- CON-001 — The company is a small business, so the solution should avoid unnecessary operational complexity.
- CON-002 — The clinic operates in healthcare and must account for HIPAA compliance obligations.
- CON-003 — Email reminders require patient consent before sending.
- CON-004 — Existing patients may reschedule online only up to 24 hours before the appointment.
- CON-005 — Patient-facing launch depends on the staff-only internal rollout completing first.
- CON-006 — The final dependency on the clinic’s scheduling system is not decided.

## 3. Architecture Principles

1. Minimize PHI exposure across UI, APIs, logs, reminders, and integrations.
2. Isolate scheduling-system dependencies behind adapters until the final EHR/practice-management integration decision is made.
3. Reuse established repository and platform patterns where appropriate.
4. Keep presentation, orchestration, domain, integration, and persistence concerns separated.
5. Prefer managed HIPAA-eligible services with BAA support over self-managed infrastructure.
6. Block patient-facing capabilities that depend on unresolved compliance-critical services until those services are approved.

## 4. System Context

### 4.1 Actors

- Existing Adult Patient — Books selected appointment types directly and reschedules eligible appointments through unique email links.
- New Adult Patient — Submits appointment requests for staff approval, modification, or decline.
- Clinic Scheduling Staff — Reviews the day schedule, manages appointment requests, controls online appointment types, and updates appointment status.
- Clinic Operations — Selects launch appointment types and providers and owns scheduling process decisions.
- Product Owner — Owns open product metrics, launch timing, and unresolved scheduling dependency decisions.
- Security Reviewer — Owns HIPAA security review, scanning policy, SBOM policy, and unresolved authentication controls.
- Future Scheduling/EHR/Practice-Management System — Potential external system for appointment availability, booking, and reconciliation once selected.

### 4.2 External Systems

| ID | System | Purpose | Interface | Owner |
|---|---|---|---|---|
| EXT-001 | Clinic scheduling/EHR/practice-management system | Future source or synchronization target for schedules, availability, and appointments | REST/Event/File/TBD | Product Owner / Clinic Operations |
| EXT-002 | Email sending mechanism | Sends consent-based appointment reminders and appointment-specific rescheduling links | REST/SMTP/TBD | Product Owner / Security Reviewer |
| EXT-003 | HIPAA-eligible managed cloud platform | Hosts application components under BAA-backed managed services | Managed platform interfaces | Engineering Lead / Security Reviewer |

## 5. Technology Stack

| Layer | Technology | Version/Constraint | Rationale |
|---|---|---|---|
| Frontend | React SPA | Version TBD | Supports mobile-first patient and staff workflows with a separate frontend and REST API backend.
| Backend | Python/FastAPI REST API | Python and FastAPI versions TBD | Provides REST API boundary, validation, domain orchestration, and adapter-based integrations.
| Data | Repository interfaces over storage technology TBD | Database choice TBD | User selected TBD database choice; repository interfaces preserve portability while data architecture is unresolved.
| Hosting | HIPAA-eligible managed cloud services | Signed BAA required; provider TBD | Satisfies healthcare/HIPAA posture while minimizing operational burden for a small business.

## 6. Logical Architecture

### 6.1 Components

#### COMP-001 — React Scheduling SPA

- **Responsibility:** Provides mobile-first patient booking, rescheduling, reminder consent, staff schedule, staff request review, and appointment type control screens.
- **Inputs:** Patient selections, staff actions, reminder link tokens, schedule filters.
- **Outputs:** REST API requests and rendered workflow state.
- **Dependencies:** COMP-002.
- **Repository Area:** `frontend/` or TBD.

#### COMP-002 — FastAPI REST API

- **Responsibility:** Exposes authenticated and token-based REST endpoints, validates requests, enforces workflow boundaries, and delegates to domain services.
- **Inputs:** REST requests from COMP-001 and scheduled/internal job calls.
- **Outputs:** REST responses, domain commands, audit events.
- **Dependencies:** COMP-003, COMP-006, COMP-007, COMP-008.
- **Repository Area:** `backend/api/` or TBD.

#### COMP-003 — Scheduling Domain Service

- **Responsibility:** Owns booking, new patient request, approval, modification, decline, rescheduling eligibility, appointment type availability, and schedule view rules.
- **Inputs:** Booking commands, request commands, rescheduling commands, staff actions.
- **Outputs:** Appointment records, request records, state transitions, validation errors.
- **Dependencies:** COMP-004, COMP-005, COMP-007.
- **Repository Area:** `backend/domain/scheduling/` or TBD.

#### COMP-004 — Scheduling Integration Adapter

- **Responsibility:** Provides a stable interface for standalone scheduling data at launch and future clinic scheduling/EHR/practice-management integration.
- **Inputs:** Availability queries, booking commands, update commands, schedule queries.
- **Outputs:** Availability, appointment confirmations, synchronization results.
- **Dependencies:** COMP-005, EXT-001 when selected.
- **Repository Area:** `backend/integrations/scheduling/` or TBD.

#### COMP-005 — Repository Layer

- **Responsibility:** Defines persistence interfaces for appointments, requests, appointment types, consent, reminder links, staff users/roles, and audit events while the database choice is TBD.
- **Inputs:** Repository reads/writes from domain services.
- **Outputs:** Persisted entities and query results.
- **Dependencies:** Database technology TBD.
- **Repository Area:** `backend/repositories/` or TBD.

#### COMP-006 — Reminder Service

- **Responsibility:** Determines reminder eligibility, creates appointment-specific rescheduling links, and blocks delivery until the compliant email sending mechanism is selected.
- **Inputs:** Appointment data, consent state, reminder schedules.
- **Outputs:** Reminder send requests, link records, blocked-delivery events.
- **Dependencies:** COMP-005, COMP-007, EXT-002.
- **Repository Area:** `backend/services/reminders/` or TBD.

#### COMP-007 — Audit Logging Service

- **Responsibility:** Records scheduling activity audit events with actor, action, affected appointment or request, and timestamp.
- **Inputs:** Domain events and staff/patient/token context.
- **Outputs:** Audit records.
- **Dependencies:** COMP-005.
- **Repository Area:** `backend/services/audit/` or TBD.

#### COMP-008 — Staff Authentication and Authorization Service

- **Responsibility:** Provides application-managed staff identity, role-based access checks, session handling, and unresolved clinic-policy authentication controls.
- **Inputs:** Staff credentials, staff sessions, role assignments.
- **Outputs:** Authenticated staff context and authorization decisions.
- **Dependencies:** COMP-005, COMP-007.
- **Repository Area:** `backend/services/auth/` or TBD.

#### COMP-009 — Observability and Operations Layer

- **Responsibility:** Provides TBD logging, metrics, tracing, alerting, and baseline capture capabilities once operations model is decided.
- **Inputs:** Application events, errors, audit-safe operational telemetry.
- **Outputs:** Operational logs, metrics, traces, alerts, baseline reports.
- **Dependencies:** Hosting/observability tooling TBD.
- **Repository Area:** `ops/` or TBD.

### 6.2 Data Flow

1. Existing Adult Patient uses COMP-001 to select a staff-enabled appointment type and available slot.
2. COMP-001 sends the booking request to COMP-002.
3. COMP-002 validates the request and calls COMP-003.
4. COMP-003 applies booking rules and uses COMP-004 to query or reserve schedule capacity.
5. COMP-004 reads or writes through COMP-005 in standalone mode, or through EXT-001 when a future integration is selected.
6. COMP-007 records audit events for booking, rescheduling, staff approval, modification, decline, and schedule-view access.
7. COMP-006 creates reminder link records for consenting patients but blocks outbound reminder delivery until EXT-002 is resolved.
8. Staff uses COMP-001 to view the day schedule, process pending requests, and control online appointment types through COMP-002 and COMP-003.

## 7. Architecture Decisions

### ARD-DEC-001 — Separate React SPA and FastAPI REST API

- **Status:** Accepted
- **Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-003, PRD-FR-005, PRD-NFR-003

**Decision**

Use a separate React SPA frontend and Python/FastAPI REST API backend.

**Rationale**

The user selected a separate SPA frontend plus standalone REST API backend and standardized the concrete stack as React plus Python/FastAPI.

**Consequences**

- Supports clear API boundaries between patient/staff UI and backend scheduling services.
- Requires contract management between frontend and backend.
- Requires frontend build, API deployment, and cross-origin/session handling decisions.

**Alternatives Considered**

- Single full-stack web application — Not selected by the user.
- React SPA plus Node.js/TypeScript REST API — Not selected by the user.
- Low-code scheduling platform — Not selected by the user.
- Native mobile apps — Not selected because the PRD requires mobile-first responsive UI, not native apps.

### ARD-DEC-002 — Adapter-Based Scheduling Integration

- **Status:** Accepted
- **Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-003, PRD-FR-005, PRD-FR-006

**Decision**

Implement scheduling access through a Scheduling Integration Adapter that supports standalone launch first and later EHR/practice-management integration without rewriting workflows.

**Rationale**

The final scheduling system dependency is TBD in the PRD, but booking, request, rescheduling, and staff schedule workflows must still be designed.

**Consequences**

- Reduces rework when the final scheduling system is selected.
- Enables staff-only rollout while integration decisions remain open.
- Requires careful interface design for availability, booking, rescheduling, appointment type eligibility, and schedule views.

**Alternatives Considered**

- Integration-first launch blocker — Rejected because patient and staff workflows need architectural progress while the dependency remains undecided.
- Calendar-only integration — Rejected because it does not fully cover clinic appointment workflows.
- Standalone only without adapters — Rejected because future integration is a known dependency.

### ARD-DEC-003 — HIPAA-Eligible Managed Cloud Hosting

- **Status:** Accepted
- **Related Requirements:** PRD-NFR-001, PRD-NFR-002, PRD-NFR-004

**Decision**

Host on HIPAA-eligible managed cloud services with a signed BAA and minimal self-managed infrastructure.

**Rationale**

The clinic operates in healthcare with HIPAA obligations and is a small business, so the architecture should avoid unnecessary operational complexity while preserving compliance posture.

**Consequences**

- Requires vendor eligibility and BAA verification before production use.
- Reduces infrastructure management burden.
- Constrains hosting, logging, email, storage, and monitoring provider choices.

**Alternatives Considered**

- Self-hosted VPS — Rejected due to higher operational burden.
- Generic low-cost SaaS hosting without healthcare controls — Rejected due to HIPAA risk.
- On-premises deployment — Rejected due to operational complexity.

### ARD-DEC-004 — Repository Interfaces Before Database Selection

- **Status:** Accepted
- **Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-003, PRD-FR-004, PRD-FR-005, PRD-FR-006, PRD-NFR-001

**Decision**

Define repository interfaces for scheduling, consent, reminder links, staff users/roles, and audit data while keeping the database technology TBD.

**Rationale**

The user selected TBD database choice with repository interfaces only.

**Consequences**

- Prevents premature database commitment.
- Preserves architectural boundaries for future database selection.
- Requires an open architecture question before production persistence can be finalized.

**Alternatives Considered**

- Relational database with encrypted storage and append-only audit records — Recommended but not selected.
- Document database — Not selected.
- Managed scheduling SaaS as the sole data store — Not selected.

### ARD-DEC-005 — Reminder Delivery Blocked Until Compliant Email Mechanism Is Selected

- **Status:** Accepted
- **Related Requirements:** PRD-FR-004, PRD-NFR-002, PRD-NFR-004

**Decision**

Design reminder generation and reminder-link creation now, but block outbound reminder delivery until a compliant email sending provider or mechanism is selected.

**Rationale**

The approved PRD requires the system to send consent-based email reminders, but the user selected “email sending provider TBD and keep reminder delivery blocked until resolved.”

**Consequences**

- Prevents non-compliant reminder delivery.
- Allows reminder eligibility and link-generation logic to be built and tested before provider selection.
- Creates a launch dependency for PRD-FR-004 acceptance.

**Alternatives Considered**

- HIPAA-eligible transactional email provider with BAA support — Recommended but not selected yet.
- Clinic-owned SMTP configured for application sending — Not selected yet.
- EHR/practice-management email capability — Not selected because EXT-001 is undecided.
- Manual staff sending — Rejected because the PRD requires the system to send reminders.

### ARD-DEC-006 — Application-Managed Staff Authentication With Controls TBD

- **Status:** Proposed
- **Related Requirements:** PRD-NFR-001

**Decision**

Use application-managed staff authentication, with specific password, MFA, session, and account policy controls TBD pending clinic policy and security review.

**Rationale**

The user selected application-managed username/password with optional MFA, then selected that clinic policy decides later and authentication controls remain TBD.

**Consequences**

- Role-based access and audit logging remain mandatory because PRD-NFR-001 requires them.
- Specific login hardening cannot be finalized until clinic policy is decided.
- Security review must resolve whether MFA is mandatory before production launch.

**Alternatives Considered**

- Managed identity provider with MFA — Recommended but not selected.
- Clinic network/VPN only — Not selected.
- Shared staff accounts — Not selected and incompatible with actor-specific audit logging.

## 8. API and Integration Architecture

### ARD-API-001 — Patient Booking API

- **Type:** REST
- **Operation/Topic:** `POST /api/patient/bookings`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** Patient flow access model TBD for booking; no patient account login per PRD scope.
- **Versioning:** URI versioning strategy TBD.

**Request/Input Contract**

Appointment type ID, selected slot, patient identity/contact fields needed to identify an existing adult patient, and reminder consent state where collected.

**Response/Output Contract**

Booking confirmation or validation error; response must include only the minimum appointment information needed for the workflow.

**Error Handling**

Return validation errors for unavailable appointment types, unavailable slots, missing required fields, and unresolved scheduling adapter failures. Idempotency strategy TBD.

### ARD-API-002 — New Patient Appointment Request API

- **Type:** REST
- **Operation/Topic:** `POST /api/patient/appointment-requests`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** Public patient request flow with server-side validation; anti-abuse controls TBD.
- **Versioning:** URI versioning strategy TBD.

**Request/Input Contract**

Requested appointment type, preferred slot or request details, new patient identity/contact fields, and reminder consent where collected.

**Response/Output Contract**

Pending request confirmation; request does not become confirmed appointment until staff approval.

**Error Handling**

Return validation errors for unavailable appointment types and invalid request data. Staff approval conflicts are handled in ARD-API-004.

### ARD-API-003 — Reminder Link Rescheduling API

- **Type:** REST
- **Operation/Topic:** `GET /api/reschedule/{token}` and `POST /api/reschedule/{token}`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** Unique appointment-specific reminder link token.
- **Versioning:** URI versioning strategy TBD.

**Request/Input Contract**

Unique link token and selected replacement slot.

**Response/Output Contract**

Eligible appointment rescheduling state, successful reschedule confirmation, or privacy-preserving invalid/expired/ineligible response.

**Error Handling**

Invalid or expired links must not expose patient appointment details. Rescheduling less than 24 hours before appointment start is blocked. A link cannot access appointments other than the linked appointment.

### ARD-API-004 — Staff Scheduling API

- **Type:** REST
- **Operation/Topic:** `GET /api/staff/schedule?date={date}`, `POST /api/staff/requests/{id}/approve`, `POST /api/staff/requests/{id}/modify`, `POST /api/staff/requests/{id}/decline`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** Application-managed staff authentication with role-based authorization; controls TBD.
- **Versioning:** URI versioning strategy TBD.

**Request/Input Contract**

Staff session context, date filters, request IDs, modification data, approval/decline commands.

**Response/Output Contract**

Day schedule entries with patient name, time, provider, visit type, and status; pending request workflow results.

**Error Handling**

Unauthorized role access is denied and audited. Conflicting staff actions return conflict errors and create audit events where applicable.

### ARD-API-005 — Appointment Type Control API

- **Type:** REST
- **Operation/Topic:** `GET /api/staff/appointment-types` and `PATCH /api/staff/appointment-types/{id}`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** Application-managed staff authentication with role-based authorization; controls TBD.
- **Versioning:** URI versioning strategy TBD.

**Request/Input Contract**

Appointment type ID and online-booking availability flag.

**Response/Output Contract**

Updated appointment type configuration and availability status.

**Error Handling**

Unauthorized changes are denied and audited. Future booking options reflect configuration changes.

### ARD-API-006 — Scheduling Adapter Interface

- **Type:** REST
- **Operation/Topic:** Internal interface: `availability`, `create_appointment`, `update_appointment`, `get_day_schedule`, `set_appointment_type_online_availability`
- **Provider:** COMP-004
- **Consumers:** COMP-003
- **Authentication:** Internal service boundary; external authentication TBD if EXT-001 is selected.
- **Versioning:** Adapter contract versioning TBD.

**Request/Input Contract**

Normalized scheduling domain commands and queries independent of the final scheduling system.

**Response/Output Contract**

Normalized availability, appointment, request, and schedule view results.

**Error Handling**

Adapter errors are mapped to domain-safe API errors. Retry and idempotency rules are TBD pending final integration system.

### ARD-API-007 — Reminder Delivery Interface

- **Type:** REST | SMTP | File
- **Operation/Topic:** TBD provider send operation
- **Provider:** EXT-002
- **Consumers:** COMP-006
- **Authentication:** TBD pending email sending mechanism.
- **Versioning:** TBD pending email sending mechanism.

**Request/Input Contract**

PHI-minimized reminder template data, recipient email for consenting patient, and unique rescheduling link when eligible.

**Response/Output Contract**

Delivery accepted/rejected status and delivery metadata suitable for audit-safe operational tracking.

**Error Handling**

Outbound reminder delivery remains blocked until EXT-002 is resolved. Retry and bounce handling are TBD.

## 9. Data Architecture

### DATA-001 — Appointment

- **Purpose:** Represents booked or rescheduled appointment details shown to patients and staff.
- **System of Record:** Application scheduling repository in standalone mode; future system of record TBD pending EXT-001.
- **Classification:** Restricted
- **Retention:** TBD
- **Key Relationships:** Patient, provider, appointment type, reminder link, audit events.

### DATA-002 — Appointment Request

- **Purpose:** Represents new patient requests pending staff approval, modification, or decline.
- **System of Record:** Application scheduling repository in standalone mode; future system of record TBD pending EXT-001.
- **Classification:** Restricted
- **Retention:** TBD
- **Key Relationships:** New patient contact, appointment type, preferred slot, staff decision, audit events.

### DATA-003 — Appointment Type

- **Purpose:** Defines visit types and whether each type is available for online booking.
- **System of Record:** Application scheduling repository in standalone mode; future system of record TBD pending EXT-001.
- **Classification:** Internal
- **Retention:** TBD
- **Key Relationships:** Appointments, appointment requests, staff configuration audit events.

### DATA-004 — Patient Contact and Reminder Consent

- **Purpose:** Stores patient contact details and whether email reminders are consented.
- **System of Record:** Application repository in standalone mode; future system of record TBD pending EXT-001.
- **Classification:** Restricted
- **Retention:** TBD
- **Key Relationships:** Appointment, appointment request, reminder link, audit events.

### DATA-005 — Reminder Link

- **Purpose:** Stores unique appointment-specific tokens for no-login rescheduling through reminder emails.
- **System of Record:** Application repository.
- **Classification:** Restricted
- **Retention:** TBD
- **Key Relationships:** Appointment, consent state, reminder generation event, audit events.

### DATA-006 — Audit Event

- **Purpose:** Records scheduling activity involving patient appointment information.
- **System of Record:** Application audit repository.
- **Classification:** Restricted
- **Retention:** TBD
- **Key Relationships:** Actor, action, affected appointment or request, timestamp.

### DATA-007 — Staff User and Role

- **Purpose:** Supports application-managed staff authentication and role-based authorization.
- **System of Record:** Application repository.
- **Classification:** Confidential
- **Retention:** TBD
- **Key Relationships:** Role assignments, sessions, audit events.

### Data Migration

- **Required:** TBD
- **Approach:** TBD pending the final scheduling system, database technology, and launch data strategy decisions.

## 10. Security Architecture

### ARD-SEC-001 — HIPAA-Aligned Staff Access and Audit Logging

- **Related Requirements:** PRD-NFR-001

The implementation must:

- Enforce role-based staff access for scheduling information.
- Record audit events for booking, rescheduling, approval, modification, decline, and schedule-view access.
- Include actor, action, affected appointment or request, and timestamp in audit events.
- Support actor-specific auditability for staff actions.

The implementation must not:

- Permit staff access to scheduling information outside assigned roles.
- Rely on shared staff identity for actions requiring actor-specific audit records.
- Store or emit audit logs that omit the action or affected appointment/request context required by PRD-NFR-001.

### ARD-SEC-002 — Secure Reminder Link Handling

- **Related Requirements:** PRD-NFR-002, PRD-NFR-004

The implementation must:

- Generate unique appointment-specific rescheduling links.
- Restrict each reminder link to the linked appointment only.
- Block rescheduling less than 24 hours before the appointment start time.
- Return privacy-preserving responses for invalid or expired links.

The implementation must not:

- Allow a reminder link to access appointments other than the linked appointment.
- Expose patient appointment details when a link is invalid, expired, or unauthorized.
- Include diagnosis, triage, or treatment recommendation content in reminder emails.

### ARD-SEC-003 — Consent-Based Reminder Delivery Gate

- **Related Requirements:** PRD-FR-004, PRD-NFR-004

The implementation must:

- Record email reminder consent before reminder delivery.
- Send reminder emails only after a compliant email sending mechanism is approved.
- Minimize patient information in reminder templates.
- Block outbound reminder delivery while EXT-002 remains TBD.

The implementation must not:

- Send reminder emails without recorded consent.
- Use an email provider or delivery mechanism that has not passed HIPAA/compliance review.
- Send reminders to an email address other than the address associated with the consenting patient record or appointment request.

### ARD-SEC-004 — Security Review, Scanning, and SBOM Policy

- **Related Requirements:** PRD-NFR-001, PRD-NFR-002, PRD-NFR-004

The implementation must:

- Resolve dependency scanning, vulnerability blocking thresholds, container scanning, and SBOM policy before production release.
- Track scanning and SBOM as open security-review items while policy is TBD.

The implementation must not:

- Treat unresolved scanning and SBOM policy as approved for production without Security Reviewer decision.

### Security Controls

- **Authentication:** Application-managed staff username/password selected; MFA, password policy, session timeout, recovery, and lockout controls are TBD pending clinic policy and security review.
- **Authorization:** Role-based staff access is required by PRD-NFR-001.
- **Secrets Management:** TBD pending hosting and operations model; must use HIPAA-eligible managed platform capabilities once selected.
- **Encryption:** In transit and at rest requirements are TBD pending security review and hosting/data store choices.
- **Audit Logging:** Required for booking, rescheduling, approval, modification, decline, and schedule-view access with actor, action, affected appointment/request, and timestamp.
- **Dependency/CVE Scanning:** TBD pending security review.
- **SBOM:** TBD pending security review.

## 11. Reliability, Performance, and Scalability

### ARD-OPS-001 — Availability Baseline

- **Target:** TBD monthly uptime target; owner Engineering Lead / Product Owner.
- **Validation Method:** TBD monitoring and reporting method pending operations model.

### ARD-OPS-002 — API Performance Baseline

- **Target:** TBD response-time target for core scheduling reads and writes; owner Engineering Lead / Product Owner.
- **Validation Method:** TBD load or performance test method pending testing and operations model.

### ARD-OPS-003 — Reminder Generation Baseline

- **Target:** TBD reminder generation timeliness target; outbound delivery blocked until EXT-002 is resolved.
- **Validation Method:** TBD scheduled job monitoring and reminder workflow test method.

### ARD-OPS-004 — Scalability Baseline

- **Target:** TBD patient/staff concurrency and appointment volume assumptions.
- **Validation Method:** TBD performance and capacity validation method.

## 12. Observability

- **Logging:** TBD pending operations model; must avoid exposing unnecessary PHI and must not replace required audit logging.
- **Metrics:** TBD pending operations model; needed to establish availability, API performance, reminder generation, booking, and staff workflow baselines.
- **Tracing:** TBD pending operations model; core scheduling flow tracing is unresolved.
- **Alerting:** TBD pending operations model; error, failed job, and security-relevant alert policies are unresolved.
- **Sensitive Data Restrictions:** PHI minimization is required; specific redaction/masking standards are TBD pending security and operations review.

## 13. Deployment Architecture

- **Environments:** TBD pending operations model.
- **Deployment Model:** TBD pending operations model.
- **CI/CD:** TBD pending operations model and security review.
- **Configuration Management:** TBD pending operations model.
- **Rollback:** TBD pending operations model.
- **Infrastructure as Code:** TBD pending operations model.

## 14. Testing Architecture

Required test levels:

- Unit tests — Applicability and ownership TBD pending feature-team testing strategy.
- Integration tests — Applicability and ownership TBD pending feature-team testing strategy.
- Contract tests — Applicability and ownership TBD pending feature-team testing strategy.
- End-to-end tests — Applicability and ownership TBD pending feature-team testing strategy.
- Security tests — Applicability and ownership TBD pending security review.
- Performance tests, where applicable — Applicability and ownership TBD pending reliability/performance target decisions.

Minimum quality expectations:

- **Coverage Threshold:** TBD pending feature-team testing strategy.
- **Blocking Security Severity:** TBD pending security review.
- **Required Build/Lint Checks:** TBD pending feature-team testing strategy and CI/CD model.

## 15. Architecture Constraints

- ARC-CON-001 — The solution must support HIPAA compliance obligations for a healthcare clinic.
- ARC-CON-002 — The hosting platform must use HIPAA-eligible managed cloud services with a signed BAA before production use.
- ARC-CON-003 — The solution must avoid unnecessary operational complexity because the company is a small business.
- ARC-CON-004 — Existing patients may reschedule online only up to 24 hours before the appointment.
- ARC-CON-005 — Patient-facing launch depends on the staff-only internal rollout completing first.
- ARC-CON-006 — The final clinic scheduling/EHR/practice-management dependency is undecided, so scheduling integrations must be adapter-based.
- ARC-CON-007 — Email reminders require patient consent before sending.
- ARC-CON-008 — Outbound reminder delivery must remain blocked until the email sending mechanism is resolved and approved.
- ARC-CON-009 — Patient account login is out of scope for launch.
- ARC-CON-010 — Clinical diagnosis, triage, and treatment recommendations are out of scope.
- ARC-CON-011 — Database technology, retention, migration, operations model, observability baseline, testing strategy, security scanning policy, and SBOM policy are unresolved and must be closed before production readiness can be approved.

## 16. Risks and Trade-offs

| ID | Risk/Trade-off | Impact | Mitigation |
|---|---|---|---|
| ARC-RISK-001 | Final scheduling system is undecided | High impact to data ownership, migration, and integration design | Use ARD-DEC-002 adapter-based integration and keep EXT-001 open until selected. |
| ARC-RISK-002 | Email sending provider is TBD while PRD-FR-004 requires system-sent reminders | PRD-FR-004 cannot be fully accepted until delivery is resolved | Build reminder eligibility/link generation but block outbound delivery per ARD-DEC-005. |
| ARC-RISK-003 | Staff authentication controls are TBD | HIPAA security posture cannot be finalized | Keep RBAC/audit mandatory and require Security Reviewer decision before production. |
| ARC-RISK-004 | Database choice, retention, and migration are TBD | Data architecture and compliance retention cannot be finalized | Use repository interfaces now and close DATA/retention decisions before production data migration. |
| ARC-RISK-005 | Operations, observability, testing, scanning, and SBOM policies are TBD | Release readiness cannot be objectively validated | Track as open architecture questions with Engineering Lead and Security Reviewer owners. |
| ARC-RISK-006 | No-login rescheduling through email links may expose PHI if mishandled | Privacy and HIPAA risk | Use unique appointment-specific links, privacy-preserving invalid-link responses, audit logging, and minimal reminder content. |

## 17. Open Architecture Questions

| ID | Question | Owner | Status | Decision/Due Date |
|---|---|---|---|---|
| ARC-OQ-001 | What clinic scheduling/EHR/practice-management system or manual process is EXT-001 for launch? | Product Owner | Open | TBD |
| ARC-OQ-002 | What database technology will implement COMP-005 repository interfaces? | Engineering Lead | Open | TBD |
| ARC-OQ-003 | What are the retention requirements for appointments, requests, consent, reminder links, staff user records, and audit events? | Product Owner / Security Reviewer | Open | TBD |
| ARC-OQ-004 | Is data migration required for launch, and what data must be migrated or synchronized? | Product Owner / Engineering Lead | Open | TBD |
| ARC-OQ-005 | What compliant email sending mechanism will satisfy PRD-FR-004 and EXT-002? | Product Owner / Security Reviewer | Open | TBD |
| ARC-OQ-006 | What staff authentication controls are required for application-managed accounts, including MFA, password policy, lockout, recovery, and session timeout? | Security Reviewer | Open | TBD |
| ARC-OQ-007 | What encryption, secrets-management, and PHI redaction standards apply to the selected hosting and data stack? | Security Reviewer / Engineering Lead | Open | TBD |
| ARC-OQ-008 | What measurable availability, API performance, reminder generation, and scalability targets apply to launch? | Product Owner / Engineering Lead | Open | TBD |
| ARC-OQ-009 | What observability baseline is required for logging, metrics, tracing, alerting, and PHI restrictions? | Engineering Lead | Open | TBD |
| ARC-OQ-010 | What operations model covers environments, CI/CD, configuration, rollback, and infrastructure as code? | Engineering Lead | Open | TBD |
| ARC-OQ-011 | What release testing strategy, coverage threshold, build checks, lint checks, contract tests, E2E tests, and performance tests are required? | Engineering Lead | Open | TBD |
| ARC-OQ-012 | What dependency/container scanning thresholds and SBOM policy are required? | Security Reviewer | Open | TBD |
| ARC-OQ-013 | What are the baseline and target values for PRD KPIs KPI-001, KPI-002, and KPI-003? | Product Owner | Open | TBD |
| ARC-OQ-014 | Which exact appointment types and providers are included in staff-only and patient-facing launch? | Clinic Operations | Open | TBD |
| ARC-OQ-015 | What are the target dates for staff-only rollout and patient-facing launch? | Product Owner | Open | TBD |

## 18. Feature Mapping

| Feature | Relevant Components | Decision IDs | Interface IDs | Security IDs |
|---|---|---|---|---|
| FEAT-001 | COMP-001, COMP-002, COMP-003, COMP-004, COMP-005, COMP-007 | ARD-DEC-001, ARD-DEC-002, ARD-DEC-004 | ARD-API-001, ARD-API-002, ARD-API-006 | ARD-SEC-001 |
| FEAT-002 | COMP-001, COMP-002, COMP-003, COMP-004, COMP-005, COMP-007 | ARD-DEC-001, ARD-DEC-002, ARD-DEC-004 | ARD-API-003, ARD-API-006 | ARD-SEC-001, ARD-SEC-002 |
| FEAT-003 | COMP-002, COMP-005, COMP-006, COMP-007 | ARD-DEC-004, ARD-DEC-005 | ARD-API-007 | ARD-SEC-002, ARD-SEC-003 |
| FEAT-004 | COMP-001, COMP-002, COMP-003, COMP-004, COMP-007, COMP-008 | ARD-DEC-001, ARD-DEC-002, ARD-DEC-006 | ARD-API-004, ARD-API-006 | ARD-SEC-001 |
| FEAT-005 | COMP-001, COMP-002, COMP-003, COMP-004, COMP-005, COMP-007, COMP-008 | ARD-DEC-001, ARD-DEC-002, ARD-DEC-004, ARD-DEC-006 | ARD-API-005, ARD-API-006 | ARD-SEC-001 |

## 19. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Solution Architect | TBD | Pending | TBD |
| Security Reviewer | TBD | Pending | TBD |
| Engineering Lead | TBD | Pending | TBD |