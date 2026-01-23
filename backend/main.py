from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import get_settings
from backend.controllers.auth_controller import router as auth_router
from backend.controllers.userManagement_controller import (
    router as user_management_router,
)
from backend.controllers.registration_controller import(
    router as registration_router
)

settings = get_settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(user_management_router)
app.include_router(registration_router)
