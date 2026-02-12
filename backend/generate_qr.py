import qrcode
from database import engine
from sqlalchemy import text
import os
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://qrcodebrightlandscan.vercel.app/scan/"
OUTPUT_DIR = "test_qr_codes"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with engine.connect() as conn:
    tickets = conn.execute(text("SELECT id, public_number FROM concert_tickets")).fetchall()

for ticket in tickets:
    ticket_id = str(ticket.id)
    public_number = ticket.public_number

    qr_url = BASE_URL + ticket_id

    qr = qrcode.make(qr_url)
    qr = qr.resize((400, 400))

    canvas = Image.new("RGB", (400, 500), "white")
    canvas.paste(qr, (0, 0))


    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((200, 450), public_number, fill="black", font=font, anchor="mm")

    canvas.save(f"{OUTPUT_DIR}/{public_number}.png")

print("QR codes generated.")
