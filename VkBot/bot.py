from config import bot, dummy_bot
from handlers import labelers

from handlers import posts_clearing
from utils.base_utils import startup_task, shutdown_task

bot.loop_wrapper.on_startup.append(startup_task())
bot.loop_wrapper.on_shutdown.append(shutdown_task())

bot.loop_wrapper.add_task(posts_clearing)

for lab in labelers:
    bot.labeler.load(lab)


if __name__ == "__main__":
    bot.run_forever()
