from typing import Optional

from my_types import Color
from my_types.objects import reds, blacks
from utils.base_utils import my_random


def roulette(color: Optional[Color] = None, number: Optional[int] = None, triple: Optional[int] = None) -> tuple[int, int]:
    rand_num = my_random(37)
    if color is not None:
        if rand_num in reds and color == Color.red or rand_num in blacks and color == Color.black:
            return rand_num, 2
    elif number is not None:
        if number == rand_num:
            return rand_num, 36
    elif triple is not None:
        if triple == 1 and (1 <= rand_num <= 12):
            return rand_num, 3
        if triple == 2 and (13 <= rand_num <= 24):
            return rand_num, 3
        if triple == 3 and (25 <= rand_num <= 36):
            return rand_num, 3
    return rand_num, 0
