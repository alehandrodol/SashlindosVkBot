from db.config import DeclarativeBase

from sqlalchemy import Column, Integer, String, ForeignKey, Date


class Inventory(DeclarativeBase):
    __tablename__ = "inventory"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_row_id = Column(Integer, ForeignKey('users.id'))
    item_name = Column(String, unique=False)
    count = Column(Integer, default=0)
    get_date = Column(Date, nullable=False)
    expired_date = Column(Date, nullable=True)

