import asyncio

from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import VBMLRule

from config import ctx_storage

from Rules import RouletteRule, ChooseRoulette, ChatIdRule
from my_types import Color, RouletteType, MultiRoulette
from my_types.objects import reds, blacks
from utils import games, base_utils


games_labeler = BotLabeler()
games_labeler.vbml_ignore_case = True
games_labeler.auto_rules = [ChatIdRule(chat_id=1)]


@games_labeler.message(VBMLRule("рулетка"), RouletteRule())
async def roulette_handler(message: Message):
    await message.answer(f'О, я вижу [id{message.from_id}|ты] рисковый парень😈\n'
                         f'Генератор выберет одно случайное число от 0 до 37 из классической рулетки\n'
                         f'У тебя есть три опции:\n'
                         f'• Умножить в два раза, выбрать красное🔴 или чёрное ⚫ (для этого напиши "цвет: <красный/чёрный>")\n'
                         f'• Умножить в три раза, выбрать одну из 3-ёх третей (для этого напиши "треть: <число от 1 до 3>")\n'
                         f'• Умножить в 36 раз, угадать число от 0 до 36 (для этого напиши "число: <число от 0 до 36>")')


@games_labeler.message(ChooseRoulette(), RouletteRule())
async def start_roulette(message: Message, args: tuple[RouletteType, str]):
    number = -1
    match args[0]:
        case RouletteType.color:
            color = Color.red if args[1] == Color.red.value else Color.black
            number, result = games.roulette(color=color)
        case RouletteType.triple:
            number, result = games.roulette(triple=int(args[1]))
        case RouletteType.number:
            number, result = games.roulette(number=int(args[1]))
        case _:
            await message.answer(f"Произошло что-то странное [id221767748|разберись],"
                                 f"[id{message.from_id}|твой] рейтинг должен остаться прежним")
            result = 1

    smile = "🟢"
    if number in reds:
        smile = "🔴"
    elif number in blacks:
        smile = "⚫"
    await message.answer(f"Выпало число: {number}{smile}")

    multi_roulette: MultiRoulette = ctx_storage.get("MultiRoulette")
    reward: int = multi_roulette.users_award[message.from_id]
    await asyncio.sleep(1)
    if result == 0:
        await message.answer(f"Ууупс, [id{message.from_id}|тебе] не повезло, мне придётся вычесть у тебя "
                             f"полученный сегодня рейтинг ({reward})")
    if result == 2 or result == 3:
        await message.answer(f"А ты хорош!\nТы умножил сегодняшний приз в {result} раза🥳\n"
                             f"И получил сверху {reward * (result-1)}")
    if result == 36:
        await message.answer(f"Ебать😱, я не верю своим глазам, я не думал, что этот день когда-либо наступит...\n"
                             f"Но ты сделал это, ты умножил сегодняшний приз в 36 раз"
                             f"И получил сверху {reward * (result-1)}")
    await base_utils.make_reward(user_id=message.from_id, chat_id=message.chat_id, points=reward * (result-1))
    multi_roulette.users_award.pop(message.from_id)
    ctx_storage.set("MultiRoulette", multi_roulette)
