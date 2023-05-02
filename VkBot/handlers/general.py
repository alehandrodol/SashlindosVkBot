from sqlalchemy import delete
from sqlalchemy.future import select
from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import RegexRule
from vkbottle.framework.labeler import BotLabeler

from Rules import TextPlusRegexpRule
from config import api
from db.connection import SessionManager
from db.models import User, Inventory, TagDoc
from db.utils.chats import get_chats_list
from db.utils.users import get_user_by_user_id, update_user, set_user
from messages.default_msg import PICTURE
from utils.base_utils import my_random, make_reward, get_photo, change_keyboard
from utils.items_utils import create_new_msg_tag

general_labeler = BotLabeler()
general_labeler.vbml_ignore_case = True


@general_labeler.message(RegexRule(r".*@all.*"))
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


@general_labeler.message(text="команды")
async def give_instructs(message: Message):
    await message.answer("Здесь можно посмотреть все команды", attachment="wall-209871225_36")


# @general_labeler.message(text="верни фишку Попу сука")
async def tags_ret(message: Message):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chats = await get_chats_list(session)
        pop = await get_user_by_user_id(146549595, chats[1].id, session)
        q_i = select(Inventory).where(Inventory.user_row_id == pop.row_id, Inventory.item_name == "item_tag")
        items = (await session.scalars(q_i)).all()
        for i in items:
            q = delete(TagDoc).where(TagDoc.inventory_id == i.id)
            await session.execute(q)
        q_i = delete(Inventory).where(Inventory.user_row_id == pop.row_id, Inventory.item_name == "item_tag")
        await session.execute(q_i)
    await create_new_msg_tag(user_id=146549595, chat_id=message.chat_id,
                             attachment="photo-209871225_457239337", num_days=180)
    await message.answer("Так, возможно вернул твою фишку, я уже не уверен...")


# @general_labeler.message(text="diagnos")
async def diag(message: Message):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chats = await get_chats_list(session)
        pop = await get_user_by_user_id(146549595, chats[1].id, session)
        await message.answer(f"row_id={pop.row_id}")
        q_i = select(Inventory).where(Inventory.user_row_id == pop.row_id, Inventory.item_name == "item_tag")
        items = (await session.scalars(q_i)).all()
        for i in items:
            await message.answer(f"id={i.id}, row_id={i.user_row_id}, item_name={i.item_name}")

