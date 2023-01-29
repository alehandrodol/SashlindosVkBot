from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import RegexRule
from vkbottle.framework.labeler import BotLabeler

from config import api

from db.connection import SessionManager
from db.models import User
from db.utils.users import get_user_by_user_id, update_user, set_user
from Rules import TextPlusRegexpRule, ChatIdRule
from messages.default_msg import PICTURE
from utils.base_utils import my_random, make_reward, get_photo, change_keyboard

general_labeler = BotLabeler()
general_labeler.vbml_ignore_case = True


@general_labeler.message(RegexRule(r".*@all.*"), ChatIdRule(chat_id=1))
async def dailies_people(message: Message):
    minus_rat = my_random(11)
    await message.reply(f"[id{message.from_id}|Ты] норм? Я тебе сейчас allну по ебалу🤬 (-{minus_rat} рейтинга)")
    await make_reward(user_id=message.from_id, chat_id=message.chat_id, points=minus_rat*-1)


@general_labeler.message(TextPlusRegexpRule(text=PICTURE, regexp_pat=r"^[oо]+[рp]+$"))
async def test_photo(message: Message):
    photo = await get_photo()
    await message.answer(attachment=f"photo-209871225_{photo.id}")


@general_labeler.message(text=("переведи", "gthtdtlb"))
async def translate(message: Message):
    if message.reply_message is not None:
        text = change_keyboard(message.reply_message.text)
        await message.reply(text)
    else:
        await message.reply("Нечего переводить")


@general_labeler.message(func=lambda message:
                         message.action is not None and
                         message.action.type.value == "chat_kick_user")
async def kick(message: Message):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user: User = await get_user_by_user_id(message.from_id, message.chat_id, session)

    user.is_active = False
    await update_user(user)
    await message.answer(f"О, чел вышел, записал")


@general_labeler.message(func=lambda message:
                         message.action is not None and
                         message.action.type.value == "chat_invite_user")
async def invite(message: Message):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user: User = await get_user_by_user_id(message.from_id, message.chat_id, session)

    if user is None:
        session_maker = SessionManager().get_session_maker()
        async with session_maker() as session:
            new_user = (await api.users.get(user_ids=message.from_id))[0]
            await set_user(
                user_id=new_user.id,
                chat_id=message.chat_id,
                firstname=new_user.first_name,
                lastname=new_user.last_name,
                session=session
            )
            await message.answer(f"О, новый чувак, добавил его в список!\n"
                                 f"Здорова [id{message.from_id}|{new_user.first_name}]!")
    else:
        user.is_active = True
        await update_user(user)
        await message.answer(f"О, чел вернулся, записал")
