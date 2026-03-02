from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models import User
from app.services.user_service import create_user, get_user
from app.errors import PhoneAlreadyExistsError, EmailAlreadyExistsError, UserNotFoundError
from app.schemas import UserRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", tags=["users"], response_model=UserResponse)
async def create_new_user(user: UserRequest, session: Annotated[AsyncSession, Depends(get_db)]) -> User:
    try:
        result = await create_user(session, user)
    except (PhoneAlreadyExistsError, EmailAlreadyExistsError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(id: int, session: Annotated[AsyncSession, Depends(get_db)]) -> User:
    try:
        result = await get_user(session, id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
