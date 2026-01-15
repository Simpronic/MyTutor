from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.controllers.auth_controller import router as auth_router
from backend.controllers.UserManagement_controller import (
    router as user_management_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(user_management_router)
