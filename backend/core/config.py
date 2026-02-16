from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CFG_PATH = BASE_DIR / "cfg" / "appconf.cfg"


def _cfg_bool(cfg: configparser.ConfigParser, section: str, option: str, fallback: bool) -> bool:
    raw = cfg.get(section, option, fallback=str(fallback))
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}

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
    bootstrap_seed_enabled: bool
    bootstrap_seed_file_path: str


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
        bootstrap_seed_enabled=_cfg_bool(cfg, "BOOTSTRAP", "SEED_ON_STARTUP", True),
        bootstrap_seed_file_path=cfg.get(
            "BOOTSTRAP",
            "SEED_FILE_PATH",
            fallback=str(BASE_DIR / "cfg" / "bootstrap_seed.json"),
        )
    )