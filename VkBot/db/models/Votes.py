from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean

from db.config import DeclarativeBase


class Votes(DeclarativeBase):
    __tablename__ = "votes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    launched_ui = Column(Integer, ForeignKey('users.row_id'), nullable=False)
    target_ui = Column(Integer, ForeignKey('users.row_id'), nullable=False)
    rep_num = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    finished = Column(Boolean, default=False)
