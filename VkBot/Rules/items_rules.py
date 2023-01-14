import re
from typing import Union

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule


class CheckTagInsideRule(ABCRule[Message]):
    async def check(self, message: Message) -> Union[bool, dict]:
        if (user_id := re.search(r"\[id[0-9]*\|", message.text)) is not None:
            return {"user_id": int(user_id.group(0)[3:-1])}

