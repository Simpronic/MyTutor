from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey,UniqueConstraint, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base


class Sessione(Base):
    __tablename__ = "sessione"
    __table_args__ = (UniqueConstraint("utente_id", name="uq_sessione_utente_id"),)

    token: Mapped[str] = mapped_column(VARCHAR(128), primary_key=True)
    utente_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("utente.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_seen_at: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False)

    utente: Mapped["Utente"] = relationship("Utente", lazy="joined")