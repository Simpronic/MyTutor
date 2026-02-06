from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Index, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATE, DATETIME, TINYINT

from backend.db.base import Base


class Studente(Base):
    __tablename__ = "studente"
    __table_args__ = (
        Index("idx_studente_tutor", "tutor_id"),
        Index("idx_studente_cognome_nome", "cognome", "nome"),
        UniqueConstraint("tutor_id", "email", name="uq_studente_tutor_email"),
        UniqueConstraint("tutor_id", "cf", name="uq_studente_tutor_cf"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    tutor_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)

    nome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    cognome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)

    email: Mapped[Optional[str]] = mapped_column(VARCHAR(254), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(VARCHAR(30), nullable=True)
    cf: Mapped[Optional[str]] = mapped_column(VARCHAR(16), nullable=True)
    data_nascita: Mapped[Optional[date]] = mapped_column(DATE, nullable=True)

    citta: Mapped[Optional[str]] = mapped_column(VARCHAR(120), nullable=True)
    indirizzo: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    cap: Mapped[Optional[str]] = mapped_column(VARCHAR(10), nullable=True)
    paese: Mapped[Optional[str]] = mapped_column(VARCHAR(2), nullable=True)

    pagante_nome: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    pagante_cognome: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    pagante_cf: Mapped[Optional[str]] = mapped_column(VARCHAR(16), nullable=True)
    pagante_email: Mapped[Optional[str]] = mapped_column(VARCHAR(254), nullable=True)
    pagante_telefono: Mapped[Optional[str]] = mapped_column(VARCHAR(30), nullable=True)
    pagante_indirizzo: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)

    attivo: Mapped[bool] = mapped_column(TINYINT(1), nullable=False, server_default=text("1"))

    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    tutor: Mapped["Utente"] = relationship("Utente", back_populates="studenti")

    pagamenti: Mapped[List["Pagamento"]] = relationship(
        "Pagamento",
        back_populates="studente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    partecipazioni_link: Mapped[List["LezionePartecipante"]] = relationship(
        "LezionePartecipante",
        back_populates="studente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    lezioni: Mapped[List["Lezione"]] = relationship(
        "Lezione",
        secondary="lezione_partecipante",
        viewonly=True,
        lazy="selectin",
    )