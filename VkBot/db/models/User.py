from db.config import DeclarativeBase

from sqlalchemy import Column, Integer, String, ForeignKey


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True, unique=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    pdr_num = Column(Integer, default=0)
    fucked = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    pdr_of_the_year = Column(Integer, default=0)

    def __str__(self) -> str:
        return f"Instanse from table users:\n" \
               f"id: {self.id}, chat_id: {self.chat_id}, firstname: {self.firstname}, lastname: {self.lastname},\n" \
               f"pdr_num: {self.pdr_num}, fucked: {self.fucked}, rating: {self.rating}, " \
               f"pdr_of_the_year: {self.pdr_of_the_year}.\n" \
               f"----------------------------------------------------------------------------------------------------\n"
