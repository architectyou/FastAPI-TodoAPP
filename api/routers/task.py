from fastapi import APIRouter, Depends, HTTPException
# 스키마 폴더의 예제 스키마를 이용하여 실제로 API 응답을 반환할 수 있는지 확인하기
# 나중에 DB와 연결하여 모델을 정의할 때 같은 이름의 task 파일을 구분하기 위해 task_schema 로 지정
import api.schemas.task as task_schema
from typing import List, Dict

# db 가져오기
from sqlalchemy.orm import Session
import api.cruds.task as task_crud
from api.db import get_db
router = APIRouter()

# 비동기
from sqlalchemy.ext.asyncio import AsyncSession

# @router.get("/tasks")
# async def list_tasks() :
#     #pass : 아무것도 하지 않는 문장
#     pass

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks(db : AsyncSession = Depends(get_db)) :
    return await task_crud.get_tasks_with_done(db)

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_tasks(task_body : task_schema.TaskCreate, db : AsyncSession = Depends(get_db)):
    return await task_crud.create_task(db, task_body)


@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    # db를 받아오도록 수정
    task_id : int, task_body : task_schema.TaskCreate, db : AsyncSession = Depends(get_db)
) :
    task = await task_crud.get_task(db, task_id = task_id)
    if task is None : 
        # task 가 없는 경우 HTTP exception을 출력하도록 설정
        # raise 문은 파이썬에서 예외를 명시적으로 발생시키는 데 이용됨
        raise HTTPException(status_code=404, detail = "Task not found")
    return await task_crud.update_task(db, task_body, original=task)

@router.delete("/tasks/{task_id}", response_model = None)
async def delete_tasks(task_id : int, db : AsyncSession = Depends(get_db)) :
    task = await task_crud.get_task(db, task_id = task_id)
    if task is None : 
        raise HTTPException(status_code=404, detail = "Task not found")
    
    return await task_crud.delete_task(db, original = task)
