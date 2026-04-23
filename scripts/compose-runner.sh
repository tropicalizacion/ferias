#!/usr/bin/env bash
set -euo pipefail

# Shared startup runner for docker compose environments.
# Expected variables from caller:
# - MODE_NAME (e.g., Development, Production)
# - COMPOSE_FILE (e.g., compose.dev.yml)
# - ENV_OVERLAY_FILE (e.g., .env.dev)

MODE_NAME="${MODE_NAME:-Development}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.dev.yml}"
ENV_OVERLAY_FILE="${ENV_OVERLAY_FILE:-.env.dev}"

# Always run from the repo root, regardless of where this script is invoked from
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

print_section() {
    local color="$1"
    local title="$2"
    echo ""
    echo -e "${color}-----------------------------------------------------${NC}"
    echo -e "${color}  ${title}${NC}"
    echo -e "${color}-----------------------------------------------------${NC}"
}

get_env_value() {
    local key="$1"
    local default_value="$2"
    local value overlay_value

    value=$(grep -E "^${key}=" .env 2>/dev/null | tail -n1 | cut -d'=' -f2- || true)
    overlay_value=$(grep -E "^${key}=" "$ENV_OVERLAY_FILE" 2>/dev/null | tail -n1 | cut -d'=' -f2- || true)
    [ -n "$overlay_value" ] && value="$overlay_value"
    echo "${value:-$default_value}"
}

WEB_PORT=$(get_env_value "WEB_PORT" "8000")

echo -e "${GREEN}Ferias - ${MODE_NAME} environment${NC}"
echo ""

if ! command -v docker >/dev/null 2>&1; then
    echo -e "${RED}Error: docker is not installed or not in PATH.${NC}"
    exit 1
fi
if ! command -v curl >/dev/null 2>&1; then
    echo -e "${RED}Error: curl is not installed or not in PATH.${NC}"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found.${NC}"
    if [ -f ".env.example" ]; then
        echo "Copying .env.example -> .env ..."
        cp .env.example .env
        echo -e "${YELLOW}Edit .env with your values before continuing.${NC}"
    fi
    exit 1
fi

if [ ! -f "$ENV_OVERLAY_FILE" ]; then
    echo -e "${YELLOW}Warning: $ENV_OVERLAY_FILE not found. Using values from .env only.${NC}"
fi

if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}Error: $COMPOSE_FILE not found.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Pulling required Docker images...${NC}"
docker compose -f "$COMPOSE_FILE" pull --ignore-buildable

echo ""
echo -e "${BLUE}Building and starting services...${NC}"
set +e
docker compose -f "$COMPOSE_FILE" up --build -d --remove-orphans
UP_EXIT=$?
set -e
if [ $UP_EXIT -ne 0 ]; then
    echo -e "${RED}Error: docker compose up failed (exit code ${UP_EXIT}).${NC}"
    echo -e "${YELLOW}Recent logs:${NC}"
    docker compose -f "$COMPOSE_FILE" logs --tail=30
    exit 1
fi

echo ""
echo -e "${YELLOW}Waiting for web on: ${WEB_PORT}...${NC}"
echo -e "${GRAY}(First run may take 1-2 minutes while database setup and Django migrations run)${NC}"

MAX_WAIT=90
ELAPSED=0
WEB_OK=false

while [ $ELAPSED -lt $MAX_WAIT ]; do
    if curl -sf --max-time 3 "http://localhost:${WEB_PORT}" >/dev/null 2>&1; then
        WEB_OK=true
        break
    fi

    if [ $(( ELAPSED % 15 )) -eq 0 ] && [ $ELAPSED -gt 0 ]; then
        echo ""
        echo -e "${GRAY}  [${ELAPSED}s] Containers:${NC}"
        docker compose -f "$COMPOSE_FILE" ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null \
            | while IFS= read -r line; do echo -e "${GRAY}    ${line}${NC}"; done
        echo -e "${GRAY}  [${ELAPSED}s] Last web lines:${NC}"
        docker compose -f "$COMPOSE_FILE" logs --tail=5 web 2>/dev/null \
            | while IFS= read -r line; do echo -e "${GRAY}    ${line}${NC}"; done
    else
        echo -e "${GRAY}  . [${ELAPSED}s]${NC}"
    fi

    sleep 3
    ELAPSED=$(( ELAPSED + 3 ))
done

if [ "$WEB_OK" = true ]; then
    echo ""
    echo -e "${GREEN}Web responding after ${ELAPSED} s.${NC}"
else
    echo ""
    echo -e "${RED}Web did not respond within ${MAX_WAIT} s.${NC}"
    echo -e "${YELLOW}Last web logs:${NC}"
    docker compose -f "$COMPOSE_FILE" logs --tail=30 web
fi

print_section "$CYAN" "Container status"
docker compose -f "$COMPOSE_FILE" ps

print_section "$CYAN" "Infrastructure health checks"
for svc in database; do
    cid=$(docker compose -f "$COMPOSE_FILE" ps -q "$svc" 2>/dev/null || true)
    if [ -n "$cid" ]; then
        health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' "$cid" 2>/dev/null || echo "unknown")
        status=$(docker inspect --format='{{.State.Status}}' "$cid" 2>/dev/null || echo "?")
        if [ "$health" = "healthy" ] || [ "$health" = "no healthcheck" ]; then
            echo -e "  ${GREEN}[OK]${NC}  ${svc}: ${status} / ${health}"
        else
            echo -e "  ${RED}[!!]${NC}  ${svc}: ${status} / ${health}"
        fi
    else
        echo -e "  ${RED}[!!]${NC}  ${svc}: container not found"
    fi
done

print_section "$CYAN" "Docker volumes"
for vol in database_data; do
    full_name="ferias_${vol}"
    if docker volume inspect "$full_name" >/dev/null 2>&1; then
        mp=$(docker volume inspect --format='{{.Mountpoint}}' "$full_name" 2>/dev/null || echo "?")
        echo -e "  ${GREEN}[OK]${NC}  ${full_name}"
        echo "        Mountpoint: ${mp}"
    else
        echo -e "  ${YELLOW}[--]${NC}  ${full_name}: does not exist yet (created on first use)"
    fi
done

print_section "$GREEN" "${MODE_NAME} URLs"
echo "  Django web           http://localhost:${WEB_PORT}"
echo "  Django admin         http://localhost:${WEB_PORT}/admin"
echo "  REST API             http://localhost:${WEB_PORT}/api/"

print_section "$BLUE" "Infrastructure"
echo "  PostgreSQL (database)  internal only (docker compose exec database psql -U postgres)"

print_section "$YELLOW" "Useful commands"
echo "  Stream logs:          docker compose -f $COMPOSE_FILE logs -f"
echo "  Web logs:             docker compose -f $COMPOSE_FILE logs -f web"
echo "  Run migrations:       docker compose -f $COMPOSE_FILE exec web uv run python manage.py migrate"
echo "  Create superuser:     docker compose -f $COMPOSE_FILE exec web uv run python manage.py createsuperuser"
echo "  Django shell:         docker compose -f $COMPOSE_FILE exec -it web uv run python manage.py shell"
echo "  Stop all:             docker compose -f $COMPOSE_FILE down"
echo ""
