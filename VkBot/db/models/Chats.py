from db.config import DeclarativeBase

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean


class Chat(DeclarativeBase):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    today_pdr = Column(Integer, nullable=True)
    today_pass = Column(Integer, nullable=True)
    year_pdr = Column(Integer, nullable=True)

    def __str__(self) -> str:
        return f"Instanse from table chats:\n" \
               f"id: {self.id}; name: {self.name}, today_pdr: {self.today_pdr}, today_pass: {self.today_pass}, " \
               f"pdr_date: {self.pdr_date},\nyear_pdr: {self.year_pdr}, year_pdr_num: {self.year_pdr_num},\n" \
               f"----------------------------------------------------------------------------------------------------\n"


class LaunchInfo(DeclarativeBase):
    __tablename__ = "launch_info"

    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True)
    day_phrase = Column(String, nullable=True)
    up_to_date_phrase = Column(Boolean, default=False)
    daily_launch_date = Column(Date, nullable=True)
    year_launch_num = Column(Integer, nullable=True)
    who_launched = Column(Integer, ForeignKey('users.row_id'), nullable=True)
    launch_streak = Column(Integer, default=1)
