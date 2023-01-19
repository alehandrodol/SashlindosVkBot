import re
from typing import Union
from datetime import datetime

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from config import moscow_zone

from db.connection import SessionManager
from db.models import Inventory, User
from db.utils import items, users


class CheckTagInsideRule(ABCRule[Message]):
    async def check(self, message: Message) -> Union[bool, dict]:
        if (user_id := re.search(r"\[id[0-9]*\|", message.text)) is not None:
            session_maker = SessionManager().get_session_maker()
            async with session_maker() as session:
                user_db: User = await users.get_user_by_user_id(user_id=int(user_id.group(0)[3:-1]),
                                                                chat_id=message.chat_id, session=session)
                item_db: Inventory = await items.get_item(item_name="item_tag", user_row_id=user_db.row_id, session=session)
                today = datetime.now(tz=moscow_zone).date()
                if item_db is None or item_db.expired_date < today:
                    return False
            return {"user": user_db, "item": item_db}

