from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from db.connection import SessionManager
from db.models import User
from db.utils.chats import get_chat_by_id, set_chat
from db.utils.users import get_active_users_from_chat
from utils import daily_utils
from utils.items_utils import create_new_msg_tag
from Rules import ChatIdRule

init_labeler = BotLabeler()
init_labeler.vbml_ignore_case = True
init_labeler.auto_rules = [ChatIdRule(chat_id=1)]


@init_labeler.message(text="Погнали нахуй!")
async def init_bot(message: Message):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        if (chat := await get_chat_by_id(local_chat_id=message.chat_id, session=session)) is None:
            chat_name = await message.ctx_api.messages.get_conversations_by_id(message.peer_id)
            chat_name = chat_name.items[0].chat_settings.title
            chat = await set_chat(local_chat_id=message.chat_id, chat_name=chat_name, session=session)
        else:
            await message.answer("Я уже активирован, чего надо?")
            return
        chat_users_db: list[User] = await get_active_users_from_chat(message.chat_id, session)
        if len(chat_users_db) == 0:
            await daily_utils.fill_users(message)
    await create_new_msg_tag(user_id=221767748, chat_id=message.chat_id,
                             attachment="photo-209871225_457239323", num_days=90)
    await message.answer("all Я родился🥳")  # TODO поставить @ при релизе и выдать msg теги кому надо, и дописать сообщения
    await message.answer("Я слышал здесь обитают настоящие геюги, кажется я попал куда надо😈")

