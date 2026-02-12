import uuid
from database import engine
from sqlalchemy import text

EVENT_CODE = "Concert-2026"

with engine.connect() as conn:
    for _ in range(50):

        result = conn.execute(
            text("""
                INSERT INTO concert_tickets (id)
                VALUES (:id)
                RETURNING sequence_id
            """),
            {"id": str(uuid.uuid4())}
        )

        sequence_id = result.scalar()

        public_number = f"{EVENT_CODE}-{sequence_id:05d}"


        conn.execute(
            text("""
                UPDATE concert_tickets
                SET public_number = :public_number
                WHERE sequence_id = :sequence_id
            """),
            {
                "public_number": public_number,
                "sequence_id": sequence_id
            }
        )

    conn.commit()
