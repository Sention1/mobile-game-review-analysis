import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

db_password = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql://postgres:{db_password}@localhost:5432/gaming_reviews_db"
)


query = """
SELECT
    game,
    COUNT(*) AS review_count,
    AVG(rating) AS avg_rating
FROM game_reviews
GROUP BY game
ORDER BY review_count DESC;
"""

result = pd.read_sql(query, engine)

print(result)