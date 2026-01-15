from __future__ import annotations

from datetime import datetime, time
from typing import Optional
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, TIME, VARCHAR, DATETIME

from backend.db.base import Base


class DisponibilitaTutor(Base):
    __tablename__ = "disponibilita_tutor"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    tutor_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)

    giorno_settimana: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)  # 1..7
    ora_inizio: Mapped[time] = mapped_column(TIME, nullable=False)
    ora_fine: Mapped[time] = mapped_column(TIME, nullable=False)
    timezone: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, server_default=text("'Europe/Rome'"))

    attiva: Mapped[bool] = mapped_column(TINYINT(1), nullable=False, server_default=text("1"))
    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    tutor: Mapped["Utente"] = relationship("Utente", back_populates="disponibilita")
