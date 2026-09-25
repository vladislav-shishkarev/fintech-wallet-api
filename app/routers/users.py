from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.errors import (
    EmailAlreadyExistsError,
    PhoneAlreadyExistsError,
    UserNotFoundError,
)
from app.models import User
from app.schemas import UserRequest, UserResponse
from app.services.user_service import create_user, get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    responses={
        409: {"description": "Phone or email is being used by another user already"}
    },
)
async def create_new_user(
    user: UserRequest, session: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """
    Create a new user.
    """
    try:
        result = await create_user(session, user)
    except (PhoneAlreadyExistsError, EmailAlreadyExistsError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result


@router.get(
    "/{id}",
    response_model=UserResponse,
    responses={404: {"description": "Required user is not found"}},
)
async def get_user_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """
    Return user by id.
    """
    try:
        result = await get_user(session, id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
