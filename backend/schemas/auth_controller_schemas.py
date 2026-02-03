from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

class PaeseResponse(BaseModel):
    id: int
    nome: str
    iso2: str = Field(..., min_length=2, max_length=2)
    iso3: str | None = Field(None, min_length=3, max_length=3)
    iso_numeric: str | None = Field(None, min_length=3, max_length=3)

    class Config:
        from_attributes = True    # Pydantic v2


class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=1, max_length=254, description="Username oppure email")
    password: str = Field(..., min_length=1, max_length=255)


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    nome: str
    cognome: str
    attivo: bool

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    user: UserPublic
    session_token: str
    token_type: str = "bearer"

class RolePublic(BaseModel):
    id: int
    nome: str
    descrizione: str | None = None

    class Config:
        from_attributes = True

class UserRolesResponse(BaseModel):
    roles: List[RolePublic]

class UserPermission(BaseModel): 
    id: int 
    codice: str
    descrizione: str | None = None

    class Config:
        from_attributes = True


class UserPermissionResponse(BaseModel): 
    permissions: List[UserPermission]
