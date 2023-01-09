from vkbottle import Bot
from config import api, state_dispenser, labeler
from handlers import labelers


for lab in labelers:
    labeler.load(lab)


bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

if __name__ == "__main__":
    bot.run_forever()
