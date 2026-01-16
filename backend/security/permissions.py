# app/security/permissions.py
from typing import List, Optional, Set

from fastapi import HTTPException, status

from backend.model import Permesso, Ruolo, Utente


def _get_active_role(user: Utente, role_id: int) -> Ruolo:
    for role in user.ruoli:
        if role.id == role_id:
            return role
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Role not assigned to user",
    )


def user_permission_codes(user: Utente, active_role_id: Optional[int] = None) -> Set[str]:
    if active_role_id is None:
        return {p.codice for r in user.ruoli for p in r.permessi}
    role = _get_active_role(user, active_role_id)
    return {p.codice for p in role.permessi}


def user_permissions(user: Utente, active_role_id: Optional[int] = None) -> List[Permesso]:
    if active_role_id is None:
        permissions_by_id: dict[int, Permesso] = {}
        for role in user.ruoli:
            for permesso in role.permessi:
                permissions_by_id[permesso.id] = permesso
        return list(permissions_by_id.values())
    role = _get_active_role(user, active_role_id)
    return list(role.permessi)
