import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
reviews_engine = create_engine(f"postgresql://postgres:{db_password}@localhost:5432/gaming_reviews_db")


# Does review length differ by sentiment (positive/negative/neutral)?
query1 = """
    SELECT rating_label, AVG(review_length) AS avg_length
    FROM game_reviews
    GROUP BY rating_label
"""
print(pd.read_sql(query1, reviews_engine))


# Do translated reviews rate differently than non-translated ones?
query2 = """
    SELECT is_translated, AVG(rating) AS avg_rating
    FROM game_reviews
    GROUP BY is_translated
"""
print(pd.read_sql(query2, reviews_engine))


# Does sentiment differ between US and other-country reviewers?
query3 = """
    SELECT country_group, AVG(sentiment_score) AS avg_sentiment
    FROM game_reviews
    GROUP BY country_group
"""
print(pd.read_sql(query3, reviews_engine))


# Which game has the highest percentage of long, detailed negative reviews?
query4 = """
    SELECT game,
        ROUND(100.0 * SUM(CASE WHEN is_long_negative THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_long_negative
    FROM game_reviews
    GROUP BY game
    ORDER BY pct_long_negative DESC
"""
print(pd.read_sql(query4, reviews_engine))


# Which game has the highest percentage of short reviews?
query5 = """
    SELECT game,
        ROUND(100.0 * SUM(CASE WHEN is_short_review THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_short_review
    FROM game_reviews
    GROUP BY game
    ORDER BY pct_short_review DESC
"""
print(pd.read_sql(query5, reviews_engine))


# Does matching the review language to the app's UI language relate to rating?
query6 = """
    SELECT locale_match, AVG(rating) AS avg_rating
    FROM game_reviews
    GROUP BY locale_match
"""
print(pd.read_sql(query6, reviews_engine))


# What is each game's top-rated review (window function: DENSE_RANK)?
query7 = """
    WITH ranked AS (
        SELECT game, english_review, rating,
            DENSE_RANK() OVER (PARTITION BY game ORDER BY rating DESC) AS rnk
        FROM game_reviews
    )
    SELECT game, english_review, rating
    FROM ranked
    WHERE rnk = 1
"""
print(pd.read_sql(query7, reviews_engine))


# What is each game's average rating, alongside its genre (JOIN with game_metadata)?
query8 = """
    SELECT gr.game, AVG(gr.rating) AS avg_rating, gm.genre
    FROM game_reviews gr
    LEFT JOIN game_metadata gm ON gr.game = gm.game
    GROUP BY gr.game, gm.genre
"""
print(pd.read_sql(query8, reviews_engine))




# How many reviews does each game have? (sample size check for cross-game comparisons)
query9 = ("""
    SELECT game, COUNT(*) AS review_count
    FROM game_reviews
    GROUP BY game
""")
print(pd.read_sql(query9, reviews_engine))


# How do review volume and average rating trend by month? (Note: review volume is heavily skewed
# toward September, so month-over-month rating changes should be treated cautiously, not as a
# confirmed trend.)
query10 = ("""
    SELECT DATE_TRUNC('month', date::timestamp) AS month, AVG(rating) AS avg_rating, COUNT(*) AS review_count
    FROM game_reviews
    GROUP BY DATE_TRUNC('month', date::timestamp)
    ORDER BY month
""")
print(pd.read_sql(query10, reviews_engine))




# What are the most common complaint themes in 1-2 star reviews? (matches the Power BI
# "Complaint Themes" measures — keyword-based, case-insensitive, multi-label: a single
# review can count toward more than one theme if it mentions multiple issues, e.g. a review
# mentioning both "lag" and "update" counts under both Performance and Updates. Built on the
# raw review_text column to match the Power BI model exactly.)
query11 = ("""
    SELECT
        SUM(CASE WHEN review_text ILIKE '%%lag%%' OR review_text ILIKE '%%fps%%' OR review_text ILIKE '%%slow%%' OR review_text ILIKE '%%freeze%%' OR review_text ILIKE '%%loading%%' THEN 1 ELSE 0 END) AS performance,
        SUM(CASE WHEN review_text ILIKE '%%update%%' THEN 1 ELSE 0 END) AS updates,
        SUM(CASE WHEN review_text ILIKE '%%server%%' THEN 1 ELSE 0 END) AS server,
        SUM(CASE WHEN review_text ILIKE '%%bug%%' OR review_text ILIKE '%%crash%%' THEN 1 ELSE 0 END) AS bugs_crashes,
        SUM(CASE WHEN review_text ILIKE '%%device%%' THEN 1 ELSE 0 END) AS device
    FROM game_reviews
    WHERE rating <= 2
""")
print(pd.read_sql(query11, reviews_engine))


