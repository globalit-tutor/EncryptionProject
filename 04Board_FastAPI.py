# 파일명은 04Board_FastAPI로 작성할 것!
# pip install aiosqlite

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import aiosqlite

DB_NAME = "board.db"

# 데이터베이스 초기화/마무리를 비동기적으로 하는 코드
# 시작할 때 할 일과 끝날 때 할 일을 한 쌍으로 관리해 주는 라이프사이클 관리자
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
         CREATE TABLE IF NOT EXISTS board (
              bdno INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              username TEXT NOT NULL,
              regdate TEXT DEFAULT (datetime('now','localtime')),
              views INTEGER DEFAULT 0,
              contents TEXT NOT NULL)
         """)
        await db.commit()

    # 함수를 중간에 멈췄다가 다시 이어서 실행하게 만드는 키워드
    # 한편, return은 함수를 완전히 종료하게 만드는 키워드
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index():
    return {"message": "Hello, World!"}


@app.get("/board", response_class=HTMLResponse)
async def board_list(request: Request):
    async with aiosqlite.connect(DB_NAME) as db:
        results = await db.execute_fetchall("""
            SELECT bdno, title, username, regdate, views
            FROM board ORDER BY bdno DESC""")

    # 조회된 결과집합을 html에서 처리하기 편하게 JSON형식으로 변환
    boards = []
    for rs in results:
        board = {
            "bdno": rs[0],
            "title": rs[1],
            "username": rs[2],
            "regdate": rs[3][:10],  # 년월일만 추출
            "views": rs[4]
        }
        boards.append(board)

    return templates.TemplateResponse("board_list.html", {
        "request": request,
        "boards": boards
    })


# 스크립트를 직접 실행할 때만 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("04Board_FastAPI:app", host="0.0.0.0", port=8000, reload=True)