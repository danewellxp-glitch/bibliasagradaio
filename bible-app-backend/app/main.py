import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.bible import router as bible_router
from app.api.v1.profile import router as profile_router
from app.api.v1.quiz import router as quiz_router
from app.api.v1.study import router as study_router
from app.api.v1.user_content import router as user_content_router
from app.core.config import settings

# Firebase Admin SDK init (required for auth/login verify_id_token)
try:
    import firebase_admin
    from firebase_admin import credentials

    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    if os.path.isfile(cred_path):
        firebase_admin.initialize_app(credentials.Certificate(cred_path))
except Exception:
    pass  # Auth will fail until credentials are configured

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(bible_router, prefix="/api/v1")
app.include_router(study_router, prefix="/api/v1")
app.include_router(quiz_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(user_content_router, prefix="/api/v1")
