from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, TEXT

from backend.db.base import Base


class Sede(Base):
    __tablename__ = "sede"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    organizzazione_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("organizzazione.id"))

    nome: Mapped[Optional[str]] = mapped_column(VARCHAR(200), nullable=True)
    citta: Mapped[Optional[str]] = mapped_column(VARCHAR(120), nullable=True)
    cap: Mapped[Optional[str]] = mapped_column(VARCHAR(10), nullable=True)
    indirizzo: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    organizzazione: Mapped[Optional["Organizzazione"]] = relationship("Organizzazione", back_populates="sedi")
    lezioni: Mapped[List["Lezione"]] = relationship("Lezione", back_populates="sede", lazy="selectin")
