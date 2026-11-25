from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter


class HealthResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"status": "ok"}})

    status: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Service health")
def health() -> HealthResponse:
    return HealthResponse(status="ok")
