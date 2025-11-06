import marimo

__generated_with = "0.16.5"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(
        r"""
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
    """
    )
    return


@app.cell(column=1)
def _():
    import marimo as mo
    import sys
    import os
    import polars as pl
    import matplotlib.pyplot as plt
    return (mo,)


@app.cell
def _():
    from utils import download
    return


if __name__ == "__main__":
    app.run()
