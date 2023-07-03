@echo off

REM Stop and remove all containers
docker-compose down

REM Remove all containers
docker ps -aq | ForEach-Object { docker stop $_ 2>nul "&" docker rm $_ }

REM Remove all images
docker rmi $(docker images -aq)

REM Stop all containers
docker stop $(docker ps -aq)

REM Display message indicating every stopped and is removed
echo All containers and images have been stopped and removed.