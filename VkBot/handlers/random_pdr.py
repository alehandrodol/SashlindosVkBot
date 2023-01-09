import asyncio

import pytz
from datetime import datetime

from vkbottle.bot import BotLabeler, Message
from vkbottle_types.codegen.objects import UsersUserFull

from config import api, ctx_storage

from db.connection import SessionManager
from db.utils.users import get_users_from_chat
from db.models import Chat, LaunchInfo, User

from utils import daily_utils
from utils import base_utils

from messages import default_msg
from my_types import ChosenUser, MultiRoulette
from Rules import ChatIdRule  # TODO убрать при релизе


daily_labeler = BotLabeler()
daily_labeler.vbml_ignore_case = True
daily_labeler.auto_rules = [ChatIdRule(chat_id=1)]  # TODO убрать при релизе


@daily_labeler.message(text=default_msg.DAILY)
async def dailies_people(message: Message):
    chat: Chat = await base_utils.get_chat_sure(message)
    launch: LaunchInfo = await base_utils.get_launch_info_sure(message.chat_id)

    moscow_zone = pytz.timezone("Europe/Moscow")
    today = datetime.now(tz=moscow_zone).date()

    if not (launch.daily_launch_date is None or today > launch.daily_launch_date):  # Проверка, что сегодня уже выбирали
        today_pdr: UsersUserFull = await api.users.get(chat.today_pdr)
        today_pass: UsersUserFull = await api.users.get(chat.today_pass)
        await message.answer(f"Чё? С памятью проблемы?\n"
                             f"Сегодня пидор - {today_pdr.last_name} {today_pdr.first_name}\n"
                             f"А трахает он - {today_pass.last_name_gen} {today_pass.first_name_gen}")
        return

    if not launch.up_to_date_phrase:  # Проверка на то, что фраза дня сгенерирована
        launch = await daily_utils.set_day_phrase(launch)

    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chat_users: list[User] = await get_users_from_chat(message.chat_id, session)
        if len(chat_users) == 0:
            await daily_utils.fill_users(message)
            chat_users = await get_users_from_chat(message.chat_id, session)

    # Проверка, что сообщение не совпадает с фразой дня и 33% на случайную неудачу
    if message.text != launch.day_phrase or base_utils.my_random(100) < 33:
        await message.reply(f"{message.text} - эта фраза не является кодом запуска сегодня или является? 🤡\n"
                            f"• Но за попытку получаешь +5")
        await base_utils.make_reward(message.from_id, 5)
        return

    await message.reply(f"Хорош, сегодня [id{message.from_id}|Ты] угадал кодовую фразу!\n"
                        f"• И получил за это +25 очков")
    await base_utils.make_reward(message.from_id, 25)
    await asyncio.sleep(1)

    await daily_utils.update_launch_info(message.from_id, launch)

    if launch.year_launch_num is None or today.year > launch.year_launch_num:
        chosen_year: ChosenUser = await daily_utils.choose_year_guy(chat_users, chat, launch)
        await base_utils.make_reward(chosen_year.user_record.id, chosen_year.reward)
        await message.answer(chosen_year.message)
        await asyncio.sleep(3)

    dailies = await daily_utils.choose_dailies(chat_users, chat, launch)
    daily_pdr: ChosenUser = dailies[0]
    daily_pass: ChosenUser = dailies[1]

    await base_utils.make_reward(daily_pdr.user_record.id, daily_pdr.reward)
    await base_utils.make_reward(daily_pass.user_record.id, daily_pass.reward)

    await message.answer(
        f'Пидор дня сегодня - [id{daily_pdr.user_record.id}|{daily_pdr.user_record.firstname} '
        f'{daily_pdr.user_record.lastname}]\n'
        f'{daily_pdr.message}\n'
        f'А трахает он - [id{daily_pass.user_record.id}|{daily_pass.user_record.firstname} '
        f'{daily_pass.user_record.lastname}]\n'
        f'{daily_pass.message}'
    )

    await daily_utils.update_chat(daily_pdr.user_record.id, daily_pass.user_record.id, chat)

    await asyncio.sleep(1)
    await message.answer(f'[id{daily_pdr.user_record.id}|{daily_pdr.user_record.firstname}] и '
                         f'[id{daily_pass.user_record.id}|{daily_pass.user_record.firstname}], '
                         f'вы можете сыграть в рулетку и умножить ваш полученный рейтинг полученный за номинацию.\n'
                         f'Если вы хотите попробовать, напишите "рулетка"🎰')

    multi_roulette: MultiRoulette = ctx_storage.get("MultiRoulette")
    multi_roulette.date_for_multi = today
    multi_roulette.users_award = {
        daily_pdr.user_record.id: daily_pdr.reward,
        daily_pass.user_record.id: daily_pass.reward
    }
    ctx_storage.set("MultiRoulette", multi_roulette)
