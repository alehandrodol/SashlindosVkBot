from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule

from Rules import ChatIdRule


chat_labeler = BotLabeler()
chat_labeler.vbml_ignore_case = True

chat_labeler.custom_rules["chat_id"] = ChatIdRule
chat_labeler.auto_rules = [ChatIdRule(chat_id=1)]


@chat_labeler.message(CommandRule("say", ["!", "/"], 1))
async def say_handler(message: Message, args: tuple[str]):
    await message.answer(f"Меня попросили сказать: {args[0]}")


@chat_labeler.message(text=("test", "test2"))
async def test_chat(message: Message):
    await message.answer(f"Я из тестовой беседы")

