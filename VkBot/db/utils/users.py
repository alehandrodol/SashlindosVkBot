from typing import Optional, Union

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ScalarResult

from db.connection import SessionManager
from db.models import User


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    q = select(User).where(User.id == user_id)
    user: User = await session.scalar(q)
    return user


async def get_users_from_chat(chat_id: int, session: AsyncSession,
                              user_param: object = User.id) -> list[User]:
    q = select(User).where(User.chat_id == chat_id).order_by(user_param)
    users: ScalarResult = await session.scalars(q)
    return users.all()


async def set_user(user_id: int, chat_id: int, firstname: str, lastname: str, session: AsyncSession) -> User:
    user = User(
        id=user_id,
        chat_id=chat_id,
        firstname=firstname,
        lastname=lastname
    )
    session.add(user)
    return user


async def update_user(user: User) -> User:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(user)
        await session.commit()
    return user

