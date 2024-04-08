from sqlalchemy.orm import Session
# orm : Object Relational Mapper

import api.models.task as task_model
import api.schemas.task as task_schema

# 비동기용 CRUD 작성
from sqlalchemy.ext.asyncio import AsyncSession


# def create_task(db: Session, task_create : task_schema.TaskCreate) -> task_model.Task:
#     # task_schema.TaskCreate를 인수로 받아 DB 모델인 task_model.Task로 변환한다.
#     task = task_model.Task(**task_create.model_dump())
#     db.add(task)
#     db.commit()
#     # DB의 데이터를 바탕으로 Task 인스턴스인 task를 업데이트 한다. (작성된 레코드의 ID를 가져옴)
#     db.refresh(task)
#     # 생성된 DB 모델 반환 
#     return task

async def create_task(
          db : AsyncSession, task_create : task_schema.TaskCreate
) -> task_model.Task : 
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    # db 접속에서 (IO) 처리 과정이 발생하므로 대기 시간이 발생하는 처리를 할게요.라고 비동기 처리를 알리는 역할
    await db.commit()
    await db.refresh(task)
    return task

# 조인으로 Todo 작업에 done 플래그가 부여된 상태의 리스트 가져오기

from sqlalchemy import select
from sqlalchemy.engine import Result

async def get_tasks_with_done(db : AsyncSession) -> list[tuple[int, str, bool]] :
    result : Result = await db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )

    return result.all()


async def get_task(db : AsyncSession, task_id : int) -> task_model.Task | None : 
    result : Result = await db.execute(
         # filter method를 이용하여 SELECT-WHERE의 SQL 쿼리의 대상을 좁히고 있음.
        select(task_model.Task).filter(task_model.Task.id == task_id)
        # 지정한 요소가 하나라도 튜플로 반환되므로 튜플이 아닌 값으로 가져오는 과정이 필요.
    )
    return result.scalars().first()

async def update_task(
        db : AsyncSession, task_create : task_schema.TaskCreate, original : task_model.Task
    ) -> task_model.Task : 
        original.title = task_create.title
        db.add(original)
        await db.commit()
        await db.refresh(original)
        return original

async def delete_task(db : AsyncSession, original : task_model.Task) -> None : 
     await db.delete(original)
     await db.commit()