from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR,TINYINT,CHAR,DATETIME
from backend.db.base import Base

class Paese(Base):
    __tablename__ = "paese"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    iso2: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    iso3: Mapped[str] = mapped_column(CHAR(3), nullable=True)
    iso_numeric: Mapped[str] = mapped_column(CHAR(3), nullable=True)
    attivo: Mapped[int] = mapped_column(TINYINT(1), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
