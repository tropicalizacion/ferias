#!/bin/bash
set -euo pipefail

# Ensure virtual environment bin is on PATH if present
if [ -d "/app/.venv/bin" ]; then
    export PATH="/app/.venv/bin:$PATH"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log(){ echo -e "${GREEN}[entrypoint]${NC} $*"; }
warn(){ echo -e "${YELLOW}[entrypoint][warn]${NC} $*"; }
err(){ echo -e "${RED}[entrypoint][error]${NC} $*"; }

# Build DATABASE_URL if missing (fallback)
if [ -z "${DATABASE_URL:-}" ]; then
    if [[ -n "${DB_USER:-}" && -n "${DB_HOST:-}" && -n "${DB_NAME:-}" ]]; then
        if [ -n "${DB_PASSWORD:-}" ]; then
            export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT:-5432}/${DB_NAME}"
        else
            export DATABASE_URL="postgresql://${DB_USER}@${DB_HOST}:${DB_PORT:-5432}/${DB_NAME}"
        fi
        warn "DATABASE_URL not set; constructed: ${DATABASE_URL}"
    else
        warn "DATABASE_URL not set and insufficient components to construct it."
    fi
fi

log "Starting Django application..."

# Ensure virtual environment exists (install if not present)
if [ ! -d "/app/.venv" ]; then
warn "Setting up virtual environment (uv sync)..."
    uv sync --frozen
else
log "Virtual environment already exists"
fi

# Wait for database to be ready
log "Waiting for database connection..."
until uv run python -c "import psycopg2; import os; conn = psycopg2.connect(os.environ['DATABASE_URL']); conn.close(); print('Database is ready!')"; do
warn "Database is unavailable - sleeping"
    sleep 5
done

log "Database is ready!"

# Run database migrations (initial)
log "Running database migrations (initial)..."
uv run python manage.py migrate --noinput

# Make migrations
APPS_TO_MIGRATE=(
    "marketplaces"
    "products"
    "crowdsourcing"
    "website"
    "cms_pages"
    "users"
    "feed"
    "blog"
    "content"
    "recipes"
)
log "Creating migrations for: ${APPS_TO_MIGRATE[*]}"
uv run python manage.py makemigrations "${APPS_TO_MIGRATE[@]}" || warn "No changes detected for migrations"

# Run database migrations (after makemigrations)
log "Running database migrations (final)..."
uv run python manage.py migrate --noinput

# Create superuser if it doesn't exist using defaults in development mode
if [[ "${CREATE_SUPERUSER:-True}" == "True" && ( "${DEBUG:-}" == "True" || "${DEBUG:-}" == "1" ) ]]; then
    export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
    export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-admin}"
    export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
    log "Ensuring development superuser '${DJANGO_SUPERUSER_USERNAME}' exists (DEBUG mode)"
    set +e
    uv run python manage.py createsuperuser --noinput
    csu_exit=$?
    set -e
    if [ $csu_exit -eq 0 ]; then
        log "Superuser created: ${DJANGO_SUPERUSER_USERNAME}/${DJANGO_SUPERUSER_PASSWORD}"
    else
        warn "Superuser creation skipped (maybe already exists)"
    fi
else
    log "Skipping auto superuser creation (CREATE_SUPERUSER=${CREATE_SUPERUSER:-0} DEBUG=${DEBUG:-})"
fi

# Initialize Wagtail default pages (home/blog)
log "Initializing Wagtail default pages..."
uv run python manage.py init_wagtail || warn "Wagtail init skipped or already initialized"

# Collect static files
log "Collecting static files..."
uv run python manage.py collectstatic --noinput || warn "Static files collection skipped"

# Load initial data
INITIAL_FIXTURES=(
    "marketplaces"
    "products"
    "website"
    "crowdsourcing"
    "users"
    "feed"
    "content"
)
for fixture in "${INITIAL_FIXTURES[@]}"; do
    log "Loading fixture: ${fixture}"
    uv run python manage.py loaddata "${fixture}" || warn "Fixture load failed for ${fixture}"
done

log "Django application setup complete!"

# Execute the main command
log "Launching: $*"
exec "$@"