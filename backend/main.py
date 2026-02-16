from fastapi import FastAPI
import logging
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import get_settings
from backend.db.base import ensure_schema,SessionLocal
from backend.controllers.auth_controller import router as auth_router
from contextlib import asynccontextmanager
from backend.controllers.userManagement_controller import (
    router as user_management_router,
)
from backend.controllers.registration_controller import(
    router as registration_router
)
from backend.controllers.lesson_controller import (
    router as lesson_router,
)
from backend.controllers.student_controller import (
    router as student_router,
)
from backend.services.bootstrap_service import bootstrap_from_file

logger = logging.getLogger(__name__)
settings = get_settings()



@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_schema()
    if settings.bootstrap_seed_enabled:
        with SessionLocal() as db:
            bootstrap_from_file(
                db,
                seed_file_path=settings.bootstrap_seed_file_path
            )
    else:
        logger.info("Bootstrap seed disabilitato (SEED_ON_STARTUP=false)")
    yield
    logger.info("Shutdown")


app = FastAPI(lifespan=lifespan)

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
app.include_router(lesson_router)
app.include_router(student_router)

@app.get("/swagger", include_in_schema=False)
def swagger_ui() -> object:
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
    )