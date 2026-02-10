import qrcode
from database import engine
from sqlalchemy import text

BASE_URL = "https://yourdomain.com/scan/"

with engine.connect() as conn:
    tickets = conn.execute(text("SELECT id FROM tickets")).fetchall()

for t in tickets:
    img = qrcode.make(BASE_URL + str(t.id))
    img.save(f"qr_{t.id}.png")
