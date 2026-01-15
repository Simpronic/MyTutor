# app/security/permissions.py
from typing import Set
from backend.model import Utente

def user_permission_codes(user: Utente) -> Set[str]:
    return {p.codice for r in user.ruoli for p in r.permessi}
