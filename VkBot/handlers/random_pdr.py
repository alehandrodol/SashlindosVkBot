import asyncio

from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message
from vkbottle_types.codegen.objects import UsersUserFull, MessagesGetConversationMembers

from config import api, ctx_storage, moscow_zone

from db.connection import SessionManager
from db.utils.users import get_active_users_from_chat, update_user
from db.utils.items import update_item
from db.utils.chats import get_chat_by_id
from db.models import Chat, LaunchInfo, User

from utils import daily_utils, base_utils, items_utils

from messages import default_msg
from my_types import ChosenUser, MultiRoulette, Items
from Rules import ChatIdRule  # TODO убрать при релизе


daily_labeler = BotLabeler()
daily_labeler.vbml_ignore_case = True
daily_labeler.auto_rules = [ChatIdRule(chat_id=1)]  # TODO убрать при релизе


@daily_labeler.message(text=default_msg.DAILY)
async def dailies_people(message: Message):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chat: Chat = await get_chat_by_id(message.chat_id, session)
    if chat is None:
        await message.answer("Меня нужно сначала активировать🤡")
        return
    launch: LaunchInfo = await base_utils.get_launch_info_sure(message.chat_id)

    today = datetime.now(tz=moscow_zone).date()

    if not (launch.daily_launch_date is None or today > launch.daily_launch_date):  # Проверка, что сегодня уже выбирали
        today_pdr: UsersUserFull = (await api.users.get(chat.today_pdr))[0]
        today_pass: UsersUserFull = (await api.users.get(chat.today_pass))[0]
        await message.answer(f"Чё? С памятью проблемы?\n"
                             f"Сегодня пидор - {today_pdr.last_name} {today_pdr.first_name}\n"
                             f"А трахает он - {today_pass.last_name} {today_pass.first_name}")
        return

    if not launch.up_to_date_phrase:  # Проверка на то, что фраза дня сгенерирована
        launch = await daily_utils.set_day_phrase(launch)

    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        chat_users_db: list[User] = await get_active_users_from_chat(message.chat_id, session)

    # Проверка, что сообщение не совпадает с фразой дня и 50% на случайную неудачу
    if message.text.lower() != launch.day_phrase or base_utils.my_random(100) < 50:
        item_try = await items_utils.get_item_sure(Items.launch.value, message.from_id, message.chat_id)
        has_try = True if item_try.expired_date is not None and today < item_try.expired_date else False
        await message.reply(f"{message.text} - эта фраза не является кодом запуска сегодня или является? 🤡\n"
                            f"{'• Но за попытку получаешь +7' if not has_try else '• Балы даются только за первую попытку в день :)'}")
        if not has_try:
            await base_utils.make_reward(user_id=message.from_id, chat_id=message.chat_id, points=7)
            item_try.count = 1
            item_try.expired_date = today + timedelta(days=1)
            await update_item(item_try)
        return

    launch = await daily_utils.update_launch_info(message.from_id, message.chat_id, launch)
    addition_msg = f"О, а у тебя уже стрик из запусков: {launch.launch_streak} (кол-во дней)\n• За это ты получил +1😎"
    await message.reply(f"Хорош, сегодня [id{message.from_id}|Ты] угадал кодовую фразу!\n"
                        f"• И получил за это +25 очков\n"
                        f"{'' if launch.launch_streak == 1 else addition_msg}")

    launch_reward = 26 if launch.launch_streak > 1 else 25
    await base_utils.make_reward(user_id=message.from_id, chat_id=message.chat_id, points=25)
    await asyncio.sleep(1)

    if launch.year_launch_num is None or today.year > launch.year_launch_num:
        chosen_year: ChosenUser = await daily_utils.choose_year_guy(chat_users_db, chat, launch)
        chosen_year.user_record.pdr_of_the_year += 1
        await update_user(chosen_year.user_record)
        await base_utils.make_reward(user_id=chosen_year.user_record.user_id, chat_id=message.chat_id,
                                     points=chosen_year.reward)
        await message.answer(chosen_year.message)
        await asyncio.sleep(3)

    dailies = await daily_utils.choose_dailies(chat_users_db, chat, launch)
    daily_pdr: ChosenUser = dailies[0]
    daily_pass: ChosenUser = dailies[1]

    daily_pdr.user_record.pdr_num += 1
    await update_user(daily_pdr.user_record)

    daily_pass.user_record.fucked += 1
    await update_user(daily_pass.user_record)

    await base_utils.make_reward(user_id=daily_pdr.user_record.user_id, chat_id=message.chat_id,
                                 points=daily_pdr.reward)
    await base_utils.make_reward(user_id=daily_pass.user_record.user_id, chat_id=message.chat_id,
                                 points=daily_pass.reward)

    await message.answer(
        f'Пидор дня сегодня - [id{daily_pdr.user_record.user_id}|{daily_pdr.user_record.firstname} '
        f'{daily_pdr.user_record.lastname}]\n'
        f'{daily_pdr.message}\n'
        f'А трахает он - [id{daily_pass.user_record.user_id}|{daily_pass.user_record.firstname} '
        f'{daily_pass.user_record.lastname}]\n'
        f'{daily_pass.message}',
        attachment=f"photo-209871225_{(await base_utils.get_photo()).id}"
    )

    await daily_utils.update_chat(daily_pdr.user_record.user_id, daily_pass.user_record.user_id, chat)

    await asyncio.sleep(1)
    await message.answer(f'[id{daily_pdr.user_record.user_id}|{daily_pdr.user_record.firstname}] и '
                         f'[id{daily_pass.user_record.user_id}|{daily_pass.user_record.firstname}], '
                         f'вы можете сыграть в рулетку и умножить ваш полученный рейтинг полученный за номинацию.\n'
                         f'Если вы хотите попробовать, напишите "рулетка"🎰')

    multi_roulette: MultiRoulette = ctx_storage.get("MultiRoulette")
    multi_roulette.date_for_multi = today
    multi_roulette.users_award = {
        daily_pdr.user_record.user_id: daily_pdr.reward,
        daily_pass.user_record.user_id: daily_pass.reward
    }
    ctx_storage.set("MultiRoulette", multi_roulette)
