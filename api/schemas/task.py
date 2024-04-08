from pydantic import BaseModel, Field
from typing import List, Dict
# task 와 taskcreate의 공통 필드는 title 뿐이므로, 양 쪽에 title만 가진 베이스클래스로 
# TaskBase를 정의하고 task와 taskcreate는 이를 이용하도록 고쳐쓴다.

class TaskBase(BaseModel) :
    title : str | None = Field(None, example= "세탁소에 맡인 것을 찾으러 가기")

class TaskCreate(TaskBase) :
    pass


class TaskCreateResponse(TaskCreate) :
    id : int

    class config : 
        #orm_mode (DB 접속시 사용) -> TaskCreateResponse가 암묵적으로 ORM에서 DB 모델의 객체를 받아들여, 응답 스키마로 변환하는 것
        orm_mode = True


# FastAPI의 스키마
class Task(TaskBase) :
    id : int
    done : bool = Field(False, description="완료 플래그")

    class config : 
        #orm_mode (db접속시 사용)
        orm_mode = True