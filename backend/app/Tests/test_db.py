from backend.app.database.connection import engine

try:
    with engine.connect() as connection:
        print("PostgreSQL connection successful!")
except Exception as e:
    print("Database connection failed:", e)