from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_content import (
    AnnotationCreate,
    AnnotationResponse,
    BookmarkCreate,
    BookmarkResponse,
    HighlightCreate,
    HighlightResponse,
)
from app.services.user_content_service import UserContentService

router = APIRouter(tags=["user-content"])


# --- Highlights ---
@router.get("/highlights", response_model=list[HighlightResponse])
async def get_highlights(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserContentService(db).get_highlights(user.id)


@router.post("/highlights", response_model=HighlightResponse, status_code=201)
async def create_highlight(
    data: HighlightCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserContentService(db).create_highlight(user.id, data.model_dump())


@router.delete("/highlights/{highlight_id}", status_code=204)
async def delete_highlight(
    highlight_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not UserContentService(db).delete_highlight(user.id, highlight_id):
        raise HTTPException(status_code=404)


# --- Annotations ---
@router.get("/annotations", response_model=list[AnnotationResponse])
async def get_annotations(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserContentService(db).get_annotations(user.id)


@router.post("/annotations", response_model=AnnotationResponse, status_code=201)
async def create_annotation(
    data: AnnotationCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserContentService(db).create_annotation(user.id, data.model_dump())


@router.delete("/annotations/{annotation_id}", status_code=204)
async def delete_annotation(
    annotation_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not UserContentService(db).delete_annotation(user.id, annotation_id):
        raise HTTPException(status_code=404)


# --- Bookmarks ---
@router.get("/bookmarks", response_model=list[BookmarkResponse])
async def get_bookmarks(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserContentService(db).get_bookmarks(user.id)


@router.post("/bookmarks", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(
    data: BookmarkCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserContentService(db).create_bookmark(user.id, data.model_dump())


@router.delete("/bookmarks/{bookmark_id}", status_code=204)
async def delete_bookmark(
    bookmark_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not UserContentService(db).delete_bookmark(user.id, bookmark_id):
        raise HTTPException(status_code=404)
