from __future__ import annotations

from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, TEXT
from backend.db.base import Base
from backend.model.links import materia_argomento


class Argomento(Base):
    __tablename__ = "argomento"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    descrizione: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    materie: Mapped[List["Materia"]] = relationship(
        "Materia",
        secondary=materia_argomento,
        back_populates="argomenti",
        lazy="selectin",
    )

    lezioni: Mapped[List["Lezione"]] = relationship("Lezione", back_populates="argomento", lazy="selectin")
