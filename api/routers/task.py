from fastapi import APIRouter
# 스키마 폴더의 예제 스키마를 이용하여 실제로 API 응답을 반환할 수 있는지 확인하기
# 나중에 DB와 연결하여 모델을 정의할 때 같은 이름의 task 파일을 구분하기 위해 task_schema 로 지정
import api.schemas.task as task_schema
from typing import List, Dict
router = APIRouter()

# @router.get("/tasks")
# async def list_tasks() :
#     #pass : 아무것도 하지 않는 문장
#     pass

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks() :
    return [task_schema.Task(id = 1, title = "첫 번째 ToDo 작업")]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_tasks(task_body : task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id = 1, **task_body.model_dump())

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreate)
async def update_task(task_id : int, task_body : task_schema.TaskCreate) :
    return task_schema.TaskCreateResponse(id=task_id, **task_body.model_dump())

@router.delete("/tasks/{task_id}")
async def delete_tasks(task_id : int) :
    return