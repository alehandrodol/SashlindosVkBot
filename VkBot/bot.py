from vkbottle import Bot

from config import api, state_dispenser, labeler
from handlers import labelers


from utils.base_utils import startup_task, shutdown_task


for lab in labelers:
    labeler.load(lab)


bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)
bot.loop_wrapper.on_startup.append(startup_task())
bot.loop_wrapper.on_shutdown.append(shutdown_task())

if __name__ == "__main__":
    bot.run_forever()
