from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.schemas import UserRequest
from app.enums import UserStatus
from app.models import User
from app.errors import UserNotFoundError, PhoneAlreadyExistsError, EmailAlreadyExistsError


async def create_user(session: AsyncSession, user_data: UserRequest) -> User:
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        status=UserStatus.ACTIVE
    )
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError as e:
        await session.rollback()
        error_msg = str(e.orig)
        if "users_email_key" in error_msg:
            raise EmailAlreadyExistsError(user_data.email)
        elif "users_phone_key" in error_msg:
            raise PhoneAlreadyExistsError(user_data.phone)
        raise e

    return new_user


async def get_user(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user