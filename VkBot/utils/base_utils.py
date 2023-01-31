from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from vkbottle_types.objects import PhotosPhoto

from config import user_api, api
from db.connection import SessionManager
from db.models import User, Chat
from db.utils import users
from db.utils.chats import get_chats_list
from db.utils.launch import get_launch_info_by_chat_id, set_launch_info


def change_keyboard(text):
    layout = dict(zip(map(ord, '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
                      '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''))

    return text.translate(layout)


async def get_photo() -> PhotosPhoto:
    size = (await user_api.photos.get_albums(owner_id="-209871225", album_ids="282103569")).items[0].size
    offset = my_random(size)
    photo: PhotosPhoto = \
        (await user_api.photos.get(
            owner_id="-209871225",
            album_id="282103569",
            rev=True,
            count=1,
            offset=offset
        )).items[0]
    return photo


async def get_launch_info_sure(chat_id: int):
    """
    Получение launch_info откуда отправлено сообщение по id чата, и если его не существует, то его создание
    :param chat_id:
    :return:
    """
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        if (launch := await get_launch_info_by_chat_id(chat_id=chat_id, session=session)) is None:
            launch = await set_launch_info(chat_id=chat_id, session=session)
        await session.commit()
    return launch


def my_random(right_border: int) -> int:
    return datetime.today().microsecond % right_border


async def make_reward(points: int, user_id: Optional[int] = None, user_row_id: Optional[int] = None,
                      chat_id: Optional[int] = None):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        if user_row_id is None:
            user: User = await users.get_user_by_user_id(user_id, chat_id, session)
        else:
            user: User = await users.get_user_by_id(user_row_id)
        user.rating += points
        session.add(user)
        await session.commit()


async def startup_task():
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chats = await get_chats_list(session)
        await refresh_user_list(chats, session)
        await session.commit()
    await spammer(chats, "Я проснулся и готов работать!")


async def shutdown_task():
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chats = await get_chats_list(session)
    await spammer(chats, "Я пошёл спать, работать не буду")


async def refresh_user_list(chats: list[Chat], session: AsyncSession):
    for chat in chats:
        users_list: list[User] = await users.get_all_users_from_chat(chat_id=chat.id, session=session)
        await full_users_check(users_list, chat.id, session)


async def full_users_check(users_list: list[User], chat_id: int, session: AsyncSession):
    users_dict = {user.user_id: user for user in users_list}
    real_members = (await api.messages.get_conversation_members(2000000000+chat_id)).profiles
    for member in real_members:
        if member.id in users_dict.keys():
            if not users_dict[member.id].is_active:
                users_dict[member.id].is_active = True
                await users.update_user(users_dict[member.id], session=session)
        else:
            await users.set_user(
                user_id=member.id,
                chat_id=chat_id,
                firstname=member.first_name,
                lastname=member.last_name,
                session=session,
                man_commit=True
            )
    real_ids = {mem.id for mem in real_members}
    for user in users_list:
        if user.user_id not in real_ids and user.is_active:
            user.is_active = False
            await users.update_user(user)
    return


async def spammer(chats: list[Chat], text: str):
    for chat in chats:
        await api.messages.send(chat_id=chat.id, random_id=my_random(1000_000), message=text)
