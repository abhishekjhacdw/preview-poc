#!/bin/sh
set -eu

POC_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$POC_DIR")
COMPOSE_FILE="$POC_DIR/compose.yaml"
STATE_DIR="${TMPDIR:-/tmp}/clinic-booking-preview-poc"
PID_FILE="$STATE_DIR/ttl.pid"
TTL_MINUTES="${PREVIEW_TTL_MINUTES:-45}"

case "${1:-}" in
  up)
    case "$TTL_MINUTES" in
      ''|*[!0-9]*) echo "PREVIEW_TTL_MINUTES must be a whole number from 30 to 60" >&2; exit 2 ;;
    esac
    if [ "$TTL_MINUTES" -lt 30 ] || [ "$TTL_MINUTES" -gt 60 ]; then
      echo "PREVIEW_TTL_MINUTES must be from 30 to 60" >&2
      exit 2
    fi
    mkdir -p "$STATE_DIR"
    if [ -f "$PID_FILE" ]; then
      old_pid=$(cat "$PID_FILE")
      kill "$old_pid" 2>/dev/null || true
      rm -f "$PID_FILE"
    fi
    docker compose --project-directory "$PROJECT_ROOT" -f "$COMPOSE_FILE" up --build -d
    nohup sh -c "sleep $((TTL_MINUTES * 60)); docker compose --project-directory '$PROJECT_ROOT' -f '$COMPOSE_FILE' down" >/dev/null 2>&1 </dev/null &
    echo "$!" > "$PID_FILE"
    echo "Preview: http://127.0.0.1:${PREVIEW_PORT:-8090}"
    echo "Auto-stop: ${TTL_MINUTES} minutes (override with PREVIEW_TTL_MINUTES=30..60)"
    ;;
  down)
    if [ -f "$PID_FILE" ]; then
      old_pid=$(cat "$PID_FILE")
      kill "$old_pid" 2>/dev/null || true
      rm -f "$PID_FILE"
    fi
    docker compose --project-directory "$PROJECT_ROOT" -f "$COMPOSE_FILE" down
    ;;
  status)
    docker compose --project-directory "$PROJECT_ROOT" -f "$COMPOSE_FILE" ps
    ;;
  logs)
    docker compose --project-directory "$PROJECT_ROOT" -f "$COMPOSE_FILE" logs -f --tail=100
    ;;
  *)
    echo "Usage: $0 {up|down|status|logs}" >&2
    exit 2
    ;;
esac