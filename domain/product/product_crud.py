import pandas as pd
from fastapi import Depends

from database import get_db
from models import Product
from sqlalchemy.orm import Session

from utils.crawler import crawling_notebook_info


def get_product_list(db: Session):
    product_list = db.query(Product) \
        .all()

    return product_list


def create_product_bulk_insert(db: Session):
    db.query(Product).delete()
    db.bulk_save_objects(crawling_notebook_info())
    db.commit()
    return {"message": "success"}


def export_product_csv(db: Session):
    # 전체 데이터 가져오기
    result = db.query(Product).all()

    df = pd.DataFrame([{
        '제조사': p.product_made_by,
        '이름': p.product_name,
        '배터리': p.product_battery,
        '이미지': p.product_image,
        'cpu': p.product_cpu,
        '램 용량': p.product_ram_capacity,
        '램 상세': p.product_ram_detail,
        '화면크기': p.product_display_size,
        '화면상세': p.product_display_detail,
        '그래픽': p.product_graphic,
        '저장용량': p.product_storage_capacity,
        '저장용량 상세': p.product_storage_detail,
        '무게': p.product_weight,
        '가격': p.product_price,
        # 다른 속성들도 필요한 경우에 추가
    } for p in result])

    csv_filename = "products.csv"
    df.to_csv(f"static/{csv_filename}", index=False, encoding='utf-8-sig')


