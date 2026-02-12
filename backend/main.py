from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import SessionLocal
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

app = FastAPI()

# jwt configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

security = HTTPBearer()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
##


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")


class LoginRequest(BaseModel):
    username: str
    password: str

## -- Login Endpoint --
@app.post("/login")
def login(data: LoginRequest):

    stored_username = os.getenv("ADMIN_USERNAME")
    stored_password_hash = os.getenv("ADMIN_PASSWORD_HASH")

    if data.username != stored_username:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(data.password, stored_password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    token = jwt.encode(
        {
            "scanner_id": data.username,
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://qrcodebrightlandvercel.vercel.app/"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

## -- Verification Function dependency --
def get_current_scanner(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        scanner_id = payload.get("scanner_id")

        if scanner_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return scanner_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

class VerifyRequest(BaseModel):
    ticket_id: str
    scanner_id: str

## -- Verify Endpoint --
@app.post("/verify")
def verify_ticket(request: VerifyRequest, scanner_id: str = Depends(get_current_scanner)):
    ticket_id = request.ticket_id
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



## -- Stats Endpoint --
@app.get("/stats")
def get_stats(scanner_id: str = Depends(get_current_scanner)):
    db = SessionLocal()

    total = db.execute(
        text("SELECT COUNT(*) FROM tickets")
    ).scalar()

    used = db.execute(
        text("SELECT COUNT(*) FROM tickets WHERE status = 'used'")
    ).scalar()

    db.close()

    return {
        "total": total,
        "used": used,
        "remaining": total - used
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)