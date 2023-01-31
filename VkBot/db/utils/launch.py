from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import LaunchInfo


async def get_launch_info_by_chat_id(chat_id: int, session: AsyncSession) -> Optional[LaunchInfo]:
    q = select(LaunchInfo).where(LaunchInfo.chat_id == chat_id)
    info: LaunchInfo = await session.scalar(q)
    return info


async def set_launch_info(chat_id: int, session: AsyncSession) -> Optional[LaunchInfo]:
    launch = LaunchInfo(
        chat_id=chat_id
    )
    session.add(launch)
    return launch
