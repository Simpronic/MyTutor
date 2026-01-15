# app/models/association.py
from sqlalchemy import Table, Column, ForeignKey, BigInteger, SmallInteger
from backend.db.base import Base

utente_ruolo = Table(
    "utente_ruolo",
    Base.metadata,
    Column("utente_id", BigInteger, ForeignKey("utente.id"), primary_key=True),
    Column("ruolo_id", SmallInteger, ForeignKey("ruolo.id"), primary_key=True),
)