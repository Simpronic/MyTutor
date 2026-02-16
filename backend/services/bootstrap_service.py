from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.model import Permesso, Ruolo, Utente, UtenteRuolo,Paese,Materia

from backend.security.password import hash_password

logger = logging.getLogger(__name__)


class BootstrapError(RuntimeError):
    """Errore di bootstrap dati iniziali."""

def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "on"}

def _build_user_password_hash(
    user_data: dict[str, Any],
    default_password_plain: str | None,
    existing_user: Utente | None,
) -> str:
    if user_data.get("password_hash"):
        return user_data["password_hash"]

    if user_data.get("password"):
        return hash_password(user_data["password"])

    if default_password_plain:
        return hash_password(default_password_plain)

    if existing_user is not None:
        return existing_user.password_hash

    raise BootstrapError(
        f"Password mancante per utente '{user_data['username']}'. "
        "Definisci password_hash/password nel JSON o DEFAULT_USER_PASSWORD in cfg."
    )

def _upsert_paesi(db:Session,payload: dict[str, Any]) -> None:
    for country in payload.get("paesi",[]):
        county_name = country['nome']
        county_data = db.scalar(select(Paese).where(Paese.nome == county_name))
        if(county_data is None):
            county_data = Paese(nome = county_name,
                                iso2 = country.get('iso2'))
            db.add(county_data)
        county_data.iso3 = country.get('iso3')
        county_data.iso_numeric = country.get('iso_numeric')


def _upsert_roles(db: Session,payload: dict[str, Any]) -> None:
    for role_data in payload.get("roles", []):
        role_name = role_data["name"]
        role = db.scalar(select(Ruolo).where(Ruolo.nome == role_name))
        if role is None:
            role = Ruolo(nome=role_name)
            db.add(role)
        role.descrizione = role_data.get("description")

def _upsert_permissions(db: Session,payload: dict[str, Any]) -> None:
    for permission_data in payload.get("permissions", []):
        permission_code = permission_data["code"]
        permission = db.scalar(select(Permesso).where(Permesso.codice == permission_code))
        if permission is None:
            permission = Permesso(codice=permission_code)
            db.add(permission)

        permission.descrizione = permission_data.get("description")

def _upsert_materie(db: Session,payload: dict[str, Any]) -> None:
    for subject in payload.get("paesi",[]):
        subject_name = subject['nome']
        subject_data = db.scalar(select(Materia).where(Materia.nome == subject_name))
        if(subject_data is None):
            subject_data = Materia(nome = subject_name)
            db.add(subject_data)
        subject_data.descrizione = subject.get('descrizione')

def _upsert_roles_permissions_association(db: Session,payload: dict[str, Any]) -> None:
    roles_by_name = {
        role.nome: role
        for role in db.scalars(select(Ruolo)).all()
    }
    permissions_by_code = {
        permission.codice: permission
        for permission in db.scalars(select(Permesso)).all()
    }

    for role_permissions in payload.get("role_permissions", []):
        role_name = role_permissions["role"]
        role = roles_by_name.get(role_name)
        if role is None:
            raise BootstrapError(f"Ruolo '{role_name}' non trovato per role_permissions.")

        requested_permissions = role_permissions.get("permissions", [])
        if "*" in requested_permissions:
            target_permissions = list(permissions_by_code.values())
        else:
            target_permissions = []
            for code in requested_permissions:
                permission = permissions_by_code.get(code)
                if permission is None:
                    raise BootstrapError(
                        f"Permesso '{code}' non trovato per ruolo '{role_name}'."
                    )
                target_permissions.append(permission)

        current_codes = {permission.codice for permission in role.permessi}
        for permission in target_permissions:
            if permission.codice not in current_codes:
                role.permessi.append(permission)

def _upsert_users(db: Session,payload: dict[str, Any],default_password_plain:str ='admin') -> None:
    roles_by_name = {
        role.nome: role
        for role in db.scalars(select(Ruolo)).all()
    }

    for user_data in payload.get("basic_users", []):
        username = user_data["username"]
        user = db.scalar(select(Utente).where(Utente.username == username))

        user_password_hash = _build_user_password_hash(user_data, default_password_plain, user)

        if user is None:
            user = Utente(
                username=username,
                email=user_data["email"],
                password_hash=user_password_hash,
                nome=user_data["name"],
                cognome=user_data["surname"],
                attivo=_to_bool(user_data.get("active", True)),
            )
            db.add(user)
        else:
            user.email = user_data["email"]
            user.password_hash = user_password_hash
            user.nome = user_data["name"]
            user.cognome = user_data["surname"]
            user.attivo = _to_bool(user_data.get("active", True))

        current_role_names = {link.ruolo.nome for link in user.ruoli_link}
        for role_name in user_data.get("roles", []):
            role = roles_by_name.get(role_name)
            if role is None:
                raise BootstrapError(
                    f"Ruolo '{role_name}' non trovato per utente '{username}'."
                )

            if role_name not in current_role_names:
                user.ruoli_link.append(UtenteRuolo(ruolo=role))
                current_role_names.add(role_name)


def load_seed_payload(seed_file_path: str) -> dict[str, Any] | None:
    seed_path = Path(seed_file_path)
    if not seed_path.exists():
        logger.info("Seed file non trovato, bootstrap saltato: %s", seed_file_path)
        return None

    with seed_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise BootstrapError("Il file seed JSON deve avere un oggetto come root.")

    return payload

def seed_base_data(
    db: Session,
    payload: dict[str, Any]
) -> None:
    try:
        _upsert_paesi(db,payload)
        _upsert_materie(db,payload)
        _upsert_roles(db, payload)
        _upsert_permissions(db, payload)
        db.flush()

        _upsert_roles_permissions_association(db, payload)
        _upsert_users(db, payload)
        db.commit()
    except Exception:
        db.rollback()
        raise

def bootstrap_from_file(
    db: Session,
    seed_file_path: str
) -> None:
    payload = load_seed_payload(seed_file_path)
    if payload is None:
        return

    logger.info("Avvio bootstrap dati base da %s", seed_file_path)
    seed_base_data(db, payload)
    logger.info("Bootstrap dati base completato")