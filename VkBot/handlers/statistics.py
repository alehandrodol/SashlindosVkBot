from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from Rules import ChatIdRule
from db.models import User
from utils import stats_utils
from messages import default_msg

stat_labeler = BotLabeler()
stat_labeler.vbml_ignore_case = True


@stat_labeler.message(text=default_msg.ALL_STATS)
async def all_stat(message: Message):
    user_param = User.user_id
    match message.text.lower():
        case "статистика":
            user_param = User.pdr_num
        case "пассивные":
            user_param = User.fucked
        case "рейтинги":
            user_param = User.rating
    reply_msg = await stats_utils.make_stat_message(message, user_param)
    await message.answer(reply_msg)
