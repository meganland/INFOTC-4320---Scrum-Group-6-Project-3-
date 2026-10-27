
import os
import requests
from datetime import date

def get_stock_data(symbol, function, start_date, end_date):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise ValueError("API key is missing.")

    functions = {
        "TIME_SERIES_DAILY": "Time Series (Daily)",
        "TIME_SERIES_WEEKLY": "Weekly Time Series",
        "TIME_SERIES_MONTHLY": "Monthly Time Series"
    }

    if function not in functions:
        raise ValueError("Invalid time series function.")

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    if end < start:
        raise ValueError("End date cannot be before start date.")

    url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": symbol.upper(),
        "apikey": api_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if "Note" in data or "Information" in data:
        raise ValueError(data.get("Note") or data.get("Information"))

    series_name = functions[function]

    if series_name not in data:
        raise ValueError("No stock data returned.")

    stock_data = []

    for day, prices in data[series_name].items():
        if start <= date.fromisoformat(day) <= end:
            stock_data.append({
                "date": day,
                "open": float(prices["1. open"]),
                "high": float(prices["2. high"]),
                "low": float(prices["3. low"]),
                "close": float(prices["4. close"]),
                "volume": int(prices["5. volume"])
            })

    stock_data.sort(key=lambda item: item["date"])

    if not stock_data:
        raise ValueError("No stock prices found for these dates.")

    return stock_data


if __name__ == "__main__":
    prices = get_stock_data(
        "IBM",
        "TIME_SERIES_DAILY",
        "2026-10-01",
        "2026-10-26"
    )

    for price in prices[:5]:
        print(price)
