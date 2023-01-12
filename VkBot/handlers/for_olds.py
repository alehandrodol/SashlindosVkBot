from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from Rules import ChatIdRule

for_olds_labeler = BotLabeler()
for_olds_labeler.vbml_ignore_case = True
for_olds_labeler.auto_rules = [ChatIdRule(chat_id=1)]


@for_olds_labeler.message(func=lambda message: message.from_id == 162889506)
async def main_old(message: Message):
    return
