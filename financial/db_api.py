from flask import Flask, jsonify, request
import sqlite3
import os
import json


app = Flask(__name__)


@app.route("/")
def hello():
    json_data = {
        "data": "Null",
        "info": """Thanks! Try /api, 
                 /api/financial_data, or /api/statistics""",
    }
    return jsonify(json_data)


@app.route("/api")
def get_data():
    conn = sqlite3.connect("./financial/stock_fortnight.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financial_data")
    data = cursor.fetchall()
    conn.close()

    return jsonify(data)


@app.route("/api/financial_data")
def my_table_query():
    # Get the values of the pagination parameters
    limit = int(request.args.get("limit", default=5))
    page = int(request.args.get("page", default=1))
    start_date = request.args.get("start_date", default=None)
    end_date = request.args.get("end_date", default=None)
    symbol = request.args.get("symbol", default=None)

    # Create the SQL Query
    sql_query = "SELECT * FROM financial_data WHERE length(symbol)>=0 "

    # Specific situations
    if start_date:
        sql_query += f" AND date >= '{start_date}'"
    if end_date:
        sql_query += f" AND date <= '{end_date}'"
    if symbol:
        sql_query += f" AND symbol == '{symbol}'"

    # Get the Data
    error_message = ""
    conn = sqlite3.connect("./financial/stock_fortnight.db")
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        conn.close()

    except Exception as e:
        error_message = str(e)

    # Create Error Information if it exists
    error_data = {"error": error_message}

    # Perform operations based on pagination parameters
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_data = data[start_index:end_index]

    # Prepare the response
    response = {
        "data": paginated_data,
        "pagination": {
            "count": len(data),
            "limit": limit,
            "page": page,
            "pages": int((len(data) / limit)),
        },
        # Placeholder for error info (if applicable)
        "info": json.dumps(error_data),
    }

    # Return the response as JSON
    return jsonify(response)


@app.route("/api/statistics")
def my_statistics_query():
    # Get the values of the pagination parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    symbol = request.args.get("symbol")

    # The information to return
    response = ""

    if start_date and end_date and symbol:
        # Create the SQL Query
        sql_query = """SELECT ROUND(AVG(open_price),2), 
        ROUND(AVG(close_price),2), ROUND(AVG(volume), 0) 
        FROM financial_data WHERE length(symbol)>=0 """

        # Specific situations
        if start_date:
            sql_query += f" AND date >= '{start_date}'"
        if end_date:
            sql_query += f" AND date <= '{end_date}'"
        if symbol:
            sql_query += f" AND symbol == '{symbol}'"

        # Get the Data
        error_message = ""
        conn = sqlite3.connect("./financial/stock_fortnight.db")
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            data = cursor.fetchall()
            conn.close()

        except Exception as e:
            error_message = str(e)

        # Create Error Information if it exists
        error_data = {"error": error_message}

        # Perform operations based on pagination parameters
        open_price_avg = data[0][0]
        close_price_avg = data[0][1]
        volume_avg = data[0][2]

        response = {
            "data": {
                "start_date": start_date,
                "end_date": end_date,
                "symbol": symbol,
                "average_daily_open_price": open_price_avg,
                "average_daily_close_price": close_price_avg,
                "average_daily_volume": volume_avg,
            },
            "info": {"error": error_message},
        }
    else:
        response = {
            "data": "Null",
            "info": {"error": "start_date, end_date, or symbol emtpy"},
        }

    # Return the response as JSON
    return jsonify(response)

def main():
    """This is the main function of the db_api.py file so it can be used in
       another module
    """
    port_used = os.getenv("PORT_USED")
    app.run(host="0.0.0.0", port=port_used)

if __name__ == "__main__":
    main()
