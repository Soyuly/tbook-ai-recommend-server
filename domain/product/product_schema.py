from pydantic import BaseModel


class ProductResponse(BaseModel):
    item_id: int
    item_name: str
    item_battery: str
    item_url: str
    item_cpu: str
    item_display: str
    item_graphic: str
    item_os: str
    item_ram: str
    item_storage: str
    item_weight: str
    item_price: int

    class Config:
        orm_mode = True


class ProductRecommendResponse(BaseModel):
    product_id: int
    product_image: str
    product_name: str
    similarity: float


class ProductRecommendRequest(BaseModel):
    ids: list
