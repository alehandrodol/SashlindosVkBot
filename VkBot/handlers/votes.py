import asyncio
import json
from datetime import datetime, timedelta

from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from config import ctx_storage

from Rules import ChatIdRule
from Rules.votes_rules import VoteStartRule
from config import user_api, moscow_zone
from db.connection import SessionManager
from db.models import Votes
from db.utils import votes, users
from utils.votes_utils import end_vote, vote_remind

votes_labeler = BotLabeler()
votes_labeler.vbml_ignore_case = True


@votes_labeler.message(VoteStartRule())
async def start_vote(message: Message, target_ui: int, rep: int):
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        l_u = await users.get_user_by_user_id(message.from_id, message.chat_id, session)
        t_u = await users.get_user_by_user_id(target_ui, message.chat_id, session)
        vote: Votes = await votes.set_vote(launched_ui=l_u.row_id, target_ui=t_u.row_id, rep=rep, session=session)

    poll = await user_api.polls.create(
        question=f"{'+' if rep > 0 else ''}{str(rep)} рейтинга для {t_u.firstname} {t_u.lastname}",
        owner_id=-209871225,
        end_date=(datetime.now(tz=moscow_zone) + timedelta(hours=1)).timestamp(),
        add_answers=json.dumps(['+', '-']),
        background_id=1
    )
    post = await user_api.wall.post(
        owner_id=-209871225,
        from_group=1,
        attachments=f"poll-209871225_{poll.id}"
    )
    await message.answer(message="@all Началось голосование!", attachment=f"poll-209871225_{poll.id}")

    polls_list: list[dict[str, datetime | int]] = ctx_storage.get("polls_clearing")
    polls_list.append({"post_id": post.post_id, "expired_date": datetime.now(tz=moscow_zone) + timedelta(days=1)})

    await asyncio.sleep(1801)
    await vote_remind(message)

    await asyncio.sleep(1801)
    await end_vote(message, poll.id, str(rep), vote)
    return
