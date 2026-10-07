import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

db_password = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql://postgres:{db_password}@localhost:5432/gaming_reviews_db"
)


# -------------------------
# Load raw data
# -------------------------

df = pd.read_csv("data/reviews_20250928_141614.csv")

# -------------------------
# Feature engineering
# -------------------------

df["english_review"] = df["review_text"]

non_english_mask = df["lang_detected"] != "en"

df.loc[
    non_english_mask & df["translation_en"].notna(),
    "english_review"
] = df.loc[
    non_english_mask & df["translation_en"].notna(),
    "translation_en"
]

df.loc[
    non_english_mask & df["translation_en"].isna(),
    "english_review"
] = "no translation available"


df["has_title"] = df["title"].notna()


df["rating_label"] = "neutral"
df.loc[df["rating"] >= 4, "rating_label"] = "positive"
df.loc[df["rating"] <= 2, "rating_label"] = "negative"


df["review_length"] = (
    df["english_review"]
    .fillna("")
    .str.len()
)


df["is_translated"] = (
    df["lang_detected"] != "en"
)


df["country_group"] = "other"
df.loc[df["country"] == "us", "country_group"] = "us"


df["sentiment_score"] = 0
df.loc[df["rating"] >= 4, "sentiment_score"] = 1
df.loc[df["rating"] <= 2, "sentiment_score"] = -1


df["is_short_review"] = (
    df["review_length"] < 50
)


df["platform_label"] = "Other"
df.loc[
    df["platform"] == "google_play",
    "platform_label"
] = "Play Store"


df["is_long_negative"] = (
    (df["rating"] <= 2)
    & (df["review_length"] > 200)
)


df["rating_and_length_flag"] = "other"
df.loc[
    df["is_long_negative"],
    "rating_and_length_flag"
] = "long_negative"


df["locale_match"] = (
    df["lang_detected"] == df["lang_ui"]
)


# -------------------------
# Validation
# -------------------------

print("Rows:", len(df))
print("Duplicate rows:", df.duplicated().sum())

print("\nNull values:")
print(df.isnull().sum())

print("\nRating labels:")
print(df["rating_label"].value_counts())

print("\nTranslation status:")
print(df["is_translated"].value_counts())

print("\nGames:")
print(df["game"].value_counts())


# -------------------------
# Game metadata
# -------------------------

game_metadata = pd.DataFrame({
    "game": [
        "Genshin Impact",
        "Mobile Legends",
        "PUBG Mobile"
    ],
    "genre": [
        "RPG",
        "MOBA",
        "Battle Royale"
    ],
    "publisher": [
        "HoYoverse",
        "Moonton",
        "Krafton"
    ]
})


# -------------------------
# Load into PostgreSQL
# -------------------------

df.to_sql(
    "game_reviews",
    engine,
    if_exists="replace",
    index=False
)

game_metadata.to_sql(
    "game_metadata",
    engine,
    if_exists="replace",
    index=False
)

print(
    "\nData successfully cleaned and loaded "
    "into gaming_reviews_db."
)