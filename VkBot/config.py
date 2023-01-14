import asyncio
import pytz

from vkbottle import API, BuiltinStateDispenser, Bot
from vkbottle.bot import BotLabeler
from vkbottle import CtxStorage

from environs import Env

from my_types import MultiRoulette


env = Env()
env.read_env("../.env")

api = API(env.str("TOKEN"))
user_api = API(env.str("USER_TOKEN"))
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

moscow_zone = pytz.timezone("Europe/Moscow")


ctx_storage = CtxStorage()
ctx_storage.set(
    "MultiRoulette",
    MultiRoulette(
        date_for_multi=None,
        users_award={}
    )
)
