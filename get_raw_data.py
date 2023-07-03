#!/usr/bin/env python3

"""
This module is used to create the financial_data table in a local sqlite db.

This module provides functionality for logging, and simple database creation
via sqlite3 and logging.

Author: B.G. Smit
"""

import financial.manage_database as manage_database
import financial.db_api as database_api
import logging
import requests
import json
import os


def get_api_key():
    logging.info(" -- Read API Key from Docker Secrets")

    #with open("./financial/api_key.txt", "r") as f:
    #    api_key = f.read().strip()

    with open("/run/secrets/api_key.txt") as f:
        api_key = f.read().strip()

    return api_key


def get_raw_data(stock_of_interest):
    """This function serves to get the RAW Stock data from the API and then
    processes it.

    Args:
        stock_of_interest (str): this is a stock to query with the API

    Returns:
        None: There was an error in the process
        Str: There is a collection of processed records in json format
    """
    data = "None"
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": "" + stock_of_interest + "",
        "apikey": "" + get_api_key() + "",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data_dict = response.json()

        # Process the data as into  daily information
        try:
            return get_processed_data(data_dict)
        except:
            logging.error("Data Not In Valid Foramt")
            return None

    else:
        logging.error("Request Failed. Status Code: ", response.status_code)
        return None


def get_processed_data(
    input_stock_data={},
):
    """This function will process the dictionary received from AlphaVantage
        and create separate day to day items. Ultimately returning a json
        document by creating a list of dictionaries

    Args:
        input_stock_data (dict): This is going to be a dictionary received from
            AlphaVantage for the time series data. It will contain two keys
            - Meta Data,
            - Time Series Daily Data (which is also a dict).
            Defaults to {}.
    """

    # Get the necessary keys and isolate the time series data key
    time_series_specification = "Time Series"
    time_series_info_key = get_dict_keyvalue(
        input_stock_data, time_series_specification
    )

    meta_data_specification = "Meta Data"
    meta_series_info_key = get_dict_keyvalue(input_stock_data, meta_data_specification)

    # Obtain the tiem series data in dictionary form and process it sequentially
    # with the symbol
    # Time Series Information
    daily_stock_data = input_stock_data[time_series_info_key]
    daily_stock_list = []

    daily_stock_symbol = input_stock_data[meta_series_info_key]
    daily_stock_symbol_spec = "Symbol"

    # Stock Symbol
    daily_stock_symbol_value = daily_stock_symbol[
        get_dict_keyvalue(daily_stock_symbol, daily_stock_symbol_spec)
    ]

    # Processing
    for date_key in daily_stock_data.keys():
        data_piece1 = "symbol"
        data_piece2 = "date"
        data_piece3 = "open_price"
        data_piece4 = "close_price"
        data_piece5 = "volume"

        temp_record = daily_stock_data[date_key]
        open_price_temp_key = "open"
        close_price_temp_key = "close"
        open_price_key = get_dict_keyvalue(temp_record, open_price_temp_key)
        close_price_key = get_dict_keyvalue(temp_record, close_price_temp_key)
        volume_key = get_dict_keyvalue(temp_record, data_piece5)

        open_price_value = temp_record[open_price_key]
        close_price_value = temp_record[close_price_key]
        volume_value = temp_record[volume_key]

        processed_dict = {
            data_piece1: daily_stock_symbol_value,
            data_piece2: date_key,
            data_piece3: open_price_value,
            data_piece4: close_price_value,
            data_piece5: volume_value,
        }

        daily_stock_list.append(processed_dict)

    # The daily_stock_list will be returned via reference
    return json.dumps(daily_stock_list)


def get_dict_keyvalue(input_dict, possible_value="close"):
    """This function will only return the key to be used based on a vague prompt
        to ensure that should the API change there won't be a big change in the
        code

    Args:
        input_dict (_type_): the dictionary containing the possible key
        possible_value (str): _description_. Defaults to "close".
    """
    dict_key_spec = possible_value
    dict_key = [
        item
        for item in list(input_dict.keys())
        if dict_key_spec.lower() in item.lower()
    ]
    dict_key_value = dict_key[0]

    return dict_key_value


def _get_stocks_list():
    """This function is used to retrieve a list of stock names that are of
    interest and use these to populate the local database.
    """

    # dir_path = os.path.dirname(__file__)
    # stock_path = os.path.join(dir_path, os.getenv("STOCK_PATH"))
    stock_path = os.getenv("STOCK_PATH")
    # Read the file
    stocks_list = ""
    with open(stock_path, "r") as stock_file:
        stocks_list = stock_file.read().split("\n")

    # Filter the undesirable records by length
    stocks_list = list(filter(_is_not_empty, stocks_list))

    logging.info("-- Stock List Found" + str(stocks_list))

    return stocks_list


def _is_not_empty(string):
    """Returns True if the string is not empty, False otherwise."""
    return len(string) > 0


def main():
    # Logger Setup
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    manage_database.main()

    avail_stocks = _get_stocks_list()

    # Cycle through the stocks to get in question:
    for stock_str in avail_stocks:
        # Singular Stock Raw Data retrieval, processing, and insertion
        raw_stock_data = get_raw_data(stock_str)
        # Santise the retrievals
        if not raw_stock_data is None:
            manage_database.db_record_insert(raw_stock_data)
            # manage_database.db_display_records()
            
    # Start the Flask API
    database_api.main()


if __name__ == "__main__":
    main()
