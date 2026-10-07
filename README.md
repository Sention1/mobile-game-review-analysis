# Mobile Game Review Analysis

End-to-end analysis of 3,554 Google Play Store reviews from Genshin Impact, Mobile Legends, and PUBG Mobile using Python, PostgreSQL, SQL, Power BI, and DAX.

## Project Overview

This project analyzes multilingual mobile game reviews and focuses on sentiment, review behavior, translation patterns, locale alignment, complaint themes, and cross-game performance.

The workflow cleans real-world review data, engineers analytical features, loads the processed data into PostgreSQL, performs SQL analysis, and visualizes the results in Power BI.

## Tools & Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- SQLAlchemy
- Power BI
- DAX

## Project Workflow

1. Load scraped Google Play Store review data
2. Clean and transform the data with Pandas
3. Handle multilingual text and missing translations
4. Engineer sentiment, review-length, translation, and locale features
5. Load cleaned data into PostgreSQL
6. Analyze review behavior using SQL
7. Validate selected results across SQL and Power BI
8. Build an interactive Power BI dashboard

## Data Pipeline

Raw Review CSV  
→ Python / Pandas  
→ Data Cleaning & Feature Engineering  
→ PostgreSQL  
→ SQL Analysis  
→ Power BI

## Data Cleaning

The dataset contains several real-world data-quality challenges, including:

- Missing translations
- Multilingual reviews
- Inconsistent locale values
- Country and language differences
- Uneven review volume across months

Instead of removing reviews with missing translations, the pipeline preserves their rating and metadata so they remain available for analysis.

Engineered features include:

- English review text
- Sentiment label
- Sentiment score
- Review length
- Translation status
- Short-review flag
- Long-negative-review flag
- Country group
- Platform label
- Locale match

## SQL Analysis

The SQL analysis includes:

- Average review length by sentiment
- Average rating by translation status
- Sentiment comparison by country group
- Long negative review percentage by game
- Short review percentage by game
- Rating comparison by locale match
- Top-rated reviews using `DENSE_RANK()`
- Game metadata analysis using `JOIN`
- Review volume by game
- Monthly review volume and average rating
- Multi-label complaint-theme analysis

SQL techniques used include aggregation, conditional logic, CTEs, window functions, ranking, joins, date aggregation, and keyword-based text analysis.

## Power BI Dashboard

The dashboard presents review sentiment, game performance, translation behavior, locale effects, and complaint themes.

### Dashboard Overview

![Dashboard Overview](images/dashboard.png)
### Analysis Page

![Dashboard Analysis](images/analysis.png)

## Key Findings

- **57.9%** of reviews are positive, **36.8%** negative, and **5.4%** neutral.
- The overall average rating is **3.39 / 5**.
- Mobile Legends has the lowest average rating at **2.69**, compared with **3.72** for Genshin Impact and **3.87** for PUBG Mobile.
- Review length is highest around 2–3 star ratings, suggesting users provide more detail when their experience is mixed.
- Mobile Legends has a higher proportion of long negative reviews than PUBG Mobile.
- Translated reviews received a higher average rating than English reviews.
- Reviews where the review language matches the app UI language received higher ratings than locale-mismatched reviews.
- Main complaint themes among 1–2 star reviews include **Updates, Performance, Server / Connectivity, Bugs / Crashes, and Device / Compatibility**.
- Review volume is heavily concentrated in September, so monthly rating changes should be interpreted cautiously.

## Data Validation

Complaint-theme results were cross-checked between SQL and Power BI.

An initial difference was traced to the analyses using different review-text columns. After aligning the text source, filters, keywords, and multi-label logic, the results were reconciled.

This validation step helped ensure that the SQL analysis and Power BI measures were based on consistent business logic.

## Security

The PostgreSQL password is stored in environment variables.

The real `.env` file is excluded from version control using `.gitignore`.

## Project Structure

```text
mobile-game-review-analysis/
├── data/
│   └── reviews_20250928_141614.csv
├── images/
│   └── dashboard.png
├── python/
│   ├── clean_data.py
│   └── run_analysis.py
├── sql/
│   └── analysis.sql
├── .env.example
├── .gitignore
└── README.md