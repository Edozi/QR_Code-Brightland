import uuid
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    for _ in range(10):
        conn.execute(
            text("INSERT INTO tickets (id) VALUES (:id)"),
            {"id": str(uuid.uuid4())}
        )
    conn.commit()
