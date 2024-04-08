# pytestdml fixture 정의하기
# fixture : 테스트에서 반복적으로 사용되는 설정이나 데이터를 한 곳에 모아 관리하는 개념
"""
1. 비동기식 db 접속용 engine과 session을 작성
2. 테스트용으로 온메모리 SQLite 테이블을 초기화 (함수별로 재설정)
3. DI로 FastAPI가 테스트용 DB를 참조하도록 변경
4. 테스트용으로 비동기 HTTP 클라이언트륿 반환

"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

# 실제로 테스트 코드 작성하기
import starlette.status


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    #비동기식 DB 접속을 위한 엔진과 세션을 작성
    async_engine = create_async_engine(ASYNC_DB_URL, echo = True)
    async_session = sessionmaker(
        autocommit = False, autoflush=False, bind = async_engine, class_ = AsyncSession
    )
    # 테스트용으로 온메모리 SQLite 테이블을 초기화(함수별로 재설정)
    async with async_engine.begin() as conn :
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 의존성 주입으로 FastAPI가 테스트용 DB를 참조하도록 변경
    async def get_test_db():
        async with async_session() as session : 
            yield session

    # get_db 함수는 일반적으로 api/db.py에서 가져오지만, 아래와 같이 정의함으로써
    # API 호출시 get_db 대신 get_test_db 를 사용하도록 오버라이드 함
    # 이로써 유닛테스트를 위해 프로덕션 코드인 router의 내용을 다시 작성할 필요 x
    app.dependency_overrides[get_db] = get_test_db

    # 테스트용으로 비동기 HTTP 클라이언트를 반환
    async with AsyncClient(app = app, base_url="http://test") as client : 
        yield client


@pytest.mark.asyncio
# 함수 인수에 위에서 정의한 async_clinet를 지정함으로써 픽스쳐의 반환값이 들어간 상태에서 함수를 실행시켜
# async_clinet.post()와 같이 클라이언트를 이용할 수 있음.
async def test_create_and_read(async_client) :
    # post 호출을 통해 ToDo 작업 생성
    response = await async_client.post("/tasks", json = {"title" : "테스트 작업"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "테스트 작업"

    # get 호출을 통해 ToDo 작업 확인
    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "테스트 작업"
    assert response_obj[0]["done"] is False

# 완료 플래그를 이용한 테스트 추가하기
@pytest.mark.asyncio 
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json = {"title" : "테스트 작업2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "테스트 작업2"

    # 완료 플래그 설정
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 이미 완료 플래그가 설정되어 있으므로 400을 반환
    response = await async_client.put("/task/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    # 완료 플래그 해제
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 이미 완료 플래그가 해제되었으므로 404를 반환
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND