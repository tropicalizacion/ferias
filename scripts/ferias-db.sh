#!/bin/bash
DB_NAME="ferias"
DB_USER="dsc"
DB_PASSWORD="test"

echo "Dropping database if it exists..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${DB_NAME};"

echo "Creating user..."
sudo -u postgres psql -c "CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}';"

echo "Creating database..."
sudo -u postgres createdb ${DB_NAME} --owner=${DB_USER}

echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

echo "Enabling extensions..."
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS postgis;"
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS unaccent;"

echo "Database ${DB_NAME} with user ${DB_USER} is ready!"
