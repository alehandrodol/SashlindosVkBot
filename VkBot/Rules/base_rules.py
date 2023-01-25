import re
import logging
from typing import Union, Iterable

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule


LOGGER = logging.getLogger(__name__)


class TextPlusRegexpRule(ABCRule[Message]):
    def __init__(self, text: str | Iterable[str], regexp_pat: str):
        self.regexp_pat = regexp_pat
        self.text = text

    async def check(self, message: Message) -> bool:
        if re.fullmatch(self.regexp_pat, message.text.lower()):
            return True
        if isinstance(self.text, str) and message.text.lower() == self.text:
            return True
        msgs = set(self.text)
        if message.text.lower() in msgs:
            return True
        return False


class ChatIdRule(ABCRule[Message]):  # TODO убрать все упоминания при релизе
    def __init__(self, chat_id: Union[list[int], int] = 1):
        self.chat_id = chat_id

    async def check(self, message: Message) -> bool:
        return message.chat_id == self.chat_id
