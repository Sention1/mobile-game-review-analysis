import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

df = pd.read_csv('reviews_20250928_141614.csv')


def pick_english_text(row):
    if row['lang_detected'] == 'en':
        return row['review_text']
    elif pd.notna(row['translation_en']):
        return row['translation_en']
    else:
        return "no translation available"


df['english_review'] = df.apply(pick_english_text, axis=1)


def has_title(row):
    if pd.isna(row['title']):
        return False
    else:
        return True


df['has_title'] = df.apply(has_title, axis=1)


def rating_label(row):
    if row['rating'] >= 4:
        return 'positive'
    elif row['rating'] <= 2:
        return 'negative'
    else:
        return 'neutral'


df['rating_label'] = df.apply(rating_label, axis=1)


def review_length(row):
    return len(row['english_review'])


df['review_length'] = df.apply(review_length, axis=1)


def is_translated(row):
    if row['lang_detected'] != 'en':
        return True
    else:
        return False


df['is_translated'] = df.apply(is_translated, axis=1)


def country_group(row):
    if row['country'] == 'us':
        return 'us'
    else:
        return 'other'


df['country_group'] = df.apply(country_group, axis=1)


def sentiment_score(row):
    if row['rating'] >= 4:
        return 1
    elif row['rating'] <= 2:
        return -1
    else:
        return 0


df['sentiment_score'] = df.apply(sentiment_score, axis=1)


def is_short_review(row):
    if row['review_length'] < 50:
        return True
    else:
        return False


df['is_short_review'] = df.apply(is_short_review, axis=1)


def platform_label(row):
    if row['platform'] == 'google_play':
        return 'Play Store'
    else:
        return 'Other'


df['platform_label'] = df.apply(platform_label, axis=1)


def rating_and_length_flag(row):
    if row['rating'] <= 2 and row['review_length'] > 200:
        return 'long_negative'
    else:
        return 'other'


df['rating_and_length_flag'] = df.apply(rating_and_length_flag, axis=1)


def locale_match(row):
    if row['lang_detected'] == row['lang_ui']:
        return True
    else:
        return False


df['locale_match'] = df.apply(locale_match, axis=1)

df['is_long_negative'] = df['rating_and_length_flag'] == 'long_negative'

reviews_engine = create_engine(f"postgresql://postgres:{db_password}@localhost:5432/gaming_reviews_db")

df.to_sql('game_reviews', reviews_engine, if_exists='replace', index=False)

game_metadata = pd.DataFrame({
    'game': ['Genshin Impact', 'Mobile Legends', 'PUBG Mobile'],
    'genre': ['RPG', 'MOBA', 'Battle Royale'],
    'publisher': ['HoYoverse', 'Moonton', 'Krafton']
})

game_metadata.to_sql('game_metadata', reviews_engine, if_exists='replace', index=False)

print("Data cleaned and loaded into gaming_reviews_db (game_reviews + game_metadata)")