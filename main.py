import time

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.product import product_router
from utils.crawler import crawling_notebook_info
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler(timezone='Asia/Seoul')


def job1():
    print("크롤링 시작")
    try:
        crawling_notebook_info()
    except Exception as e:
        print("crawling error", e)


# 87600초 = 하루
scheduler.add_job(job1, 'interval', seconds=87600, id="crawling")
scheduler.start()
app.include_router(product_router.router)


# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)