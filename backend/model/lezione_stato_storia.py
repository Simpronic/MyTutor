from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, VARCHAR

from backend.db.base import Base
from backend.model.lezione import LEZIONE_STATO


class LezioneStatoStoria(Base):
    __tablename__ = "lezione_stato_storia"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    lezione_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("lezione.id"), nullable=False)

    da_stato: Mapped[Optional[str]] = mapped_column(Enum(*LEZIONE_STATO, name="lezione_stato"), nullable=True)
    a_stato: Mapped[str] = mapped_column(Enum(*LEZIONE_STATO, name="lezione_stato"), nullable=False)

    cambiato_da: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=True)
    cambiato_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    motivo: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)

    lezione: Mapped["Lezione"] = relationship("Lezione", back_populates="storia_stato")
    cambiato_da_utente: Mapped[Optional["Utente"]] = relationship(
        "Utente",
        foreign_keys=[cambiato_da],
        back_populates="cambi_stato_lezione",
    )
