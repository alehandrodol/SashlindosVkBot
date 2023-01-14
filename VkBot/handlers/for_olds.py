from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from Rules import ChatIdRule, CheckTagInsideRule
from db.connection import SessionManager
from db.models import User, Inventory, TagPhoto
from db.utils import items, users

for_olds_labeler = BotLabeler()
for_olds_labeler.vbml_ignore_case = True
for_olds_labeler.auto_rules = [ChatIdRule(chat_id=1)]


@for_olds_labeler.message(CheckTagInsideRule())
async def tag_item(message: Message, user_id: int):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user_db: User = await users.get_user_by_user_id(user_id=user_id, chat_id=message.chat_id, session=session)
        item_db: Inventory = await items.get_item(item_name="photo_tag", user_row_id=user_db.id, session=session)
        photo_tag: TagPhoto = await items.get_photo_tag(item_id=item_db.id, session=session)
    await message.answer(f"[id{user_id}|{user_db.firstname}], выходи!", attachment=f"{photo_tag.attachment_str}")

