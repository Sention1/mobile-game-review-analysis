-- =========================================================
-- Mobile Game Review Analysis
-- PostgreSQL
-- =========================================================


-- =========================================================
-- 1. Average review length by sentiment
-- =========================================================

    SELECT
        rating_label,
        AVG(review_length) AS avg_length
    FROM game_reviews
    GROUP BY rating_label;



-- =========================================================
-- 2. Average rating by translation status
-- =========================================================

    SELECT
        is_translated,
        AVG(rating) AS avg_rating
    FROM game_reviews
    GROUP BY is_translated;



-- =========================================================
-- 3. Average sentiment by reviewer country group
-- =========================================================

    SELECT
        country_group,
        AVG(sentiment_score) AS avg_sentiment
    FROM game_reviews
    GROUP BY country_group;



-- =========================================================
-- 4. Percentage of long negative reviews by game
-- =========================================================

    SELECT
        game,
        ROUND(
            (
                100.0
                * SUM(
                    CASE
                        WHEN is_long_negative THEN 1
                        ELSE 0
                    END
                )
                / COUNT(*)
            )::numeric,
            2
        ) AS pct_long_negative
    FROM game_reviews
    GROUP BY game
    ORDER BY pct_long_negative DESC;



-- =========================================================
-- 5. Percentage of short reviews by game
-- =========================================================

    SELECT
        game,
        ROUND(
            (
                100.0
                * SUM(
                    CASE
                        WHEN is_short_review THEN 1
                        ELSE 0
                    END
                )
                / COUNT(*)
            )::numeric,
            2
        ) AS pct_short_review
    FROM game_reviews
    GROUP BY game
    ORDER BY pct_short_review DESC;



-- =========================================================
-- 6. Average rating by locale match
-- =========================================================

    SELECT
        locale_match,
        AVG(rating) AS avg_rating
    FROM game_reviews
    GROUP BY locale_match;



-- =========================================================
-- 7. Top-rated reviews by game
-- =========================================================

    WITH ranked_reviews AS (
        SELECT
            game,
            english_review,
            rating,
            DENSE_RANK() OVER (
                PARTITION BY game
                ORDER BY rating DESC
            ) AS review_rank
        FROM game_reviews
    )

    SELECT
        game,
        english_review,
        rating,
        review_rank
    FROM ranked_reviews
    WHERE review_rank = 1;



-- =========================================================
-- 8. Average rating by game and genre
-- =========================================================

    SELECT
        gr.game,
        gm.genre,
        AVG(gr.rating) AS avg_rating
    FROM game_reviews gr
    LEFT JOIN game_metadata gm
        ON gr.game = gm.game
    GROUP BY
        gr.game,
        gm.genre
    ORDER BY avg_rating DESC;



-- =========================================================
-- 9. Review count by game
-- =========================================================

    SELECT
        game,
        COUNT(*) AS review_count
    FROM game_reviews
    GROUP BY game
    ORDER BY review_count DESC;



-- =========================================================
-- 10. Monthly review volume and average rating
-- =========================================================

    SELECT
        DATE_TRUNC(
            'month',
            date::timestamp
        ) AS month,
        AVG(rating) AS avg_rating,
        COUNT(*) AS review_count
    FROM game_reviews
    GROUP BY DATE_TRUNC(
        'month',
        date::timestamp
    )
    ORDER BY month;



-- =========================================================
-- 11. Complaint themes in 1-2 star reviews
-- Multi-label keyword analysis
-- =========================================================

    SELECT
        SUM(
            CASE
                WHEN review_text ILIKE '%lag%'
                OR review_text ILIKE '%fps%'
                OR review_text ILIKE '%slow%'
                OR review_text ILIKE '%freeze%'
                OR review_text ILIKE '%loading%'
                THEN 1
                ELSE 0
            END
        ) AS performance,

        SUM(
            CASE
                WHEN review_text ILIKE '%update%'
                THEN 1
                ELSE 0
            END
        ) AS updates,

        SUM(
            CASE
                WHEN review_text ILIKE '%server%'
                THEN 1
                ELSE 0
            END
        ) AS server,

        SUM(
            CASE
                WHEN review_text ILIKE '%bug%'
                OR review_text ILIKE '%crash%'
                THEN 1
                ELSE 0
            END
        ) AS bugs_crashes,

        SUM(
            CASE
                WHEN review_text ILIKE '%device%'
                THEN 1
                ELSE 0
            END
        ) AS device

    FROM game_reviews
    WHERE rating <= 2;