import marimo

__generated_with = "0.16.5"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(activity, mo, users):
    joined = mo.sql(
        f"""
        -- create joined table
        SELECT
            u.id AS 'id',
            u.created_at AS 'created_at',
            a.date AS 'date',
            a.finished::BOOLEAN AS 'finished'
        FROM
            activity a
            LEFT JOIN users u ON u.id = a.user_id
        """
    )
    return (joined,)


@app.cell(hide_code=True)
def _(joined, mo):
    grouped = mo.sql(
        f"""
        -- get aggregated stats
        WITH cte AS (
        SELECT
            id,
            created_at,
            MIN(date) AS 'first_date',
            MAX(date) AS 'last_date',
    
        FROM
            joined
        WHERE finished = TRUE
        GROUP BY
            id,
            created_at
        )

        SELECT
            cte.id AS 'id',
            cte.created_at AS 'created_at',
            cte.first_date AS 'first_date',
            cte.last_date AS 'last_date',
            COUNT_IF(j.finished) AS 'finished',
            -- we assume that finished does not included started
            COUNT(
                CASE j.finished
                    WHEN FALSE THEN 1
                    ELSE 0
                END
            ) AS 'started'
        FROM cte
        INNER JOIN joined j ON cte.id = j.id
        GROUP BY cte.id, cte.created_at, cte.first_date, cte.last_date
        """
    )
    return (grouped,)


@app.cell(hide_code=True)
def _(activity, grouped, mo):
    final = mo.sql(
        f"""
        SELECT
        	g.id AS 'id',
            g.created_at AS 'created_at',
            g.first_date AS 'first_date',
            a1.movie_name AS 'First_name',
            g.last_date AS 'last_date',
            a2.movie_name AS 'last_name',
            g.started AS 'started',
            g.finished AS 'finished'
        FROM
        	grouped g
        	INNER JOIN activity a1
        	ON a1.date = g.first_date
        	INNER JOIN activity a2 ON a2.date = g.last_date
        """
    )

    solution = mo.sql(
        f"""
        SELECT
            COUNT(*)
        FROM final
        WHERE last_name = 'Fight Club'
        """
    )

    print("Final table:\n")
    final
    return final, solution


@app.cell(hide_code=True)
def _(solution):
    print("Number of users who saw fight club as their last movie:\n")
    solution
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Maven Analytics Data Drills - Movie Metrics
    https://mavenanalytics.io/data-drills/movie-metrics

    You've been given a table of Netflix users and another with their viewing activity, including the movie name, date started, and whether they finished it.

    Your task is to engineer these new features for each user, based on their activity:

        Date from the first movie they finished

        Name of the first movie they finished

        Date from the last movie they finished

        Name of the last movie they finished

        Movies started

        Movies finished

    ![Example](https://framerusercontent.com/images/L6wub14jGNcwG0zLLxlVyIWv85c.png?width=1770&height=433)

    How many users have "Fight Club" as the last film they've seen?
    """
    )
    return


@app.cell
def _(activity, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM activity
        """
    )
    return


@app.cell
def _(mo, users):
    _df = mo.sql(
        f"""
        SELECT * FROM users
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl


    # loads data sets
    activity = pl.read_csv('movie_metrics/activity.csv', try_parse_dates=True)
    users = pl.read_csv('movie_metrics/users.csv', try_parse_dates=True)
    return activity, mo, users


if __name__ == "__main__":
    app.run()
