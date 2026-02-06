from __future__ import annotations

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from backend.db.base import Base

ruolo_permesso = Table(
    "ruolo_permesso",
    Base.metadata,
    Column("ruolo_id", SMALLINT(unsigned=True), ForeignKey("ruolo.id"), primary_key=True),
    Column("permesso_id", SMALLINT(unsigned=True), ForeignKey("permesso.id"), primary_key=True),
)