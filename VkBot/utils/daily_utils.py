import logging
from datetime import datetime

from enum import Enum

import pytz
from vkbottle.bot import Message
from vkbottle_types.codegen.objects import UsersUserFull, MessagesGetConversationMembers

from db.connection import SessionManager
from db.utils.users import set_user
from db.models import Chat, LaunchInfo, User

from messages import default_msg

from my_types import ChosenUser

from utils.base_utils import my_random

logger = logging.getLogger(__name__)


class DailyStatus(Enum):
    pdr = "пидор"
    passive = "пассивный"


async def set_day_phrase(launch: LaunchInfo) -> LaunchInfo:
    launch.day_phrase = default_msg.DAILY[my_random(len(default_msg.DAILY))]
    launch.up_to_date_phrase = True

    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(launch)
        await session.commit()
    return launch


async def fill_users(message: Message):
    chat_users: MessagesGetConversationMembers = await message.ctx_api.messages. \
        get_conversation_members(message.peer_id)
    chat_users: list[UsersUserFull] = chat_users.profiles
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        for profile in chat_users:
            await set_user(
                user_id=profile.id,
                chat_id=message.chat_id,
                firstname=profile.first_name,
                lastname=profile.last_name,
                session=session
            )
        await session.commit()


async def calculate_daily_points(user_id: int, chat: Chat, launch: LaunchInfo, status: DailyStatus) -> tuple[int, str]:
    res_points = 0
    res_list_msg = []
    if status == DailyStatus.pdr:
        res_points += 100
        res_list_msg.append("• +100 за пидора дня")
    elif status == DailyStatus.passive:
        res_points += 50
        res_list_msg.append("• +50 за пассива дня")

    if launch.who_launched == user_id:
        res_points += 50
        res_list_msg.append("• +50 за запуск + попадание в номинацию дня")

    if chat.today_pdr == user_id and status == DailyStatus.pdr or \
            chat.today_pass == user_id and status == DailyStatus.passive:
        res_points += 50
        res_list_msg.append("• +50 за повторение своей позиции в прошлый день")

    if chat.today_pdr == user_id and status == DailyStatus.passive or \
            chat.today_pass == user_id and status == DailyStatus.pdr:
        res_points += 25
        res_list_msg.append("• +25 за повторное попадание в номинацию дня")

    if chat.year_pdr == user_id:
        res_points += 1
        res_list_msg.append("• +1 за пидора года 😎")

    if user_id == 221767748:
        res_points += 1
        res_list_msg.append("• +1 за то, что этот чел гений 👨🏻‍💻")

    return res_points, "\n".join(res_list_msg)


async def choose_dailies(chat_users: list[User], chat: Chat, launch: LaunchInfo) -> \
        tuple[ChosenUser, ChosenUser]:
    """
    Выбираем двух пользователей, которые будут являться пидором и пассивом дня соответсвено
    :param chat_users: список пользователей беседы
    :param chat: запись из таблицы chats о текущем чате
    :param launch: запись из таблицы launch_info привязанной к текущему чату
    :return: Возврщается кортеж с двуми кортежами, в каждом из которых лежит пользователь, его награда
    и сообщение для награждениея
    """

    pdr_ind = my_random(len(chat_users))
    daily_pdr: User = chat_users[pdr_ind]
    chat_users.pop(pdr_ind)
    daily_pass: User = chat_users[my_random(len(chat_users))]

    pdr_points, pdr_msg = await calculate_daily_points(daily_pdr.id, chat, launch, DailyStatus.pdr)
    pass_points, pass_msg = await calculate_daily_points(daily_pass.id, chat, launch, DailyStatus.passive)

    return ChosenUser(user_record=daily_pdr, reward=pdr_points, message=pdr_msg), \
        ChosenUser(user_record=daily_pass, reward=pass_points, message=pass_msg)


async def update_launch_info(who_launched_id: int, launch: LaunchInfo):
    moscow_zone = pytz.timezone("Europe/Moscow")
    today = datetime.now(tz=moscow_zone).date()

    launch.up_to_date_phrase = False
    launch.daily_launch_date = today
    if launch.who_launched == who_launched_id:
        launch.launch_streak += 1
    else:
        launch.launch_streak = 1

    launch.who_launched = who_launched_id

    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(launch)
        await session.commit()


async def update_chat(today_pdr: int, today_pass: int, chat: Chat):
    chat.today_pass = today_pass
    chat.today_pdr = today_pdr

    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(chat)
        await session.commit()


async def choose_year_guy(chat_users: list[User], chat: Chat, launch: LaunchInfo) -> ChosenUser:
    year_pdr = chat_users[my_random(len(chat_users))]
    year_pdr_message = f"Ого, наступил новый год, и я вычислил пидора этого года!\n" \
                       f"И пидором этого будет - [id{year_pdr.id}|{year_pdr.firstname} {year_pdr.lastname}]\n" \
                       f"• и за это он получает +1000 рейтинга!!!"
    chat.year_pdr = year_pdr.id
    moscow_zone = pytz.timezone("Europe/Moscow")
    launch.year_launch_num = datetime.now(tz=moscow_zone).date().year
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        session.add(chat)
        session.add(launch)
        await session.commit()
    return ChosenUser(user_record=year_pdr, reward=1000, message=year_pdr_message)
