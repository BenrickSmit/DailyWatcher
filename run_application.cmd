@echo off

REM Build and start the services
docker-compose up -d

REM Wait for the services to start
timeout /t 5

REM Display the running containers
docker-compose ps

REM Execute the db_api.py script in the running container
docker-compose exec dailywatcher python3 ./financial/db_api.py

REM Print a message with the API endpoint
echo API is now accessible at http://localhost:8000/
