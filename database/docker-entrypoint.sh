#!/bin/bash
set -euo pipefail

INIT_SCRIPT_DIR="/docker-entrypoint-initdb.d"
INIT_SCRIPT_PATH="${INIT_SCRIPT_DIR}/010-enable-extensions.sh"
EXTENSIONS_SQL_PATH="${INIT_SCRIPT_DIR}/extensions.sql"

DB_NAME="${POSTGRES_DB:-${DB_NAME:-infobus}}"
DB_USER="${POSTGRES_USER:-${DB_USER:-postgres}}"

cat > "${INIT_SCRIPT_PATH}" <<EOF
#!/bin/bash
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" -f "${EXTENSIONS_SQL_PATH}"
EOF

chmod +x "${INIT_SCRIPT_PATH}"

echo "[database-entrypoint] Extensions init prepared for database '${DB_NAME}' as user '${DB_USER}'"

exec /usr/local/bin/docker-entrypoint.sh "$@"