from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.product import product_schema
from models import Product

router = APIRouter(
    prefix="/api/v1/product",
)


@router.get("/list", response_model=list[product_schema.ProductResponse])
def product_list(db: Session = Depends(get_db)):
    _product_list = db.query(Product).all()

    return _product_list
