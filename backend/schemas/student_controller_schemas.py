from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class StudentCreateRequest(BaseModel):
    nome: str
    cognome: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    cf: Optional[str] = None
    data_nascita: Optional[date] = None
    citta: Optional[str] = None
    indirizzo: Optional[str] = None
    cap: Optional[str] = None
    paese: Optional[str] = None
    pagante_nome: Optional[str] = None
    pagante_cognome: Optional[str] = None
    pagante_cf: Optional[str] = None
    pagante_email: Optional[str] = None
    pagante_telefono: Optional[str] = None
    pagante_indirizzo: Optional[str] = None
    pagante_citta: Optional[str] = None
    pagante_cap: Optional[str] = None
    pagante_paese: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    tutor_id: int
    nome: str
    cognome: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    cf: Optional[str] = None
    data_nascita: Optional[date] = None
    attivo: bool
    citta: Optional[str] = None
    indirizzo: Optional[str] = None
    cap: Optional[str] = None
    paese: Optional[str] = None
    pagante_nome: Optional[str] = None
    pagante_cognome: Optional[str] = None
    pagante_cf: Optional[str] = None
    pagante_email: Optional[str] = None
    pagante_telefono: Optional[str] = None
    pagante_indirizzo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class StudentUpdateRequest(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    cf: Optional[str] = None
    data_nascita: Optional[date] = None
    citta: Optional[str] = None
    indirizzo: Optional[str] = None
    cap: Optional[str] = None
    paese: Optional[str] = None
    pagante_nome: Optional[str] = None
    pagante_cognome: Optional[str] = None
    pagante_cf: Optional[str] = None
    pagante_email: Optional[str] = None
    pagante_telefono: Optional[str] = None
    pagante_indirizzo: Optional[str] = None



class StudentUpdateResponse(BaseModel):
    Result: int
    update_timestamp: datetime