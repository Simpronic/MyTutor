# app/security/dependencies.py
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from backend.security.auth import get_current_user
from backend.security.permissions import user_permission_codes
from backend.model import Utente

def require_permission(code: str):
    def dep(
            user: Utente = Depends(get_current_user),
            active_role_id: Optional[int] = Header(default=None, alias="X-Active-Role-Id"),
        ) -> Utente:
            perms = user_permission_codes(user, active_role_id=active_role_id)
            if code not in perms:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
            return user
    return dep
