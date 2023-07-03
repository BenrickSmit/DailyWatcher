#!/usr/bin/env python3

"""
This module is used to create the financial_data table in a local sqlite db.

This module provides functionality for logging, and simple database creation
via sqlite3 and logging.

Author: B.G. Smit
"""


import sqlite3
import logging
import os
import json


def db_creation():
    """This function will create the SQLite database if it doesn't exist and
    use the SQL instructions found in the schema.sql file to do so
    """

    # Connect to the database (creates a new database if it doesn't exist)
    conn = sqlite3.connect(_get_db_path())
    if not conn:
        logging.error("-- Could NOT Create Database")
        raise Exception("Could not Create Database")

    # Create a cursor object to execute necessary SQL commands
    cursor = conn.cursor()

    # Read the schema.sql file to create the database with the necessary schema
    try:
        schema_sql = ""
        with open(os.getenv("SCHEMA_PATH"), "r") as schema_file:
            schema_sql = schema_file.read()

        # Create the table to hold the information as necessary via the schema.sql
        cursor.executescript(schema_sql)

    except sqlite3.Error as e:
        logging.error("-- %s", e)
        return

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    logging.info(" -- Created the financial_data table Successfully")


def db_record_insert(record_data):
    """This function will insert a record in to the SQLite database as is

    Args:
        record_data (string): this function will be the CSV style record that
            needs to be inserted in order of arguments.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(_get_db_path())

    # Convert JSON elements to a list of tuples
    json_data = json.loads(record_data)
    column_list = os.getenv("RECORD_COLLECTION").strip().split(",")
    print(column_list)

    for record in json_data:
        symbol = record[column_list[0]]
        date = record[column_list[1]]
        open = record[column_list[2]]
        close = record[column_list[3]]
        vol = record[column_list[4]]

        conn.execute(
            "INSERT OR IGNORE INTO "
            + os.getenv("TABLE_NAME")
            + " ("
            + os.getenv("RECORD_COLLECTION")
            + ") VALUES (?, ?, ?, ?, ?)",
            (symbol, date, open, close, vol),
        )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    logging.info(" -- Inserted Stock Records Successfully")


def db_display_records():
    """This function will access the locally created Database and display all
    the records in it.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(_get_db_path())

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all records from a table
    cursor.execute("SELECT * FROM " + os.getenv("TABLE_NAME") + "")

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    logging.info(" -- Displayed the financial_data records table Successfully")


def _get_db_path():
    """This function is solely used to get the proper path to the locally
    created database
    """
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, os.getenv("DATABASE_PATH"))

    db_path = file_path

    logging.info(" -- Local Database Path: " + db_path)

    return db_path


def main():
    db_creation()


if __name__ == "__main__":
    main()
