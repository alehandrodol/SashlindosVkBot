from datetime import date
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import SessionManager
from db.models import Inventory, TagPhoto


async def get_item(item_name: str, user_row_id: int, session: AsyncSession) -> Optional[Inventory]:
    q = select(Inventory).where(Inventory.user_row_id == user_row_id, Inventory.item_name == item_name)
    item: Inventory = await session.scalar(q)
    return item


async def set_item(item_name: str, user_row_id: int,
                   get_date: date, session: AsyncSession, count: int = 0, exp_date: Optional[date] = None) -> Inventory:
    item = Inventory(
        item_name=item_name,
        user_row_id=user_row_id,
        count=count,
        get_date=get_date,
        expired_date=exp_date
    )
    session.add(item)
    await session.commit()
    return item


async def update_item(item: Inventory) -> None:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(item)
        await session.commit()
    return


async def get_photo_tag(item_id: int, session: AsyncSession) -> TagPhoto:
    q = select(TagPhoto).where(TagPhoto.inventory_id == item_id)
    tag_photo: TagPhoto = await session.scalar(q)
    return tag_photo
