from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, VARCHAR, DECIMAL, CHAR, TEXT

from backend.db.base import Base

LEZIONE_STATO = ("prenotata", "confermata", "svolta", "annullata", "no_show")


class Lezione(Base):
    __tablename__ = "lezione"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    organizzazione_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("organizzazione.id"))
    sede_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("sede.id"))

    tutor_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)
    studente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)

    materia_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("materia.id"), nullable=False)
    argomento_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("argomento.id"))

    data_inizio: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    data_fine: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    timezone: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, server_default=text("'Europe/Rome'"))

    stato: Mapped[str] = mapped_column(
        Enum(*LEZIONE_STATO, name="lezione_stato"),
        nullable=False,
        server_default=text("'prenotata'"),
    )

    prezzo: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    valuta: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default=text("'EUR'"))

    note: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    note_private: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    # relazioni
    organizzazione: Mapped[Optional["Organizzazione"]] = relationship("Organizzazione", back_populates="lezioni")
    sede: Mapped[Optional["Sede"]] = relationship("Sede", back_populates="lezioni")

    tutor: Mapped["Utente"] = relationship("Utente", foreign_keys=[tutor_id], back_populates="lezioni_come_tutor")
    studente: Mapped["Utente"] = relationship("Utente", foreign_keys=[studente_id], back_populates="lezioni_come_studente")

    materia: Mapped["Materia"] = relationship("Materia", back_populates="lezioni")
    argomento: Mapped[Optional["Argomento"]] = relationship("Argomento", back_populates="lezioni")

    storia_stato: Mapped[List["LezioneStatoStoria"]] = relationship(
        "LezioneStatoStoria",
        back_populates="lezione",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    pagamenti: Mapped[List["Pagamento"]] = relationship("Pagamento", back_populates="lezione", lazy="selectin")
