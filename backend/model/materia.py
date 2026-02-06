from __future__ import annotations

from typing import List, Optional
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, TEXT, DECIMAL, CHAR

from backend.db.base import Base


class Materia(Base):
    __tablename__ = "materia"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(VARCHAR(200), nullable=False, unique=True)
    descrizione: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)


    tutor_link: Mapped[List["TutorMateria"]] = relationship(
        "TutorMateria",
        back_populates="materia",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    lezioni: Mapped[List["Lezione"]] = relationship("Lezione", back_populates="materia", lazy="selectin")


class TutorMateria(Base):
    __tablename__ = "tutor_materia"

    tutor_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), primary_key=True)
    materia_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("materia.id"), primary_key=True)

    prezzo_orario: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    valuta: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default=text("'EUR'"))

    tutor: Mapped["Utente"] = relationship("Utente", back_populates="tutor_materie_link")
    materia: Mapped["Materia"] = relationship("Materia", back_populates="tutor_link")
