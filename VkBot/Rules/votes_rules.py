import re
from typing import Union

from vkbottle import ABCRule
from vkbottle.bot import Message

from db.connection import SessionManager
from db.utils import votes, users


class VoteStartRule(ABCRule[Message]):
    async def check(self, message: Message) -> Union[dict, bool]:
        words = message.text.split()
        if len(words) != 3:
            return False
        if words[0] not in {"+rep", "-rep"}:
            return False
        if (target_ui := re.search(r"\[id[0-9]*\|", words[1])) is None:
            await message.answer("Второе слово должно быть тегом для кого голосование")
            return False
        if (not words[2].isdigit()) or (not 1 <= (rep := int(words[2])) <= 100):
            await message.answer("Кол-во рейтинги должно быть от 1 до 100")
            return False

        target_ui = int(target_ui.group(0)[3:-1])
        session_maker = SessionManager().get_session_maker()
        async with session_maker() as session:
            l_user = await users.get_user_by_user_id(message.from_id, message.chat_id, session)
            if len((await votes.get_vote_by_launched_ui(l_user.row_id, session))) >= 2:
                await message.answer("Вы сегодня больше не можете запускать голосование")
                return False

            t_user = await users.get_user_by_user_id(target_ui, message.chat_id, session)
            if len((await votes.get_vote_by_target_ui(t_user.row_id, session))) >= 2:
                await message.answer("Для этого пользователя сегодня больше нельзя запускать голосование")
                return False

        if words[0][0] == "-":
            rep *= -1

        return {"target_ui": target_ui, "rep": rep}
