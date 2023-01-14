from datetime import datetime

from config import moscow_zone

from db.connection import SessionManager
from db.models import Inventory, User
from db.utils.items import get_item, set_item
from db.utils.users import get_user_by_user_id


async def get_item_sure(item_name: str, user_id: int, chat_id: int) -> Inventory:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user: User = await get_user_by_user_id(user_id, chat_id, session)
        item: Inventory = await get_item(item_name, user.id, session)
        if item is None:
            item = await set_item(
                item_name=item_name,
                user_row_id=user.id,
                get_date=datetime.now(tz=moscow_zone).date(),
                session=session
            )
    return item
