from pydantic import BaseModel, EmailStr, Field
from datetime import date

class RegistrationRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)
    nome: str = Field(..., min_length=1, max_length=100)
    cognome: str = Field(..., min_length=1, max_length=100)

    cf: str | None = Field(None, min_length=16, max_length=16)
    telefono: str | None = Field(None, max_length=30)
    data_nascita: date | None = None

    citta: str | None = Field(None, max_length=120)
    indirizzo: str | None = Field(None, max_length=255)
    cap: str | None = Field(None, max_length=10)
    paese: str | None = Field(None, min_length=2, max_length=2)

class RegistrationResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    ruolo: str

    class Config:
        from_attributes = True