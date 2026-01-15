from __future__ import annotations

from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import SMALLINT, VARCHAR
from backend.db.base import Base
from backend.model.links import ruolo_permesso


class Permesso(Base):
    __tablename__ = "permesso"

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True, autoincrement=True)
    codice: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)
    descrizione: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)

    ruoli: Mapped[List["Ruolo"]] = relationship(
        "Ruolo",
        secondary=ruolo_permesso,
        back_populates="permessi",
        lazy="selectin",
    )
