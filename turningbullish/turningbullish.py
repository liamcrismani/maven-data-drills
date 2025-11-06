import marimo

__generated_with = "0.17.7"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""
    # Turning Bullish

    Maven Data Drill #07 https://mavenanalytics.io/data-drills/turning-bullish

    Your Objective

    Your dataset for this drill contains daily closing prices for the **SPDR S&P 500 ETF Trust (SPY)** over the last 5 years.

    Your task is to calculate the 50-day and 200-day moving averages based on the closing price, and identify every “Golden Cross” moment – **when the short-term average (50-day) crosses from below to above the long-term average (200-day)** – signaling a potential bull market.

    ![graph](https://framerusercontent.com/images/5H9l4utlcOBL5kkzNdxEvqA.png?width=1650&height=990)

    To complete the drill, create a table containing the date, close price, and three new columns:

    - **50-day moving average:** The average closing price for the last 50 trading days, calculated for each date

    - **200-day moving average:** The average closing price for the last 200 trading days, calculated for each date

    - **Golden Cross:** A binary field (1/0) that equals 1 only on the exact date when the 50-day average crosses from below the 200-day average; otherwise 0

    ![result_table](https://framerusercontent.com/images/T3csxYZQayr0beVSf7Aigj1x7gM.png?scale-down-to=1024&width=1388&height=493)
    """)
    return


@app.cell(column=1)
def _():
    import marimo as mo
    import sys
    import os
    import polars as pl
    import matplotlib.pyplot as plt
    return mo, os, pl, sys


@app.cell(hide_code=True)
def _(os, sys):
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the parent directory to sys.path
    sys.path.append(os.path.dirname(current_dir))

    url = "https://maven-datasets.s3.us-east-1.amazonaws.com/Data+Drills/SPY_close_price_5Y.csv"

    # Download file
    from utils import download

    download(url, outpath="turningbullish/prices.csv")
    return


@app.cell
def _(pl):
    # load data
    prices = pl.read_csv(
        "turningbullish/prices.csv",
        try_parse_dates=True,
    ).sort(
        by="Date"
    )

    # rename columns
    prices.columns = ["Date", "Close Price"]
    return (prices,)


@app.cell
def _(prices):
    prices
    return


@app.cell
def _(mo, prices):
    df = mo.sql(
        f"""
        SELECT
        	"Date",
        	"Close Price",
        	AVG("Close Price") OVER(
            	ORDER BY "Date" ASC
            	RANGE BETWEEN 49 PRECEDING AND CURRENT ROW
            ) AS '50-Day Avg',
        	AVG("Close Price") OVER(
            	ORDER BY "Date" ASC
            	RANGE BETWEEN 199 PRECEDING AND CURRENT ROW
            ) AS '200-Day Avg',
        	IF("50-Day Avg" > "200-Day Avg", 1, 0) AS 'Golden Cross'
        FROM prices
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## TODO

    - create rolling 50 day avg
    - create rolling 200 day avg
    - create Golden cross col

    ### Approach
    - order data set
    - window functions for rolling average
    - case or if for golden cross

    ### Bonus
    - recreate graph shown in drill brief - a tempting challenge. The orange and blue lines are matplotlib: unmistakable!
    """)
    return


if __name__ == "__main__":
    app.run()
