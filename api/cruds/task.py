from sqlalchemy.orm import Session
# orm : Object Relational Mapper

import api.models.task as task_model
import api.schemas.task as task_schema


def create_task(db: Session, task_create : task_schema.TaskCreate) -> task_model.Task:
    # task_schema.TaskCreate를 인수로 받아 DB 모델인 task_model.Task로 변환한다.
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    db.commit()
    # DB의 데이터를 바탕으로 Task 인스턴스인 task를 업데이트 한다. (작성된 레코드의 ID를 가져옴)
    db.refresh(task)
    # 생성된 DB 모델 반환 
    return task


# 조인으로 Todo 작업에 done 플래그가 부여된 상태의 리스트 가져오기

from sqlalchemy import select
from sqlalchemy.engine import Result

def get_tasks_with_done(db : Session) -> list[tuple[int, str, bool]] :
    result : Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )

    return result.all()


def get_task(db : Session, task_id : int) -> task_model.Task | None : 
    result : Result = db.execute(
         # filter method를 이용하여 SELECT-WHERE의 SQL 쿼리의 대상을 좁히고 있음.
        select(task_model.Task).filter(task_model.Task.id == task_id)
        # 지정한 요소가 하나라도 튜플로 반환되므로 튜플이 아닌 값으로 가져오는 과정이 필요.
    )
    return result.scalars().first()

def update_task(
        db : Session, task_create : task_schema.TaskCreate, original : task_model.Task
    ) -> task_model.Task : 
        original.title = task_create.title
        db.add(original)
        db.commit()
        db.refresh(original)
        return original

def delete_task(db : Session, original : task_model.Task) -> None : 
     db.delete(original)
     db.commit()