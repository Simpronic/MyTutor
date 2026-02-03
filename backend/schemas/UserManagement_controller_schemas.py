from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime,date

class RuoloCreate(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    email: str = Field(..., min_length=1, max_length=254)
    nome: str = Field(..., min_length=1, max_length=100)
    cognome: str = Field(..., min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    cf: Optional[str] = Field(None, max_length=16)
    telefono: Optional[str] = Field(None, max_length=30)
    data_nascita: Optional[datetime] = None
    iban: Optional[str] = Field(None, max_length=34)
    citta: Optional[str] = Field(None, max_length=120)
    indirizzo: Optional[str] = Field(None, max_length=255)
    cap: Optional[str] = Field(None, max_length=10)
    paese: Optional[str] = Field(None, max_length=2)
    ruoli: List[RuoloCreate] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CreatedUserResponse(BaseModel):
    user: str


class RolesResponse(BaseModel):
    id: int
    nome: str
    descrizione: str

    class Config:
        from_attributes = True


class TutorSettingsUpdateRequest(BaseModel):
    email: str | None = Field(None, min_length=1, max_length=254)
    nome: str | None = Field(None, min_length=1, max_length=100)
    cognome: str | None = Field(None, min_length=1, max_length=100)
    cf: str | None = Field(None, min_length=16, max_length=16)
    telefono: str | None = Field(None, max_length=30)
    data_nascita: date | None = None
    iban: str | None = Field(None, max_length=34)
    citta: str | None = Field(None, max_length=120)
    indirizzo: str | None = Field(None, max_length=255)
    cap: str | None = Field(None, max_length=10)
    paese: str | None = Field(None, min_length=2, max_length=2)

class UserUpdateRequest(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=64)
    email: str | None = Field(None, min_length=1, max_length=254)
    nome: str | None = Field(None, min_length=1, max_length=100)
    cognome: str | None = Field(None, min_length=1, max_length=100)
    cf: str | None = Field(None, min_length=16, max_length=16)
    telefono: str | None = Field(None, max_length=30)
    data_nascita: date | None = None
    iban: str | None = Field(None, max_length=34)
    citta: str | None = Field(None, max_length=120)
    indirizzo: str | None = Field(None, max_length=255)
    cap: str | None = Field(None, max_length=10)
    paese: str | None = Field(None, min_length=2, max_length=2)
    ruoli: List[RuoloCreate] | None = None


class UpdateResponse(BaseModel):
    Result: int
    update_timestamp: datetime


class PasswordChange(BaseModel):
    new_password: str
    old_password: str


class UserFullResponse(BaseModel):
    id: int
    username: str
    email: str
    nome: str
    cognome: str
    cf: Optional[str] = None
    telefono: Optional[str] = None
    data_nascita: Optional[date] = None
    iban: Optional[str] = None
    citta: Optional[str] = None
    indirizzo: Optional[str] = None
    cap: Optional[str] = None
    paese: Optional[str] = None
    attivo: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    ruoli: List[RolesResponse] = []

    class Config:
        from_attributes = True

