import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Maven Data Drills - Spot the Sale

    You've been given two tables:

        A table with promotional periods, each with a start and end date

        A table with orders, each with an order date and quantity

     Your task is to join each transaction to the promotion active on its order date.

    Example:

    ![Example](https://framerusercontent.com/images/UzxnkQNwlGdRaDL3M993Bv2Zo.png?width=1575&height=746)
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        value=mo.md("##Question\nHow many orders were placed outside of promotional periods?"),
        kind="info"
    )
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd

    import sys
    import os

    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the parent directory to sys.path
    sys.path.append(os.path.dirname(current_dir))

    # Now you can import the module
    from utils import download, unzip, cleanup


    # Download and extract this tasks files
    url = "https://maven-datasets.s3.us-east-1.amazonaws.com/Data+Drills/promotions.zip"

    download(url, outpath="files.zip")
    unzip(path="files.zip", outpath="promotions\\")
    return mo, pd


@app.cell
def _(pd):
    orders = pd.read_csv("promotions\orders.csv", parse_dates=["order_date"])
    promotions = pd.read_csv("promotions\promotions.csv", parse_dates=["start_date"])
    return orders, promotions


@app.cell
def _(orders, pd, promotions):
    merged = pd.merge_asof(
        left=orders.sort_values(by="order_date"),
        right=promotions.sort_values(by="start_date"),
        left_on="order_date",
        right_on="start_date",
        direction="backward"
    ).query("order_date <= end_date")
    merged
    return (merged,)


@app.cell
def _(merged, orders):
    table_solution = merged[["order_id", "order_date", "order_quantity", "promo_id"]]
    question_solution = orders.shape[0] - table_solution.shape[0]
    question_solution
    return


@app.cell
def _(mo, orders):
    mo.ui.table(orders)
    return


@app.cell
def _(mo, promotions):
    mo.ui.table(promotions)
    return


if __name__ == "__main__":
    app.run()
