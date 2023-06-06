from typing import List


from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from domain.product import product_schema
from domain.product.product_crud import create_product_bulk_insert, product_recommend_api, get_product_distinct_made_by_list
from domain.product.product_schema import ProductResponse, ProductRecommendRequest, ProductRecommendResponse
from models import Product

router = APIRouter(
    prefix="/api/v1/product",
)

@router.get('/unique')
def get_product_distinct(db: Session = Depends(get_db)):
    get_product_distinct_made_by_list(db)


@router.get("/list", response_model=list[product_schema.ProductResponse])
def product_list(db: Session = Depends(get_db)):
    _product_list = db.query(Product).all()

    return _product_list


@router.get("/refresh")
def crawling(db: Session = Depends(get_db)):
    create_product_bulk_insert(db=db)


@router.post("/recommend", response_model=List[ProductRecommendResponse])
def recommend(data: ProductRecommendRequest, db: Session = Depends(get_db)):
    return product_recommend_api(db=db, data=data)
