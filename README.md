# Clinic booking app

Foundation scaffold for a React scheduling SPA and Python/FastAPI REST API.

## Local development

### Backend

From the `backend/` directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
uvicorn api.main:app --reload
pytest
```

The API exposes a foundation health endpoint at `GET /api/health`.

### Frontend

From the `frontend/` directory:

```bash
npm install
npm run dev
npm test
npm run build
```

The SPA currently renders the scheduling workspace shell and placeholder patient/staff workflow routes.

## Verification commands

Run these before building feature work on top of the scaffold:

```bash
cd backend && pytest
cd frontend && npm test
cd frontend && npm run build
```

## Production-readiness decisions still unresolved

The ARD keeps these decisions open; this scaffold does not mark them complete:

- Database technology for repository implementations.
- Data retention requirements for appointments, requests, consent, reminder links, staff users, and audit events.
- Data migration approach and launch synchronization needs.
- Final scheduling/EHR/practice-management dependency.
- Compliant email sending mechanism; outbound reminder delivery remains blocked until selected and approved.
- Staff authentication controls, including MFA, password policy, lockout, recovery, and session timeout.
- Encryption, secrets-management, and PHI redaction standards.
- Hosting provider and production use of HIPAA-eligible managed cloud services with a signed BAA.
- Operations model, environments, configuration management, rollback, infrastructure as code, and CI/CD.
- Observability baseline for logging, metrics, tracing, alerting, and PHI restrictions.
- Release testing strategy, coverage thresholds, required build/lint checks, contract tests, end-to-end tests, and performance tests.
- Dependency scanning, container scanning, vulnerability blocking thresholds, and SBOM policy.
- Launch appointment types, providers, rollout dates, and PRD KPI baselines.
