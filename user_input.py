
import re
from datetime import datetime

# menu 

CHART_TYPES = {
    "1": ("Bar", "bar"),
    "2": ("Line", "line"),
}

TIME_SERIES = {
    "1": ("Intraday", "TIME_SERIES_INTRADAY"),
    "2": ("Daily", "TIME_SERIES_DAILY"),
    "3": ("Weekly", "TIME_SERIES_WEEKLY"),
    "4": ("Monthly", "TIME_SERIES_MONTHLY"),
}

DATE_FORMAT = "%Y-%m-%d"

# validators 

def validate_symbol(text):
    symbol = text.strip().upper()

    if not symbol:
        raise ValueError("The symbol cannot be empty.")

    return symbol


def validate_menu_choice(text, options):
    choice = text.strip()
    if choice not in options:
        valid = ", ".join(options)
        raise ValueError(f"Please enter one of: {valid}.")
    return options[choice][1]


def validate_date(text):
    text = text.strip()
    # strptime would accept 2024-1-5, so require the exact YYYY-MM-DD shape
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise ValueError("Use the format YYYY-MM-DD (for example 2024-01-31).")
    try:
        return datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        raise ValueError("That is not a real calendar date.")


def validate_date_range(start_date, end_date):
    if end_date < start_date:
        raise ValueError(
            f"The end date ({end_date}) cannot be before the start date ({start_date})."
        )


# prompts

def _ask(prompt, validator):
    while True:
        try:
            return validator(input(prompt))
        except ValueError as error:
            print(f"  Invalid input: {error}")


def _ask_menu(title, prompt, options):
    print(f"\n{title}")
    print("-" * len(title))

    for key, (label, _) in options.items():
        print(f"{key}. {label}")

    def menu_validator(text):
        return validate_menu_choice(text, options)

    return _ask(prompt, menu_validator)


def ask_symbol():
    print("\nStock Data Visualizer")
    print("---------------------")
    return _ask("Enter the stock symbol you are looking for: ", validate_symbol)


def ask_chart_type():
    return _ask_menu("Chart Types", "Enter the chart type you want (1, 2): ", CHART_TYPES)


def ask_time_series():
    return _ask_menu(
        "Select the Time Series of the chart you want to Generate",
        "Enter time series option (1, 2, 3, 4): ",
        TIME_SERIES,
    )


def ask_dates():
    print()
    start_date = _ask("Enter the start date (YYYY-MM-DD): ", validate_date)
    while True:
        end_date = _ask("Enter the end date (YYYY-MM-DD): ", validate_date)
        try:
            validate_date_range(start_date, end_date)
            return start_date, end_date
        except ValueError as error:
            print(f"  Invalid input: {error}")


def get_user_input():
    """Run all prompts and return the user's choices as a dictionary."""
    symbol = ask_symbol()
    chart_type = ask_chart_type()
    time_series = ask_time_series()
    start_date, end_date = ask_dates()
    return {
        "symbol": symbol,
        "chart_type": chart_type,
        "time_series": time_series,
        "start_date": start_date,
        "end_date": end_date,
    }


if __name__ == "__main__":
    print(get_user_input())
