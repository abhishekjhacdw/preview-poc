FROM node:22-alpine AS frontend-build

WORKDIR /src/frontend
COPY frontend/package.json ./
RUN npm install --legacy-peer-deps --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS preview

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend \
    PREVIEW_FRONTEND_DIR=/app/frontend/dist

WORKDIR /app
COPY backend/ ./backend/
RUN pip install --no-cache-dir ./backend

COPY --from=frontend-build /src/frontend/dist /app/frontend/dist
COPY preview-poc/preview_app.py /app/preview_app.py

RUN useradd --system --uid 10001 --user-group --create-home preview \
    && chown -R preview:preview /app

USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "preview_app:app", "--host", "0.0.0.0", "--port", "8080"]