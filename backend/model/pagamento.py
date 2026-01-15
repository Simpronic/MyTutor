from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, CHAR, VARCHAR, TEXT, DATETIME

from backend.db.base import Base

PAG_METODO = ("contanti", "bonifico", "carta", "paypal", "altro")
PAG_STATO = ("creato", "autorizzato", "pagato", "rimborsato", "fallito", "annullato")


class Pagamento(Base):
    __tablename__ = "pagamento"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    lezione_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("lezione.id"))
    studente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)
    tutor_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"))

    importo: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    valuta: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default=text("'EUR'"))

    metodo: Mapped[str] = mapped_column(Enum(*PAG_METODO, name="pag_metodo"), nullable=False, server_default=text("'altro'"))
    stato: Mapped[str] = mapped_column(Enum(*PAG_STATO, name="pag_stato"), nullable=False, server_default=text("'creato'"))

    riferimento_esterno: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    pagato_at: Mapped[Optional[datetime]] = mapped_column(DATETIME, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    lezione: Mapped[Optional["Lezione"]] = relationship("Lezione", back_populates="pagamenti")
    studente: Mapped["Utente"] = relationship("Utente", foreign_keys=[studente_id], back_populates="pagamenti_come_studente")
    tutor: Mapped[Optional["Utente"]] = relationship("Utente", foreign_keys=[tutor_id], back_populates="pagamenti_come_tutor")
