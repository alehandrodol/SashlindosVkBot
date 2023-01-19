from datetime import date
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import SessionManager
from db.models import Inventory, TagDoc


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


async def get_item_tag(item_id: int, session: AsyncSession) -> TagDoc:
    q = select(TagDoc).where(TagDoc.inventory_id == item_id)
    tag_photo: TagDoc = await session.scalar(q)
    return tag_photo


async def set_tags_docs(inventory_id: int, attachment: str, session: AsyncSession):
    tag_doc = TagDoc(
        inventory_id=inventory_id,
        attachment_str=attachment
    )
    session.add(tag_doc)
    await session.commit()
    return
