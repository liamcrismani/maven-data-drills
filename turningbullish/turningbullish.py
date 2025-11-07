import marimo

__generated_with = "0.17.7"
app = marimo.App(
    width="columns",
    app_title="Maven Data Drill - Turning Bullish",
)


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


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        kind="info",
        value=mo.md("**What was the close price on the date of the most recent \"golden cross\"? (numbers only, no currency symbols)**")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise solution
    """)
    return


@app.cell
def _(mo, solution):
    _df = mo.sql(
        f"""
        SELECT
            "Close Price"
        FROM
            solution
        WHERE
            "Golden Cross" = 1
        ORDER BY
            "Date" DESC
        LIMIT
            1
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Time to solve: 1hour 10 minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bonus Exercise
    Reproduce the example graph in the exercise brief.
    """)
    return


@app.cell
def _(mdates, pd, plt, solution):
    # create axis
    fig, ax = plt.subplots()

    # convert solution to pandas df
    pd_df = solution.to_pandas()
    pd_df.set_index("Date", inplace=True)
    pd_df = pd_df["2025-01-01":"2025-10-31"]

    # plot lines
    ax.plot(pd_df.index, pd_df["200-Day Avg"], label="200-Day Avg")
    ax.plot(pd_df.index, pd_df["50-Day Avg"], label="50-Day Avg")
    ax.plot(pd_df.index, pd_df["Close Price"], label="Close Price", color="gray")

    # add chart properties
    ax.set_ylabel("SPDR S&P 500 Close Price ($)")
    ax.set_xlabel("2025")

    # Customise legend
    ax.legend(
        labels=["200 day moving average", "50 day moving average", "close price"],
        loc="upper center",
        ncols=2,
        edgecolor="white",
    )

    # Annotate golden cross
    ax.annotate(
        text="Golden cross",
        xy=(pd.Timestamp(2025, 7, 1), 581.99),
        xytext=(pd.Timestamp(2025, 7, 15), 525),
        arrowprops=dict(facecolor="gold", edgecolor="gold"),
    )

    # Customise axis ticks
    ax.set_ylim([475, 700])
    ax.set_xlim([pd.Timestamp("2025-01-01"), pd_df.index[-1]])

    # use month date format instead of ISO
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    # set spine colours
    ax.spines["top"].set_color("white")
    ax.spines["right"].set_color("white")

    ax
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""
    ## Workings
    """)
    return


@app.cell
def _():
    import marimo as mo
    import sys
    import os
    import polars as pl
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    return mdates, mo, pd, pl, plt


@app.cell
def _(pl):
    # Save data url
    url = "https://maven-datasets.s3.us-east-1.amazonaws.com/Data+Drills/SPY_close_price_5Y.csv"

    # load data
    prices = pl.read_csv(
        url,
        try_parse_dates=True,
    ).sort(by="Date")

    # rename columns
    prices.columns = ["Date", "Close Price"]

    # Show data
    prices
    return (prices,)


@app.cell
def _(mo, prices):
    df = mo.sql(
        f"""
        -- cte to calc moving averages
        WITH
            cte AS (
                SELECT
                    "Date",
                    "Close Price",
                    AVG("Close Price") OVER (
                        ORDER BY
                            "Date" ASC ROWS BETWEEN 50 PRECEDING
                            AND CURRENT ROW
                    ) AS '50-Day Avg',
                    AVG("Close Price") OVER (
                        ORDER BY
                            "Date" ASC ROWS BETWEEN 200 PRECEDING
                            AND CURRENT ROW
                    ) AS '200-Day Avg'
                FROM
                    prices
            )
            -- query the cte to calculate previous/next day values
        SELECT
            *,
            -- previous value in 50 < previous value in 200
            LAG ("50-Day Avg") OVER () AS 'Previous_50',
            LAG ("200-Day Avg") OVER () AS 'Previous_200',
            -- and next value in 50 < next value in 200
            LEAD ("50-Day Avg") OVER () AS 'next_50',
            LEAD ("200-Day Avg") OVER () AS 'next_200'
        FROM
            cte
        """
    )
    return (df,)


@app.cell
def _(df, mo):
    solution = mo.sql(
        f"""
        /* query the above output, using previous/next day values to determine
        golden cross events */
        SELECT
            "Date",
            ROUND("Close Price", 2) AS 'Close Price',
            ROUND("50-Day Avg", 2) AS '50-Day Avg',
            ROUND("200-Day Avg", 2) AS '200-Day Avg',
            CASE
                WHEN "Previous_50" <= "Previous_200"
                --AND "next_50" <= "next_200"
                AND "50-Day Avg" > "200-Day Avg" THEN 1
                ELSE 0
            END AS 'Golden Cross'
        FROM
            df
        """
    )
    return (solution,)


if __name__ == "__main__":
    app.run()
