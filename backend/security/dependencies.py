# app/security/dependencies.py
from fastapi import Depends, HTTPException, status
from backend.security.auth import get_current_user
from backend.security.permissions import user_permission_codes
from backend.model import Utente

def require_permission(code: str):
    def dep(user: Utente = Depends(get_current_user)) -> Utente:
        perms = user_permission_codes(user)
        if code not in perms:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return dep
