from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from Rules import CheckTagInsideRule
from db.connection import SessionManager
from db.models import User, Inventory, TagDoc
from db.utils import items

items_labeler = BotLabeler()
items_labeler.vbml_ignore_case = True


@items_labeler.message(CheckTagInsideRule())
async def tag_item(message: Message, user: User, item: Inventory):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        photo_tag: TagDoc = await items.get_item_tag(item_id=item.id, session=session)
    await message.answer(f"[id{user.user_id}|{user.firstname}], выходи!", attachment=f"{photo_tag.attachment_str}")

