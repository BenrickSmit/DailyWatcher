## Project Description

This project makes use of Flask, Python3, and SQLite to create an API service that can be queried from the local machine at port 5000. It retrieves the stock
data for the last while by accessing AlphaVantage's API and then storing it locally on the device. The following two API access calls have been tested and their alternatives, as long as the service has been run adequately


`curl 'http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2'`
`curl http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM`

## Tech Stack
This project is built with Python3, Flask, SQLite, and Docker

## How to Use Application
In order to use the application you can run the "run_application.sh" or "run_application.cmd" file depending on the OS you're currently using. If not, follow the instrutions below. You can also stop the application with the same method, i.e. by running either "stop_all.cmd" or "stop_all.sh"

PS: If there is some trouble and there is no access directly to the API, just run the db_api.py directly. Sometimes it works, sometimes it doesn't

Starting:
For Windows (tested):
`docker-compose build dailywatcher api
 docker-compose up -d
 timeout /t 5
 docker-compose ps
 docker-compose exec dailywatcher python3 db_api.py
 echo API is now accessible at http://localhost:8000/`

For Linux (untested):
`docker-compose build dailywatcher api
 docker-compose up -d api
 timeout 30s docker-compose logs -f db | grep -q 'database system is ready to accept connections'
 docker-compose run dailywatcher python3 financial/db_api.py`


Stopping:
For Windows (tested):
`docker-compose down
 docker ps -aq | ForEach-Object { docker stop $_ 2>nul "&" docker rm $_ }
 docker rmi $(docker images -aq)
 docker stop $(docker ps -aq)`

For Linux (untested):
`docker-compose down
 docker stop $(docker ps -aq)
 docker rm $(docker ps -aq)
 docker rmi $(docker images -aq)`

## API Upkeep
In order to ensure the api stays anonymous, simple add a file in the financial folder in the root directory, and title it 'api_key.txt'. Paste the api key in here.

## Design Choices

# Database Choice

I settled on SQLite as not only is it lightweight, serverless, and self-contained, 
but it also enables me to create only a single file database which will be very
useful for this kind of program that only needs the information quickly and temporarily and at a smaller scale.
It also adds to the efficiency of the program since there is no network overhead and only
Requests will then require any overhead.

# API Caller

I settled on Requests as it is the simplest, most intuitive, and readable solution. Not only can I expand it
easily should the project require more help, but it can be used with most APIs out there as well.

# API Service
Flask is probably the best way to create a simple HTTP server for API access while ensuring I keep simplicity and efficiency