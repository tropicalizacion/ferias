#!/usr/bin/env bash
set -euo pipefail

MODE_NAME="Production"
COMPOSE_FILE="compose.prod.yml"
ENV_OVERLAY_FILE=".env.prod"

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/compose-runner.sh"
