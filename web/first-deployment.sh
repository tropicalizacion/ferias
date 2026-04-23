#!/bin/bash
set -euo pipefail

log() {
    echo "[first-deployment] $*"
}

# Ensure virtual environment bin is on PATH if present
if [ -d "/app/.venv/bin" ]; then
    export PATH="/app/.venv/bin:$PATH"
fi

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

INITIAL_FIXTURES=(
    "marketplaces"
    "products"
    "website"
    "crowdsourcing"
    "users"
    "feed"
    "content"
)

log "Creating migrations for: ${APPS_TO_MIGRATE[*]}"
uv run python manage.py makemigrations "${APPS_TO_MIGRATE[@]}"

log "Applying migrations"
uv run python manage.py migrate --noinput

log "Initializing Wagtail default pages"
uv run python manage.py init_wagtail

for fixture in "${INITIAL_FIXTURES[@]}"; do
    log "Loading fixture: ${fixture}"
    uv run python manage.py loaddata "${fixture}"
done

log "First deployment bootstrap completed"
