from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, TEXT, TINYINT

from backend.db.base import Base


class Organizzazione(Base):
    __tablename__ = "organizzazione"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    piva: Mapped[Optional[str]] = mapped_column(VARCHAR(20), nullable=True, unique=True)
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(254), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(VARCHAR(30), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    sedi: Mapped[List["Sede"]] = relationship(
        "Sede",
        back_populates="organizzazione",
        lazy="selectin",
    )

    utenti_link: Mapped[List["OrganizzazioneUtente"]] = relationship(
        "OrganizzazioneUtente",
        back_populates="organizzazione",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    utenti: Mapped[List["Utente"]] = relationship(
        "Utente",
        secondary="organizzazione_utente",
        viewonly=True,
        lazy="selectin",
    )

    lezioni: Mapped[List["Lezione"]] = relationship(
        "Lezione",
        back_populates="organizzazione",
        lazy="selectin",
    )


class OrganizzazioneUtente(Base):
    __tablename__ = "organizzazione_utente"

    organizzazione_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), ForeignKey("organizzazione.id"), primary_key=True
    )
    utente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), primary_key=True)

    ruolo_in_org: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    attivo: Mapped[bool] = mapped_column(TINYINT(1), nullable=False, server_default=text("1"))
    associato_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    organizzazione: Mapped["Organizzazione"] = relationship("Organizzazione", back_populates="utenti_link")
    utente: Mapped["Utente"] = relationship("Utente", back_populates="organizzazioni_link")
