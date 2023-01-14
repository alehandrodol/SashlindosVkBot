from datetime import datetime

from typing import Union

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from config import ctx_storage, moscow_zone

from my_types import MultiRoulette, RouletteType


class RouletteRule(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        multi_roulette: MultiRoulette = ctx_storage.get("MultiRoulette")
        if multi_roulette.date_for_multi is None:
            return False

        if message.from_id not in multi_roulette.users_award.keys():
            print(multi_roulette.users_award.keys())
            await message.answer("Вы сегодня не состоите в номинации или уже использовали😬")
            return False

        today = datetime.now(tz=moscow_zone).date()

        if today != multi_roulette.date_for_multi:
            await message.answer("Ваше время на рулетку уже закончилось😬")
            return False

        return True


class ChooseRoulette(ABCRule[Message]):
    async def check(self, message: Message) -> Union[dict, bool]:
        splited_msg = message.text.split()
        try:
            command = splited_msg[0]
        except IndexError:
            return False
        if command.lower() not in {"цвет:", "треть:", "число:"}:
            return False
        if len(splited_msg) != 2:
            await message.reply("Некорректное кол-во аргументов")
            return False
        r_type: RouletteType = RouletteType.dummy
        if command.lower() == "цвет:":
            r_type = RouletteType.color
            if splited_msg[1] not in {"красный", "чёрный"}:
                await message.reply("Некорректный цвет")
                return False
        elif command.lower() == "треть:":
            r_type = RouletteType.triple
            if not splited_msg[1].isdigit() or (not (1 <= int(splited_msg[1]) <= 3)):
                await message.answer("Для данного режима нужно выбрать число от 1 до 3")
                return False
        elif command.lower() == "число:":
            r_type = RouletteType.number
            if not splited_msg[1].isdigit() or (not (0 <= int(splited_msg[1]) <= 36)):
                await message.answer("Для данного режима нужно выбрать число от 0 до 36")
                return False
        return {"args": (r_type, splited_msg[1])}
