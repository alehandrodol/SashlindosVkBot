from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from config import moscow_zone
from db.connection import SessionManager
from db.models import Votes


async def get_vote_by_id(vote_id: int, session: AsyncSession) -> Optional[Votes]:
    q = select(Votes).where(Votes.id == vote_id)
    vote: Votes = await session.scalar(q)
    return vote


async def get_vote_by_launched_ui(launched_ui: int, session: AsyncSession) -> list[Votes]:
    today = datetime.now(tz=moscow_zone).date()
    q = select(Votes).where(Votes.launched_ui == launched_ui, Votes.start_date == today)
    votes: ScalarResult = await session.scalars(q)
    return votes.all()


async def get_vote_by_target_ui(target_ui: int, session: AsyncSession) -> list[Votes]:
    today = datetime.now(tz=moscow_zone).date()
    q = select(Votes).where(Votes.target_ui == target_ui, Votes.start_date == today)
    votes: ScalarResult = await session.scalars(q)
    return votes.all()


async def set_vote(launched_ui: int, target_ui: int, rep: int, session: AsyncSession) -> Votes:
    today = datetime.now(tz=moscow_zone).date()
    vote = Votes(
        launched_ui=launched_ui,
        target_ui=target_ui,
        rep_num=rep,
        start_date=today
    )
    session.add(vote)
    await session.commit()
    return vote


async def finish_vote(vote: Votes) -> None:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        vote.finished = True
        session.add(vote)
        await session.commit()
    return
