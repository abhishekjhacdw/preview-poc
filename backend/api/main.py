from fastapi import FastAPI

from api.db import Base, engine
from api.routes import api_router
from services.audit.service import AuditLoggingService
from services.auth.service import StaffAuthenticationProvider, StaffAuthorizationService


def create_app(
    *,
    audit_logging_service: AuditLoggingService | None = None,
    staff_authentication_provider: StaffAuthenticationProvider | None = None,
    staff_authorization_service: StaffAuthorizationService | None = None,
) -> FastAPI:
    app = FastAPI(
        title="Clinic Booking API",
        version="0.1.0",
        description="REST API boundary for clinic scheduling workflows.",
    )
    app.state.audit_logging_service = audit_logging_service
    app.state.staff_authentication_provider = staff_authentication_provider
    app.state.staff_authorization_service = staff_authorization_service
    app.include_router(api_router, prefix="/api")

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()
