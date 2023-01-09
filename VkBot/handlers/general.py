from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import RegexRule
from vkbottle.framework.labeler import BotLabeler

from config import api

from Rules import TextPlusRegexpRule, ChatIdRule  # TODO ChatIdRule убрать при релизе
from messages.default_msg import PICTURE
from utils.base_utils import my_random, make_reward, get_photo, change_keyboard

general_labeler = BotLabeler()
general_labeler.vbml_ignore_case = True
general_labeler.auto_rules = [ChatIdRule(chat_id=1)]  # TODO убрать при релизе


@general_labeler.message(RegexRule(r".*@all.*"))
async def dailies_people(message: Message):
    minus_rat = my_random(11)
    await message.reply(f"[id{message.from_id}|Ты] норм? Я тебе сейчас allну по ебалу🤬 (-{minus_rat} рейтинга)")
    await make_reward(message.from_id, minus_rat)


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
