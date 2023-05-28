from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Product(Base):
    __tablename__ = "product"

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False)
    item_battery = Column(String(255), nullable=False)
    item_url = Column(String(255), nullable=True)
    item_cpu = Column(String(255), nullable=False)
    item_display = Column(String(255), nullable=False)
    item_graphic = Column(String(255), nullable=False)
    item_os = Column(String(255), nullable=False)
    item_ram = Column(String(255), nullable=False)
    item_storage = Column(String(255), nullable=False)
    item_weight = Column(String(255), nullable=False)
    item_price = Column(Integer, nullable=False)
