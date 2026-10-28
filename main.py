#Stock Data Visualizer 
import requests

from user_input import get_user_input
from stock_api import get_stock_data
from charts import create_chart


def run_once():
    choices = get_user_input()

    try:
        # user_input returns date objects; stock_api expects "YYYY-MM-DD" strings
        stock_data = get_stock_data(
            choices["symbol"],
            choices["time_series"],
            choices["start_date"].isoformat(),
            choices["end_date"].isoformat(),
        )
    except ValueError as error:
        print(f"\nCould not get stock data: {error}")
        return
    except requests.RequestException as error:
        print(f"\nCould not reach Alpha Vantage: {error}")
        return

    create_chart(
        stock_data,
        choices["chart_type"],
        choices["symbol"],
        choices["start_date"],
        choices["end_date"],
    )


def main():
    while True:
        run_once()
        again = input("\nWould you like to view more stock data? (y/n): ")
        if again.strip().lower() != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()