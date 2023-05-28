from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

"""
DB 접속 정보 설정
"""
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# DB 설정 정보 저장
engine = create_engine('mysql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username=DB_USER_NAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db_name=DB_NAME
))

# DB 커넥션 만들기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
