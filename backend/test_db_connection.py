import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES;"))
            tables = [row[0] for row in result]
            print("Connection successful! Tables:", tables)
    except Exception as e:
        print("Connection failed:", str(e))

if __name__ == "__main__":
    test_connection()
