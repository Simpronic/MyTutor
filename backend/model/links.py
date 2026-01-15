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

materia_argomento = Table(
    "materia_argomento",
    Base.metadata,
    Column("materia_id", BIGINT(unsigned=True), ForeignKey("materia.id"), primary_key=True),
    Column("argomento_id", BIGINT(unsigned=True), ForeignKey("argomento.id"), primary_key=True),
)
