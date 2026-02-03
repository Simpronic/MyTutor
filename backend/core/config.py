from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CFG_PATH = BASE_DIR / "cfg" / "appconf.cfg"


def _load_cfg() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    if not CFG_PATH.exists():
        return cfg
    with CFG_PATH.open("r", encoding="utf-8-sig") as handle:
        cfg.read_file(handle)
    return cfg


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    session_duration_minutes: int
    cors_allow_origins: list[str]


def get_settings() -> Settings:
    cfg = _load_cfg()
    database_url = cfg.get("DATABASE", "DATABASE_URL", fallback=None)
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Add it to cfg/appconf.cfg."
        )
    return Settings(
        database_url=database_url,
        jwt_secret=cfg.get("SECURITY", "JWT_SECRET", fallback="CHANGE_ME"),
        jwt_algorithm=cfg.get("SECURITY", "JWT_ALGORITHM", fallback="HS256"),
        access_token_expire_minutes=int(
            cfg.get("SECURITY", "ACCESS_TOKEN_EXPIRE_MINUTES", fallback="60")
        ),
        refresh_token_expire_days=int(
            cfg.get("SECURITY", "REFRESH_TOKEN_EXPIRE_DAYS", fallback="14")
        ),
        session_duration_minutes=int(
            cfg.get("SECURITY", "SESSION_DURATION_MINUTES", fallback="120")
        ),
        cors_allow_origins=[
            item.strip()
            for item in cfg.get("CORS", "ALLOW_ORIGINS", fallback="*").split(",")
            if item.strip()
        ],
    )