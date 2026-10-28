
import plotly.graph_objects as go
import plotly.io as pio

# Make sure fig.show() opens the user's default browser
pio.renderers.default = "browser"

PRICE_FIELDS = [
    ("open", "Open"),
    ("high", "High"),
    ("low", "Low"),
    ("close", "Close"),
]


def build_chart(stock_data, chart_type, symbol, start_date, end_date):
    #Return a Plotly figure for the given stock data.

    
    if chart_type not in ("bar", "line"):
        raise ValueError("Chart type must be 'bar' or 'line'.")

    if not stock_data:
        raise ValueError("There is no stock data to chart.")

    dates = [row["date"] for row in stock_data]
    fig = go.Figure()

    for key, label in PRICE_FIELDS:
        values = [row[key] for row in stock_data]
        if chart_type == "line":
            fig.add_trace(go.Scatter(x=dates, y=values, mode="lines+markers", name=label))
        else:
            fig.add_trace(go.Bar(x=dates, y=values, name=label))

    fig.update_layout(
        title=f"Stock Data for {symbol}: {start_date} to {end_date}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        barmode="group",
        hovermode="x unified",
        legend_title="Price",
    )
    return fig


def create_chart(stock_data, chart_type, symbol, start_date, end_date):
    #Build the chart and open it in the default web browser.
    fig = build_chart(stock_data, chart_type, symbol, start_date, end_date)
    fig.show()


if __name__ == "__main__":
    # Quick test with sample data
    sample = [
        {"date": "2026-10-20", "open": 250.0, "high": 254.1, "low": 248.7, "close": 253.2, "volume": 1000},
        {"date": "2026-10-21", "open": 253.2, "high": 256.0, "low": 251.9, "close": 255.4, "volume": 1200},
        {"date": "2026-10-22", "open": 255.4, "high": 257.3, "low": 252.0, "close": 252.8, "volume": 900},
    ]
    create_chart(sample, "line", "TEST", "2026-10-20", "2026-10-22")