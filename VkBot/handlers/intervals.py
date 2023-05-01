from datetime import datetime

from config import bot, ctx_storage, moscow_zone, user_api


@bot.loop_wrapper.interval(hours=1)
async def posts_clearing():
    polls: list[dict] = ctx_storage.get("polls_clearing")
    if not polls:
        return
    time = datetime.now(tz=moscow_zone)
    counter = 0
    for poll in polls:
        if time < poll["expired_date"]:
            break
        await user_api.wall.delete(owner_id=-209871225, post_id=poll['post_id'])
        counter += 1
    ctx_storage.set("polls_clearing", polls[counter:])
