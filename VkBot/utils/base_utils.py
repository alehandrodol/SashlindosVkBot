from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from vkbottle.bot import Message
from vkbottle_types.objects import PhotosPhoto

from config import user_api
from db.connection import SessionManager
from db.models import User, Chat
from db.utils import users
from db.utils.chats import get_chat_by_id, set_chat
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


async def get_chat_sure(message: Message) -> Chat:
    """
    Получение чата откуда отправлено сообщение, и если его не существует, то его создание
    :param message:
    :return: Chat
    """
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        if (chat := await get_chat_by_id(local_chat_id=message.chat_id, session=session)) is None:
            chat_name = await message.ctx_api.messages.get_conversations_by_id(message.peer_id)
            chat_name = chat_name.items[0].chat_settings.title
            chat = await set_chat(local_chat_id=message.chat_id, chat_name=chat_name, session=session)
        await session.commit()
    return chat


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


async def make_reward(user_id: int, points: int):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user: User = await users.get_user_by_id(user_id, session)
        user.rating += points
        session.add(user)
        await session.commit()

# def is_all_members_recorded(message: Message) -> bool:
#     group_info = await message.ctx_api.messages.get_conversations_by_id(message.peer_id)
#     count_mem = group_info.items[0].chat_settings.members_count
#     session_maker = SessionManager().get_session_maker()
#     async with session_maker() as session:
#         db_users = users.get_users_from_group(message.chat_id, session)
#     return db_users >= count_mem
