This project cleans and analyzes 3,554 real, scraped Google Play Store reviews across three mobile games — Genshin Impact, Mobile Legends, and PUBG Mobile. It handles genuine real-world messiness (missing translations, multilingual text, inconsistent locale data), engineers features for sentiment and behavior analysis, loads the data into PostgreSQL, and compares the three games using SQL (aggregation, window functions, a JOIN against a game-metadata table, and keyword-based complaint-theme analysis) and a two-page interactive Power BI dashboard.

Pipeline
Kaggle CSV (raw scraped reviews) → pandas (clean/transform, feature engineering) → PostgreSQL (store) → SQL (analyze) → Power BI (visualize)

No API was used, by design — the goal was practicing data cleaning and joining on genuinely messy data, a skill an API's typically clean JSON doesn't exercise.

Project Structure
clean_data.py — loads the raw CSV, engineers 12 derived columns (sentiment label, review length, translation status, locale match, etc.), and loads both game_reviews and a small game_metadata reference table into PostgreSQL.
analysis.py — 11 SQL queries (run via pandas) covering aggregation, percentage calculations, a window function (DENSE_RANK), a JOIN against game_metadata, a review-volume/rating trend by month, and a multi-label keyword-based complaint-theme breakdown.
.env (not included in this repo) — holds the database password. See setup below.
Setup
Install dependencies:
   pip install pandas sqlalchemy psycopg2-binary python-dotenv
Create a .env file in the project root with:
   DB_PASSWORD=your_postgres_password
Make sure PostgreSQL is running locally. clean_data.py creates the gaming_reviews_db database's tables automatically.
Run clean_data.py first to load and clean the data, then run analysis.py to see the SQL results.
Data Cleaning Highlights
Missing translations: ~1,727 of 3,554 reviews needed translation but some had none available. Rather than dropping these rows (which would have introduced bias by language/country), a unified english_review column falls back to a clear placeholder for untranslatable rows, preserving every review's rating and metadata.
Case-sensitivity bugs: real country codes ('us', not 'US') required verifying exact values before filtering, rather than assuming standard casing.
Multilingual data: 36 distinct languages detected across reviews, handled via a locale-match feature comparing each review's language to the app's UI language.
Cross-checking a Power BI finding against SQL: a keyword-based "complaint theme" analysis, prototyped in the Power BI dashboard, initially appeared to conflict with a SQL version testing the same idea. Tracing the discrepancy showed it came down to which text column each was built on (review_text vs. the cleaned english_review) — once aligned on the same column, both tools produced identical results, confirming the dashboard's numbers. That reconciliation query is documented in analysis.py.
Key Findings
57.9% of reviews are positive, 36.8% negative, only 5.4% neutral — people review when they feel strongly, rarely when lukewarm. Overall average rating: 3.39/5.
Mobile Legends has the lowest average rating (2.69) — notably below PUBG Mobile (3.87) and Genshin Impact (3.72) — despite a comparable review volume (1,266 vs. 964–1,324 for the others), ruling out sample-size bias as the explanation.
Review length peaks at 2-3 star ratings (163 characters average) and is shortest at 5 stars (85 characters) — reviewers write the most when their experience is mixed, not when it's extreme in either direction.
Mobile Legends has more than double the rate of long, detailed negative reviews (11.85%) compared to PUBG Mobile (4.46%); PUBG Mobile has the highest rate of short reviews overall (46.68%), consistent with a low-effort review culture for that game specifically.
Translated (non-English) reviews rate higher on average (3.51 vs. 3.26 for English reviews) — a pattern that tracks a parallel finding: reviews from outside the US (mostly Saudi Arabia, the dataset's other major country group) average notably higher sentiment (0.41) than US reviews (0.06).
Locale-matched reviews rate higher (3.49) than reviews written in a language that doesn't match the app's UI language (2.94).
Top complaint themes in 1-2 star reviews (keyword-based, multi-label — a review can count under more than one theme): Updates (100 mentions), Performance (79-105 depending on keyword scope), Bugs/Crashes (27-28), Device/Compatibility (16-28), Server/Connectivity (32).
Review volume is heavily skewed toward September (2,999 of 3,554 reviews), so the apparent June-to-September rating decline (3.64 → 3.34) should be treated as a directional signal, not a confirmed trend, given the imbalanced sample sizes per month.
Dashboard

Built in Power BI across two pages, connected directly to PostgreSQL:

Overview: KPI summary cards, average rating by game (with genre), review length by star rating, sentiment by country, and a rating-sentiment breakdown, all filterable by game, country, sentiment, and rating range.
Analysis (Per-Game Deep Dive): long-negative and short-review percentage breakdowns per game, a complaint-theme chart, review volume and rating trend by month, and a Key Insights panel.
Tech Stack

Python (pandas), PostgreSQL, SQL (window functions, CASE WHEN, JOIN, aggregates, keyword pattern matching), Power BI (DAX measures, interactive slicers, multi-page reports).
