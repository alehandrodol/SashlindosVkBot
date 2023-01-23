from vkbottle.bot import Message

from config import user_api

from utils.base_utils import make_reward

from db.models import Votes, User
from db.utils import votes, users

message_true = "Голосование завершено!\nРезультат положительный🥳\n• {first} {last} {g_or_l} {rep} рейтинга!!!"


async def vote_remind(message: Message):
    await message.answer("Напоминаю, идёт голосование, осталось 30 минут!")


async def end_vote(message: Message, poll_id: int, rep: str, vote: Votes):
    await votes.finish_vote(vote)
    poll = await user_api.polls.get_by_id(owner_id=-209871225, poll_id=poll_id)
    user: User = await users.get_user_by_id(vote.target_ui)
    if poll.answers[0].votes > poll.answers[1].votes:
        await make_reward(user_row_id=user.row_id, points=int(rep))
        await message.answer(message_true.format(
            first=user.firstname,
            last=user.lastname,
            g_or_l='получил' if poll.question[0] == "+" else 'потерял',
            rep=rep
        ))
    else:
        await message.answer("Голосование завершено!\nРезультат отрицательный🥲\n")
