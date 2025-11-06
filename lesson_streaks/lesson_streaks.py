import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Data Drill - Lessons streaks
    Your Objective

    You work for a popular language learning company and have a table containing ~900,000 lesson completions, including the date, user, and lesson ID.

    Your task is to create a leaderboard of the top 10 users, based on the longest daily active streaks.

        The streak length is the number of consecutive days with at least one lesson completion

        For the purpose of this drill, consider the current date to be 2025-09-29

        For a streak to be considered “active”, the user must have completed a lesson on the previous day (2025-09-28)

    https://mavenanalytics.io/data-drills/streak-leaderboard
    """
    )
    return


@app.cell
def _():
    import polars as pl

    # read in data
    data = pl.read_csv('LessonStreaks.csv', try_parse_dates=True)
    return (data,)


@app.cell
def _(data, mo):
    df_transformed = mo.sql(
        f"""
        SELECT
        	DISTINCT date,
            user_id,
            user_name
        FROM data
        WHERE date < '2025-09-29'
        ORDER BY user_id, date DESC
        """
    )
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""we only need the user and the date, lesson is irrelavent""")
    return


if __name__ == "__main__":
    app.run()
