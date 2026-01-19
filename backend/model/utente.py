from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, DATE, TINYINT, SMALLINT

from backend.db.base import Base


class Utente(Base):
    __tablename__ = "utente"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(254), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    nome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    cognome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)

    cf: Mapped[Optional[str]] = mapped_column(VARCHAR(16), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(VARCHAR(30), nullable=True)
    data_nascita: Mapped[Optional[date]] = mapped_column(DATE, nullable=True)

    citta: Mapped[Optional[str]] = mapped_column(VARCHAR(120), nullable=True)
    indirizzo: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    cap: Mapped[Optional[str]] = mapped_column(VARCHAR(10), nullable=True)
    paese: Mapped[Optional[str]] = mapped_column(VARCHAR(2), nullable=True)

    attivo: Mapped[bool] = mapped_column(TINYINT(1), nullable=False, server_default=text("1"))
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DATETIME, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    # ---- LINK: utente_ruolo (association object) ----
    ruoli_link: Mapped[List["UtenteRuolo"]] = relationship(
        "UtenteRuolo",
        back_populates="utente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # se vuoi la lista diretta dei Ruoli senza passare dal link:
    ruoli: Mapped[List["Ruolo"]] = relationship(
        "Ruolo",
        secondary="utente_ruolo",
        viewonly=True,
        lazy="selectin",
    )

    # ---- LINK: tutor_materia (association object) ----
    tutor_materie_link: Mapped[List["TutorMateria"]] = relationship(
        "TutorMateria",
        back_populates="tutor",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # disponibilita_tutor (1-N)
    disponibilita: Mapped[List["DisponibilitaTutor"]] = relationship(
        "DisponibilitaTutor",
        back_populates="tutor",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # lezione: due FK verso utente
    lezioni_come_tutor: Mapped[List["Lezione"]] = relationship(
        "Lezione",
        foreign_keys="Lezione.tutor_id",
        back_populates="tutor",
        lazy="selectin",
    )
    studenti: Mapped[List["Studente"]] = relationship(
        "Studente",
        back_populates="tutor",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    pagamenti_come_tutor: Mapped[List["Pagamento"]] = relationship(
        "Pagamento",
        foreign_keys="Pagamento.tutor_id",
        back_populates="tutor",
        lazy="selectin",
    )

    # note
    note: Mapped[List["UtenteNote"]] = relationship(
        "UtenteNote",
        foreign_keys="UtenteNote.utente_id",
        back_populates="utente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    note_create: Mapped[List["UtenteNote"]] = relationship(
        "UtenteNote",
        foreign_keys="UtenteNote.creato_da",
        back_populates="creatore",
        lazy="selectin",
    )

    # audit cambi stato lezione (puoi mettere lazy="raise" se vuoi “safe by default”)
    cambi_stato_lezione: Mapped[List["LezioneStatoStoria"]] = relationship(
        "LezioneStatoStoria",
        foreign_keys="LezioneStatoStoria.cambiato_da",
        back_populates="cambiato_da_utente",
        lazy="selectin",
    )


class UtenteRuolo(Base):
    __tablename__ = "utente_ruolo"

    utente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), primary_key=True)
    ruolo_id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), ForeignKey("ruolo.id"), primary_key=True)
    assegnato_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    utente: Mapped["Utente"] = relationship("Utente", back_populates="ruoli_link")
    ruolo: Mapped["Ruolo"] = relationship("Ruolo", back_populates="utenti_link")