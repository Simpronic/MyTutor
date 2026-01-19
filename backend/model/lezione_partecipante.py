from __future__ import annotations

from typing import Optional

from sqlalchemy import Enum, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, TEXT

from backend.db.base import Base

LEZIONE_PRESENZA = ("previsto", "presente", "assente", "no_show")


class LezionePartecipante(Base):
    __tablename__ = "lezione_partecipante"
    __table_args__ = (Index("idx_lp_studente", "studente_id"),)

    lezione_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("lezione.id"), primary_key=True)
    studente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("studente.id"), primary_key=True)

    presenza: Mapped[str] = mapped_column(
        Enum(*LEZIONE_PRESENZA, name="lezione_presenza"),
        nullable=False,
        server_default=text("'previsto'"),
    )
    note: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    lezione: Mapped["Lezione"] = relationship("Lezione", back_populates="partecipanti_link")
    studente: Mapped["Studente"] = relationship("Studente", back_populates="partecipazioni_link")