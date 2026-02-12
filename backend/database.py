from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres.hrgvqkjuipuwwyehzomz:2d3e4r23#ERs2@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"


if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Example: postgresql://user:password@localhost:5432/concert_db"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
