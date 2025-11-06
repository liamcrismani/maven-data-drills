import marimo

__generated_with = "0.16.5"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""# Maven Data Drills - Rolling up, Looking Back""")
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import polars as pl
    import sys
    import os

    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the parent directory to sys.path
    sys.path.append(os.path.dirname(current_dir))

    # Now you can import the module
    from utils import download, unzip, cleanup


    # Download and extract this tasks files
    url = "https://maven-datasets.s3.us-east-1.amazonaws.com/Data+Drills/coffee_shop_sales.csv"

    download(url, outpath="coffeesales\coffee_sales.csv")
    return mo, pl


@app.cell
def _(pl):
    sales = pl.read_csv("coffeesales\coffee_sales.csv", try_parse_dates=True)
    sales
    return (sales,)


@app.cell
def _(mo, sales):
    agg = mo.sql(
        f"""
        -- First just aggregate monthly sales
        SELECT
            MONTH(date) AS 'month',
            store,
            ROUND(SUM(sales)) AS 'sales'
        FROM
            sales
        GROUP BY
            MONTH(date),
            store
        ORDER BY
        	MONTH(date),
        	store
        """
    )
    return (agg,)


@app.cell
def _(agg, mo):
    final_table = mo.sql(
        f"""
        -- next, find previous months sales
        SELECT
            *,
            LAG (sales) OVER (
                PARTITION BY
                    store
            	ORDER BY "month"
            ) AS 'last_month_sales',
            sales - last_month_sales AS 'difference'
        FROM
            agg
        """
    )
    return (final_table,)


@app.cell
def _(final_table, pl):
    solution = final_table.filter(
        pl.col("month") == 5, pl.col("store") == "Astoria"
    ).select("difference")
    round(solution[0,0])
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Your Objective

    You’ve been given a table with raw data for individual coffee shop transactions. Your task is to aggregate the total sales by month and store, then calculate the month-over-month change in sales for each store (in dollars).

    Example input and output:
    ![Example](https://framerusercontent.com/images/KzJBIHeseB8isWzTTTEaMkobA.png?width=1439&height=728)
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        value=mo.md("## Question\nWhat was the difference in sales from April to May for the Astoria location? (digits only, rounded to the nearest dollar)"),
        kind="info"
    )
    return


if __name__ == "__main__":
    app.run()
