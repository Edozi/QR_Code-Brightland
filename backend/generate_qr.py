import qrcode
from database import engine
from sqlalchemy import text
import os

BASE_URL = "https://qrcodebrightlandscan.vercel.app/scan/"
OUTPUT_DIR = "test_qr_codes"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with engine.connect() as conn:
    tickets = conn.execute(text("SELECT id FROM tickets")).fetchall()

for ticket in tickets:
    ticket_id = str(ticket.id)
    qr_url = BASE_URL + ticket_id

    img = qrcode.make(qr_url)
    img.save(f"{OUTPUT_DIR}/qr_{ticket_id}.png")

print("QR codes generated.")
