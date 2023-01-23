from typing import Optional, Union

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ScalarResult

from db.connection import SessionManager
from db.models import User


async def get_user_by_id(row_id: int) -> Optional[User]:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        q = select(User).where(User.row_id == row_id)
        user: User = await session.scalar(q)
    return user


async def get_user_by_user_id(user_id: int, chat_id: int, session: AsyncSession) -> Optional[User]:
    q = select(User).where(User.user_id == user_id, User.chat_id == chat_id)
    user: User = await session.scalar(q)
    return user


async def get_all_users_from_chat(chat_id: int, session: AsyncSession,
                                  user_param: object = User.user_id) -> list[User]:
    q = select(User).where(User.chat_id == chat_id).order_by(user_param)
    users: ScalarResult = await session.scalars(q)
    return users.all()


async def get_active_users_from_chat(chat_id: int, session: AsyncSession,
                                     user_param: object = User.user_id, active: bool = True) -> list[User]:
    q = select(User).where(User.chat_id == chat_id, User.is_active == active).order_by(user_param)
    users: ScalarResult = await session.scalars(q)
    return users.all()


async def set_user(user_id: int, chat_id: int, firstname: str, lastname: str, session: AsyncSession) -> User:
    user = User(
        user_id=user_id,
        chat_id=chat_id,
        firstname=firstname,
        lastname=lastname
    )
    session.add(user)
    return user


async def update_user(user: User, session: Optional[AsyncSession] = None):
    if session is not None:
        session.add(user)
        await session.commit()
        return
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(user)
        await session.commit()
    return
