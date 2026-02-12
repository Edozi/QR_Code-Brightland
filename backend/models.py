from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "concert_tickets"

    id = Column(UUID, primary_key=True)
    status = Column(String)
    used_at = Column(DateTime)
    scanner_id = Column(String)
