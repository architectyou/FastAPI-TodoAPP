# python3.11のイメージをダウンロード
# python3.11 이미지 다운로드
FROM python:3.11-buster
# pythonの出力表示をDocker用に調整
# python의 출력 표시를 Docker 용으로 조정
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pipを使ってpoetryをインストール
# pip로 poetry 설치
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
# poetry의 정의 파일 복사(존재하는 경우)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
# poetry로 라이브러리 설치 (project.toml이 이미 존재하는 경우)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicornのサーバーを立ち上げる
# uvicorn 서버 실행
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]