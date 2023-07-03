#!/bin/bash

# Build the Docker image and start the database service
docker-compose build dailywatcher api

# Start the database service and wait for it to be ready
docker-compose up -d api

# Wait for the database service to be ready (adjust the timeout as needed)
timeout 30s docker-compose logs -f db | grep -q 'database system is ready to accept connections'

# Run the db_api.py file to start Flask
docker-compose run dailywatcher python3 financial/db_api.py
