import time

from apscheduler.schedulers.background import BackgroundScheduler

from utils.crawler import crawling_notebook_info

scheduler = BackgroundScheduler(timezone='Asia/Seoul')


def job1():
    try:
        crawling_notebook_info()
    except Exception as e:
        print("crawling error", e)


scheduler.add_job(job1, 'interval', seconds=10, id="crawling")
scheduler.start()

while True:
    print("crawling start...")
    time.sleep(10)
