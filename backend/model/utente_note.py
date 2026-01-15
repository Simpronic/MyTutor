from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, TEXT

from backend.db.base import Base

NOTE_TIPO = ("pagamento", "profilo", "altro")


class UtenteNote(Base):
    __tablename__ = "utente_note"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    utente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)

    tipo: Mapped[str] = mapped_column(
        Enum(*NOTE_TIPO, name="utente_note_tipo"),
        nullable=False,
        server_default=text("'altro'"),
    )
    testo: Mapped[str] = mapped_column(TEXT, nullable=False)

    creato_da: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"))
    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    utente: Mapped["Utente"] = relationship("Utente", foreign_keys=[utente_id], back_populates="note")
    creatore: Mapped[Optional["Utente"]] = relationship("Utente", foreign_keys=[creato_da], back_populates="note_create")
