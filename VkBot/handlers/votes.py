import asyncio, json
from datetime import datetime, timedelta

from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from Rules import ChatIdRule
from Rules.votes_rules import VoteStartRule
from config import user_api, moscow_zone
from db.connection import SessionManager
from db.models import Votes
from db.utils import votes, users

votes_labeler = BotLabeler()
votes_labeler.vbml_ignore_case = True
votes_labeler.auto_rules = [ChatIdRule(chat_id=1)]


@votes_labeler.message(VoteStartRule())
async def start_vote(message: Message, target_ui: int, rep: int):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        l_u = await users.get_user_by_user_id(message.from_id, message.chat_id, session)
        t_u = await users.get_user_by_user_id(target_ui, message.chat_id, session)
        vote: Votes = await votes.set_vote(launched_ui=l_u.row_id, target_ui=t_u.row_id, rep=rep, session=session)

    await message.answer("Vote start")
    poll = await user_api.polls.create(
        question=f"{'+' if rep > 0 else ''}{str(rep)} рейтинга для {t_u.firstname} {t_u.lastname}",
        owner_id=-209871225,
        end_date=(datetime.now(tz=moscow_zone) + timedelta(seconds=30)).timestamp(),
        add_answers=json.dumps(['+', '-'])
    )
    await user_api.wall.post(
        owner_id=-209871225,
        from_group=1,
        attachments=f"poll-209871225_{poll.id}",
        mute_notifications=1
    )
    await message.answer(message="Голосование!", attachment=f"poll-209871225_{poll.id}")
    await end_vote(message)
    return


async def end_vote(message: Message):
    await asyncio.sleep(30)
    await message.answer("Vote end")
