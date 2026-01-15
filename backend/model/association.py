# app/models/association.py
from sqlalchemy import Table, Column, ForeignKey, BigInteger, SmallInteger
from backend.db.base import Base

utente_ruolo = Table(
    "utente_ruolo",
    Base.metadata,
    Column("utente_id", BigInteger, ForeignKey("utente.id"), primary_key=True),
    Column("ruolo_id", SmallInteger, ForeignKey("ruolo.id"), primary_key=True),
)

organizzazione_utente = Table(
    "organizzazione_utente",
    Base.metadata,
    Column("organizzazione_id", BigInteger, ForeignKey("organizzazione.id"), primary_key=True),
    Column("utente_id", BigInteger, ForeignKey("utente.id"), primary_key=True),
)
