# Multi-stage build for Django app with uv
FROM python:3.14-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  libpq-dev \
  gdal-bin \
  libgdal-dev \
  && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV ENTRYPOINT_PATH="/app/docker-entrypoint.sh" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

# Create app user
RUN groupadd --gid 1000 app && \
  useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Set work directory
WORKDIR /app

# Change ownership of /app directory to app user
RUN chown -R app:app /app

# Copy dependency files
COPY --chown=app:app pyproject.toml uv.lock ./

# Dependencies will be installed at runtime to avoid permission issues

# Copy source code
COPY --chown=app:app . .

# Ensure entrypoint script is executable
RUN chmod +x $ENTRYPOINT_PATH

# Switch to app user before installing dependencies to avoid permission issues
USER app

# Expose port for Django development server
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# ---- Development stage
FROM base AS dev
# ----------------------

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---- Production stage
FROM base AS prod
# ---------------------

# Install dependencies in production mode
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "daphne", "-b", "0.0.0.0", "-p", "8000", "ferias.asgi:application"]
