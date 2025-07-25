FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1 \
  PYTHONUNBUFFERED 1 \
  GDAL_LIBRARY_PATH=/usr/lib/libgdal.so \
  GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

WORKDIR /app

RUN apt-get update && \
  apt-get install -y \
  build-essential \
  curl \
  gcc \
  g++ \
  libgdal-dev \
  gdal-bin \
  libgeos-dev \
  libproj-dev \
  libpq-dev \
  libspatialindex-dev \
  python3-dev \
  && apt-get clean && \
  rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./requirements.txt .
RUN uv pip install -r ./requirements.txt --system

COPY . . 

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]