# 작성한 ORM 모델을 바탕으로 DB에 테이블을 생성하고, DB 마이그레이션(이관)용 스크립트 작성하기
from sqlalchemy import create_engine

from api.models.task import Base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo = True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__" :
    reset_database()