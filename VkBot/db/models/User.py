from db.config import DeclarativeBase

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class User(DeclarativeBase):
    __tablename__ = "users"

    row_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    user_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    pdr_num = Column(Integer, default=0)
    fucked = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    pdr_of_the_year = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def params_list() -> list:
        return [User.user_id, User.chat_id, User.firstname, User.lastname, User.pdr_num,
                User.fucked, User.rating, User.pdr_of_the_year]

    def __str__(self) -> str:
        return f"Instanse from table users:\n" \
               f"id: {self.user_id}, chat_id: {self.chat_id}, firstname: {self.firstname}, lastname: {self.lastname},\n" \
               f"pdr_num: {self.pdr_num}, fucked: {self.fucked}, rating: {self.rating}, " \
               f"pdr_of_the_year: {self.pdr_of_the_year}.\n" \
               f"----------------------------------------------------------------------------------------------------\n"
