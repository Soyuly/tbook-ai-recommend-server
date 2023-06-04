from sqlalchemy import Column, Integer, String, DECIMAL

from database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=True)
    product_made_by = Column(String(255), nullable=True)
    product_battery = Column(DECIMAL(10, 2), nullable=True)
    product_image = Column(String(255), nullable=True)
    product_cpu = Column(String(255), nullable=True)
    product_ram_capacity = Column(Integer, nullable=True)
    product_ram_detail = Column(String(255), nullable=True)
    product_display_size = Column(String(255), nullable=True)
    product_display_detail = Column(String(255), nullable=True)
    product_graphic = Column(String(255), nullable=True)
    product_storage_capacity = Column(Integer, nullable=True)
    product_storage_detail = Column(String(255), nullable=True)
    product_weight = Column(DECIMAL(10, 2), nullable=True)
    product_price = Column(Integer, nullable=True)
