from .test import chat_labeler
from .random_pdr import daily_labeler
from .games import games_labeler
from .general import general_labeler


labelers = (daily_labeler, general_labeler, games_labeler, chat_labeler)


__all__ = "labelers"
