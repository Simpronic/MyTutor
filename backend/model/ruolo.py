from __future__ import annotations

from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import SMALLINT, VARCHAR
from backend.db.base import Base
from backend.model.links import ruolo_permesso


class Ruolo(Base):
    __tablename__ = "ruolo"

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)
    descrizione: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)

    # M2M con Permesso (ruolo_permesso)
    permessi: Mapped[List["Permesso"]] = relationship(
        "Permesso",
        secondary=ruolo_permesso,
        back_populates="ruoli",
        lazy="selectin",
    )

    # Association object con UtenteRuolo
    utenti_link: Mapped[List["UtenteRuolo"]] = relationship(
        "UtenteRuolo",
        back_populates="ruolo",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
