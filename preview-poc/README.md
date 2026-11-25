# Clinic Booking Preview POC

This folder is an isolated, removable proof of concept for running this generated React + FastAPI app in one container. It does not change the app's original frontend/backend source files and can be moved into BuildIQ as a preview module later.

## Run

From the project root:

```sh
./preview-poc/preview.sh up
```

Open `http://127.0.0.1:8090`. The launcher builds the React bundle, packages it with FastAPI in one image, binds only to localhost, and schedules an automatic stop after 45 minutes by default. Set `PREVIEW_TTL_MINUTES=30` through `60` to change the timer, or `PREVIEW_PORT=8091` to choose another local port.

Useful commands:

```sh
./preview-poc/preview.sh status
./preview-poc/preview.sh logs
./preview-poc/preview.sh down
```

The adapter serves the existing FastAPI `/api/*` routes, the React SPA at `/`, and a `/healthz` container health endpoint. This generated app currently has no database connection in its backend dependencies, so this POC does not create SQLite or PostgreSQL resources. Add database configuration only when the app has persistence code to exercise.

The preview is for local demonstration only. It has no user authentication or Kubernetes isolation; localhost binding keeps it off the LAN. The TTL launcher is a host-side convenience process and is not a production cleanup controller. The production plan remains in [the BuildIQ final preview plan](../../final-preview-plan_BuildIQ.md).