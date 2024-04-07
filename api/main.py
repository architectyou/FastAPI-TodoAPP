from fastapi import FastAPI

from api.routers import task, done

app = FastAPI()

#router
app.include_router(task.router)
app.include_router(done.router)

#pydantic 라이브러리를 이용하면 타입힌트를 적극적으로 활용하여 API 입출력의 유혀성 검사를 수행한다.
