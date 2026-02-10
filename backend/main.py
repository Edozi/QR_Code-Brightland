from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import SessionLocal
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://qrcodebrightlandscan.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VerifyRequest(BaseModel):
    ticket_id: str
    scanner_id: str

@app.post("/verify")
def verify_ticket(request: VerifyRequest):
    ticket_id = request.ticket_id
    scanner_id = request.scanner_id
    db = SessionLocal()

    query = text("""
        UPDATE tickets
        SET status = 'used',
            used_at = NOW(),
            scanner_id = :scanner_id
        WHERE id = :ticket_id
          AND status = 'valid'
        RETURNING id, used_at;
    """)

    result = db.execute(query, {
        "ticket_id": ticket_id,
        "scanner_id": scanner_id
    }).fetchone()

    db.commit()
    db.close()

    if result:
        return {
            "status": "valid",
            "used_at": result.used_at
        }
    else:
        # Check if ticket exists
        db = SessionLocal()
        exists = db.execute(
            text("SELECT status, used_at FROM tickets WHERE id = :id"),
            {"id": ticket_id}
        ).fetchone()
        db.close()

        if exists:
            return {
                "status": "used",
                "used_at": exists.used_at
            }
        else:
            raise HTTPException(status_code=404, detail="Invalid ticket")



if __name__ == "__main__":
    import uvicorn
    # import os
    # port = int(os.environ.get("PORT", 80)) ## Deploying to render
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)