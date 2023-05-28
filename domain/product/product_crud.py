from models import Product
from sqlalchemy.orm import Session


def get_product_list(db: Session):
    product_list = db.query(Product) \
        .all()

    return product_list
