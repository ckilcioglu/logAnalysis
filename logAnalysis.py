#!/usr/bin/env python
#
# log_analysis.py -- implementation of a log analysis service running on
#                    published news
#

import psycopg2
from psycopg2 import sql

# Create a table (view) where 'authors', 'articles' and 'log' tables are joined
# Join rules:
#   articles <-> log                : log.path = '/article/' + articles.slug
#   authors <-> (articles <-> log)  : authors.id = articles.author
#
# Left join is used since some authors may not have written any article and
# some articles may not have been viewed.
BIG_VIEW_QUERY = """
    CREATE VIEW big_view AS
    SELECT
        authors.name AS name,
        articles.title AS title
    FROM authors LEFT JOIN
    (articles LEFT JOIN log ON log.path = '/article/' || articles.slug)
    ON authors.id = articles.author"""


# Create a table (view) where logs are represented with date
# 'status' filed is kept in this view to observe success rate later on
LOG_WITH_DATES_VIEW_QUERY = """
    CREATE VIEW log_with_dates AS
    SELECT id, status, date(time) AS exact_day
    FROM log"""


# Query which gives the most popular ones as given in {0} variable
POPULAR_TYPE_QUERY = """
    SELECT
        {0},
        count(*) AS hits
    FROM big_view
    GROUP BY {0}
    ORDER BY hits DESC"""


# Query which gives the most popular ones as given in {0} variable
# and limits to see the top ones
POPULAR_TYPE_QUERY_LIMIT = POPULAR_TYPE_QUERY + """
    LIMIT %s"""


# Query which gives the days ordered by their error counts with greater than
# given percentage
# Two subqueries are executed with:
#   1. Count of all calls for each day system is logged
#   2. Count of errorous calls for each day system is logged
# These two tables are joined on dates and percentage is calculated and
# selected where error percentage is greater than some given value.
ERROR_PERCENTAGE_QUERY = """
    SELECT * FROM
    (SELECT
        x.exact_day as call_day,
        cast(wrong_calls AS double precision)/all_calls AS errorous_perc
        FROM
        (SELECT
            exact_day,
            count(*) AS all_calls
            FROM log_with_dates
            GROUP BY exact_day) AS x
        INNER JOIN
        (SELECT exact_day,
            count(*) AS wrong_calls
            FROM log_with_dates
            WHERE status NOT LIKE '2%%'
            GROUP BY exact_day) AS y
        ON x.exact_day = y.exact_day
        ORDER BY errorous_perc DESC) AS subq
    WHERE errorous_perc > %s"""


def connect():
    """Connect to the PostgreSQL database named "news"

    Returns:
        A tupple which holds the database connection and its health status
        First element   : connection to database
        Second element  : health status (1:OK, -1:NOK)
    """
    try:
        conn = psycopg2.connect("dbname=news")
    except:
        print "I am unable to connect to the database"
        return (None, -1)
    return (conn, 1)


def createViews(theDB):
    """Create some common views during analysis

    Args:
        theDB   : PostgreSQL database connection

    Returns:
        None
    """
    cur = theDB.cursor()
    cur.execute(BIG_VIEW_QUERY)
    cur.execute(LOG_WITH_DATES_VIEW_QUERY)


def dropViews(theDB):
    """Remove the views created for analysis purpose

    Args:
        theDB   : PostgreSQL database connection

    Returns:
        None
    """
    cur = theDB.cursor()
    cur.execute("DROP VIEW big_view;")
    cur.execute("DROP VIEW log_with_dates;")


def disconnect(theDB):
    """Close the database connection

    Args:
        theDB   : PostgreSQL database connection

    Returns:
        None
    """
    theDB.close()


def getMostPopularArticles(theDB, theLimit):
    """Prints the most popular articles ordered by view counts

    Args:
        theDB       : PostgreSQL database connection
        theLimit    : number of top articles you like to see
                      (0 to see all of them)

    Returns:
        None
    """
    cur = theDB.cursor()
    if theLimit < 1:
        print "Articles according to popularity:"
        cur.execute(
            sql.SQL(POPULAR_TYPE_QUERY).format(sql.Identifier('title')))
    else:
        if theLimit == 1:
            print "Most popular article:"
        else:
            print "Most popular " + str(theLimit) + " articles:"
        cur.execute(
            sql.SQL(POPULAR_TYPE_QUERY_LIMIT).format(sql.Identifier('title')),
            (theLimit,))
    rows = cur.fetchall()
    for row in rows:
        print ' * "' + row[0] + '"" - ' + str(row[1]) + ' views'
    return


def getMostPopularAuthors(theDB, theLimit):
    """Prints the most popular authors ordered by view counts

    Args:
        theDB       : PostgreSQL database connection
        theLimit    : number of top articles you like to see
                      (0 to see all of them)

    Returns:
        None
    """
    cur = theDB.cursor()
    if theLimit < 1:
        print "Article authors according to popularity:"
        cur.execute(
            sql.SQL(POPULAR_TYPE_QUERY).format(sql.Identifier('name')))
    else:
        if theLimit == 1:
            print "Most popular article author:"
        else:
            print "Most popular " + str(theLimit) + " article authors:"
        cur.execute(
            sql.SQL(POPULAR_TYPE_QUERY_LIMIT).format(sql.Identifier('name')),
            (theLimit,))
    rows = cur.fetchall()
    for row in rows:
        print " * " + row[0] + " - " + str(row[1]) + " views"
    return


def getErrorousDays(theDB, theErrorRatio):
    """Prints the days and their error percantages where this percantage is
    greater than given ratio. Precision is determined as 0.1%.

    Args:
        theDB           : PostgreSQL database connection
        theErrorRatio   : Error ratio represented by double precision (<1.0)

    Returns:
        None
    """
    print "The days in which more than %.1f%s of requests are errorous:" % \
        (float(theErrorRatio*100), "%")
    cur = theDB.cursor()
    cur.execute(ERROR_PERCENTAGE_QUERY, (theErrorRatio,))
    rows = cur.fetchall()
    for row in rows:
        dateString = "{:%B %d, %Y}".format(row[0])
        print " * " + dateString + " - " + str(round(row[1] * 100, 2)) + \
            ("%s errors" % "%")
    return


# Main part of code running after program is called
if __name__ == '__main__':
    theDB, connection = connect()
    if connection == 1:
        createViews(theDB)
        getMostPopularArticles(theDB, 3)
        getMostPopularAuthors(theDB, 0)
        getErrorousDays(theDB, 0.01)
        dropViews(theDB)
        disconnect(theDB)
