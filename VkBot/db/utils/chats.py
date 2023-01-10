from typing import Optional

from sqlalchemy.engine import ScalarResult
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Chat


async def get_chat_by_id(local_chat_id: int, session: AsyncSession) -> Optional[Chat]:
    q = select(Chat).where(Chat.id == local_chat_id)
    chat: Chat = await session.scalar(q)
    return chat


async def set_chat(local_chat_id: int, chat_name: str, session: AsyncSession) -> Optional[Chat]:
    chat = Chat(
        id=local_chat_id,
        name=chat_name
    )
    session.add(chat)
    return chat


async def get_chats_list(session: AsyncSession) -> list[Chat]:
    q = select(Chat)
    chats: ScalarResult = await session.scalars(q)
    return chats.all()
