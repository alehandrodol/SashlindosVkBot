from db.config import DeclarativeBase

from sqlalchemy import Column, Integer, String, ForeignKey, Date


class Inventory(DeclarativeBase):
    __tablename__ = "inventory"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_row_id = Column(Integer, ForeignKey('users.row_id'))
    item_name = Column(String, unique=False)
    count = Column(Integer, default=0)
    get_date = Column(Date, nullable=False)
    expired_date = Column(Date, nullable=True)


class TagDoc(DeclarativeBase):
    __tablename__ = "tags_docs"

    id = Column(Integer, autoincrement=True, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    attachment_str = Column(String)
