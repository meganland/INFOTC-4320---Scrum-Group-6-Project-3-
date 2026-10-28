
import os
import requests
from datetime import date, datetime


def get_stock_data(symbol, function, start_date, end_date):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise ValueError("Alpha Vantage API key is missing.")

    functions = {
        "TIME_SERIES_INTRADAY": "Time Series (5min)",
        "TIME_SERIES_DAILY": "Time Series (Daily)",
        "TIME_SERIES_WEEKLY": "Weekly Time Series",
        "TIME_SERIES_MONTHLY": "Monthly Time Series"
    }

    if function not in functions:
        raise ValueError("Invalid time series function.")

    # Accept both date objects and YYYY-MM-DD strings
    if isinstance(start_date, str):
        start = date.fromisoformat(start_date)
    else:
        start = start_date

    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date

    if end < start:
        raise ValueError("End date cannot be before start date.")

    url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": symbol.strip().upper(),
        "apikey": api_key
    }

    # Intraday requires an interval
    if function == "TIME_SERIES_INTRADAY":
        params["interval"] = "5min"
        params["outputsize"] = "full"

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Handle API errors and limits
    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if "Note" in data:
        raise ValueError(data["Note"])

    if "Information" in data:
        raise ValueError(data["Information"])

    series_name = functions[function]

    if series_name not in data:
        raise ValueError("No stock data was returned by the API.")

    stock_data = []

    for timestamp, prices in data[series_name].items():

        # Works with both dates and intraday timestamps
        record_date = datetime.fromisoformat(timestamp).date()

        if start <= record_date <= end:
            stock_data.append({
                "date": timestamp,
                "open": float(prices["1. open"]),
                "high": float(prices["2. high"]),
                "low": float(prices["3. low"]),
                "close": float(prices["4. close"]),
                "volume": int(prices["5. volume"])
            })

    stock_data.sort(key=lambda item: item["date"])

    if not stock_data:
        raise ValueError(
            "No stock prices found for the selected date range."
        )

    return stock_data


if __name__ == "__main__":
    # Test the API using daily stock data
    try:
        prices = get_stock_data(
            "IBM",
            "TIME_SERIES_DAILY",
            "2026-10-01",
            "2026-10-26"
        )

        for price in prices[:5]:
            print(price)

    except (ValueError, requests.RequestException) as error:
        print("Error:", error)
