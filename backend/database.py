from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Example: postgresql://user:password@localhost:5432/concert_db"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
