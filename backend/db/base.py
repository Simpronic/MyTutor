from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import configparser 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR → backend/

CFG_PATH = BASE_DIR / "cfg" / "appconf.cfg"


cfg = configparser.ConfigParser()
with open(CFG_PATH, "r", encoding="utf-8-sig") as f:
    cfg.read_file(f)

engine = create_engine(cfg['DATABASE']['DATABASE_URL'], pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass