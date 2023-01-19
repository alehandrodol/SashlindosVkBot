from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import date

from db.models import User


user_id = int
reward = int
active = bool

reds = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
blacks = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}


@dataclass
class ChosenUser:
    user_record: User
    reward: int = 0
    message: str = ""


@dataclass
class MultiRoulette:
    date_for_multi: Optional[date]
    users_award: dict[user_id, reward]


class Color(Enum):
    red = "красный"
    black = "чёрный"


class RouletteType(Enum):
    dummy = "dummy"
    color = "color"
    triple = "triple"
    number = "number"


class Items(Enum):
    launch = "launch_try"
    tags = "item_tag"
