from datetime import datetime, date, timedelta
from typing import Optional

from config import moscow_zone
from db.connection import SessionManager
from db.models import Inventory, User
from db.utils.items import get_item, set_item, set_tags_docs, get_item_tag, update_tag_doc
from db.utils.users import get_user_by_user_id
from my_types import Items


async def get_item_sure(item_name: str, user_id: int, chat_id: int) -> Inventory:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user: User = await get_user_by_user_id(user_id, chat_id, session)
        item: Inventory = await get_item(item_name, user.row_id, session)
        if item is None:
            item = await set_item(
                item_name=item_name,
                user_row_id=user.row_id,
                get_date=datetime.now(tz=moscow_zone).date(),
                session=session
            )
    return item


async def create_new_msg_tag(user_id: int, chat_id: int, attachment: str, num_days: Optional[int] = None) -> None:
    exp_date: Optional[date] = None
    if num_days is not None:
        exp_date = datetime.now(tz=moscow_zone).date() + timedelta(days=num_days)
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user: User = await get_user_by_user_id(user_id, chat_id, session)

        item = await get_item(Items.tags.value, user.row_id, session)
        if item is not None:
            tag_doc = await get_item_tag(item.id, session)
            tag_doc.attachment_str = attachment
            await update_tag_doc(tag_doc, session)
            return

        item = await set_item(
            item_name=Items.tags.value,
            user_row_id=user.row_id,
            get_date=datetime.now(tz=moscow_zone).date(),
            exp_date=exp_date,
            session=session
        )
        await set_tags_docs(item.id, attachment, session)
    return
