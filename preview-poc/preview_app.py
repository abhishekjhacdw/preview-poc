from __future__ import annotations

import os
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.main import create_app


frontend_dir = Path(os.environ.get("PREVIEW_FRONTEND_DIR", "/app/frontend/dist")).resolve()
index_file = frontend_dir / "index.html"
if not index_file.is_file():
    raise RuntimeError(f"Frontend build is missing: {index_file}")

app = create_app()
app.mount("/assets", StaticFiles(directory=frontend_dir / "assets"), name="frontend-assets")


@app.get("/healthz", include_in_schema=False)
def preview_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def frontend_root() -> FileResponse:
    return FileResponse(index_file)


@app.get("/{path:path}", include_in_schema=False)
def frontend_fallback(path: str) -> FileResponse:
    if path == "api" or path.startswith("api/") or path == "assets" or path.startswith("assets/"):
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(index_file)
