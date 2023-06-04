from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import APIRouter, Depends
from fastapi_amis_admin.admin import AdminSite, Settings
from fastapi_scheduler import SchedulerAdmin
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from database import get_db
from domain.product import product_schema
from domain.product.product_crud import create_product_bulk_insert, export_product_csv
from models import Product

router = APIRouter(
    prefix="/api/v1/product",
)


@router.get("/list", response_model=list[product_schema.ProductResponse])
def product_list(db: Session = Depends(get_db)):
    _product_list = db.query(Product).all()

    return _product_list


@router.get("/refresh")
def crawling(db: Session = Depends(get_db)):
    create_product_bulk_insert(db=db)


@router.get("/recommend")
def recommend(db: Session = Depends(get_db)):
    export_product_csv(db=db)
    csv_filename = "products.csv"
    return FileResponse(f"static/{csv_filename}", media_type="text/csv", filename=csv_filename)
