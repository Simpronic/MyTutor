from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RuoloCreate(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    email: str = Field(..., min_length=1, max_length=254)
    nome: str = Field(..., min_length=1, max_length=100)
    cognome: str = Field(..., min_length=1, max_length=100)
    cf: Optional[str] = Field(None, max_length=16)
    telefono: Optional[str] = Field(None, max_length=30)
    data_nascita: Optional[datetime] = None
    citta: Optional[str] = Field(None, max_length=120)
    indirizzo: Optional[str] = Field(None, max_length=255)
    cap: Optional[str] = Field(None, max_length=10)
    paese: Optional[str] = Field(None, max_length=2)
    ruoli: List[RuoloCreate] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CreatedUserResponse(BaseModel):
    user: str
    psw: str


class RolesResponse(BaseModel):
    id: int
    nome: str
    descrizione: str

    class Config:
        from_attributes = True