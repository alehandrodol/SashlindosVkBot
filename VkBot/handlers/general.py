from vkbottle.bot import Message
from vkbottle.dispatch.rules.base import RegexRule
from vkbottle.framework.labeler import BotLabeler
from vkbottle_types.objects import PhotosPhoto

from Rules import TextPlusRegexpRule, ChatIdRule  # TODO убрать при релизе
from messages.default_msg import PICTURE
from config import user_api
from utils.base_utils import my_random, make_reward

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
    size = (await user_api.photos.get_albums(owner_id="-209871225", album_ids="282103569")).items[0].size
    offset = my_random(size)
    photo: PhotosPhoto = (await user_api.photos.get(owner_id="-209871225", album_id="282103569", rev=True, count=1, offset=offset)).items[0]

    await message.answer(attachment=f"photo-209871225_{photo.id}")
