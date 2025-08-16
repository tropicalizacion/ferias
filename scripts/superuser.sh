#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if containers are running
echo -e "${YELLOW}Checking if containers are running...${NC}"
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Containers not running. Starting them...${NC}"
    docker-compose up -d
else
    echo -e "${GREEN}Containers are already running${NC}"
fi

# Function to check if database is ready
check_database() {
    docker-compose exec -T db pg_isready -U ${DB_USER:-postgres} -d ${DB_NAME:-ferias} > /dev/null 2>&1
    return $?
}

echo -e "${YELLOW}Waiting for database to be ready...${NC}"

# Wait for database to be ready (max 30 seconds)
counter=0
max_attempts=15

while [ $counter -lt $max_attempts ]; do
    if check_database; then
        echo -e "${GREEN}Database is ready!${NC}"
        break
    else
        echo -e "${YELLOW}Database not ready yet, waiting... (attempt $((counter + 1))/$max_attempts)${NC}"
        sleep 2
        counter=$((counter + 1))
    fi
done

# Check if we exceeded max attempts
if [ $counter -eq $max_attempts ]; then
    echo -e "${RED}Database failed to become ready after $max_attempts attempts${NC}"
    exit 1
fi

# Create superuser
echo -e "${YELLOW}Creating superuser...${NC}"
docker-compose exec web python manage.py createsuperuser

echo -e "${GREEN}Superuser creation process completed!${NC}"