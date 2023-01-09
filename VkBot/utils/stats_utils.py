from typing import Union, Type

from vkbottle.bot import Message

from db.connection import SessionManager
from db.models import User
from db.utils import users


async def make_stat_message(message: Message, sort_type: object) -> str:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        users_list: list[User] = await users.get_users_from_chat(chat_id=message.chat_id, session=session,
                                                                 user_param=sort_type.desc())

    res_list_msg = []
    ind = 1
    for user in users_list:
        if sort_type == User.rating:
            if user.rating == 0:
                continue
            row = \
                f'{ind}. {user.firstname} {user.lastname} ' \
                f'имеет рейтинг пидора: {user.rating}'
        else:
            count_num = user.pdr_num if sort_type == User.pdr_num else user.fucked
            if count_num <= 0:
                continue
            row = \
                f'{ind}. {user.firstname} ' \
                f'{user.lastname} {"имел титул" if user.pdr_num else "зашёл не в ту дверь"}: {count_num} ' \
                f'{"раза" if count_num % 10 in [2, 3, 4] and count_num not in [12, 13, 14] else "раз"}'
        if user.id == message.from_id:
            row += " 🤡"
        res_list_msg.append(row)
        ind += 1
    return '\n'.join(res_list_msg)
