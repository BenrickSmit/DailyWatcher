# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

# Ensures SQLLite is being used
RUN apt-get update && apt-get install -y sqlite3
RUN pip install --upgrade pip setuptools wheel

# Add the environment variables necessary for the database
ENV PATH=$PATH:/financial
ENV DATABASE_PATH=stock_fortnight.db
ENV STOCK_PATH=./financial/stocks.txt
ENV RECORD_COLLECTION=symbol,date,open_price,close_price,volume
ENV TABLE_NAME=financial_data
ENV SCHEMA_PATH=schema.sql

ENV PORT_USED=5000
ENV API_DATABASE_PATH=./financial/stock_fortnight.db

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "-u", "get_raw_data.py"]
