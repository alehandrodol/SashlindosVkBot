from .test import chat_labeler
from .random_pdr import daily_labeler
from .games import games_labeler
from .general import general_labeler
from .statistics import stat_labeler
from .items_hands import items_labeler
from .bot_init import init_labeler
from .votes import votes_labeler

# Располагать от более приоритетных к менее, а при неопределённости более медленные в конец
labelers = (
    daily_labeler,
    stat_labeler,
    general_labeler,
    votes_labeler,
    games_labeler,
    items_labeler,
    chat_labeler,
    init_labeler
)


__all__ = "labelers"
