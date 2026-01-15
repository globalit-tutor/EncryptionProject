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


# 게시트 리스트
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

# 게시판 글쓰기 폼
@app.get("/board/new", response_class=HTMLResponse)
def board_new_form(request: Request):
    return templates.TemplateResponse("board_new.html", {"request": request})

# 게시판 글쓰기 처리
@app.post("/board/new")
async def board_new(title: str = Form(...), username: str = Form(...), contents: str = Form(...)):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO board (title, username, contents) VALUES (?, ?, ?)",
            (title, username, contents))
        await db.commit()

    return RedirectResponse(url="/board", status_code=303)

# 게시판 본문글 처리
@app.get("/board/{bdno}", response_class=HTMLResponse)
async def board_detail(request: Request, bdno: int):
    async with aiosqlite.connect(DB_NAME) as db:
        # 조회수 증가
        await db.execute("UPDATE board SET views = views + 1 WHERE bdno = ?", (bdno,))
        await db.commit()

        # 상세 조회
        async with db.execute("SELECT * FROM board WHERE bdno = ?", (bdno,)) as cur:
            result = await cur.fetchone()

    if result is None:
        return HTMLResponse("해당 글이 존재하지 않습니다.", status_code=404)

    board = {
        "bdno": result[0],
        "title": result[1],
        "username": result[2],
        "regdate": result[3],
        "views": result[4],
        "contents": result[5],
    }

    return templates.TemplateResponse("board_detail.html", {
        "request": request,
        "bd": board
    })

# 게시글 삭제하기
@app.post("/board/{bdno}/delete")
async def board_delete(bdno: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM board WHERE bdno = ?", (bdno,))
        await db.commit()

    # 게시글 삭제 후 게시판 목록으로 전환
    return RedirectResponse(url="/board", status_code=303)


# 스크립트를 직접 실행할 때만 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("04Board_FastAPI:app", host="0.0.0.0", port=8000, reload=True)