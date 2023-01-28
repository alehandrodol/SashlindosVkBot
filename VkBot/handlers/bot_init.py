import asyncio

from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from db.connection import SessionManager
from db.models import User
from db.utils.chats import get_chat_by_id, set_chat
from db.utils.users import get_all_users_from_chat
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
        chat_users_db: list[User] = await get_all_users_from_chat(message.chat_id, session)
        if len(chat_users_db) == 0:
            await daily_utils.fill_users(message)
    if message.chat_id == 1:
        await create_new_msg_tag(user_id=162889506, chat_id=message.chat_id,
                                 attachment="photo-209871225_457239207", num_days=180)
        await create_new_msg_tag(user_id=146549595, chat_id=message.chat_id,
                                 attachment="photo-209871225_282103569", num_days=180)
        await create_new_msg_tag(user_id=455752320, chat_id=message.chat_id,
                                 attachment="photo-209871225_457239239", num_days=180)
        await create_new_msg_tag(user_id=233035002, chat_id=message.chat_id,
                                 attachment="photo-209871225_457239080", num_days=180)
    await message.answer("3")
    await asyncio.sleep(1)
    await message.answer("2")
    await asyncio.sleep(1)
    await message.answer("1")
    await asyncio.sleep(1)
    await message.answer("@all Я родился👹")  # TODO при релизе выдать msg теги кому надо, и дописать сообщения
    await message.answer("Всех с Новым....\nБлять.. Опять опоздал...")
    await asyncio.sleep(3)
    await message.answer("Ну да похуй, я ваш подарок на НГ, всех с Новым Годом!🥳")
    await asyncio.sleep(1)
    await message.answer("Итак, к делу, Я слышал здесь обитают настоящие геюги, кажется я попал куда надо😈")
    await asyncio.sleep(1)
    await message.answer("И несколько из них прям не плохо так выделились😏")
    await message.answer("• Самый рейтинговый пидр прошлого года, барабанная дробь...")
    await asyncio.sleep(1)
    await message.answer("Кого я обманываю, все итак знают: [id162889506|Артур Кузнецов]")
    await asyncio.sleep(1)
    await message.answer("• Самый частый пидор дня: [id233035002|Павел Погожев aka Маслёнок], поздравляем🥳")
    await asyncio.sleep(1)
    await message.answer("• Главный пассив дня: и тут произошёл ньанс, их двое, поздравляем:\n"
                         "[id146549595|Андрей Поповец aka Поп aka Панда] и [id455752320|Макар Михалищин aka БигМак]")
    await message.answer("Попробуйте меня запустить, этот процесс ПОЧТИ не изменился ;)")

