# 파일명은 04bMemberBoard_FastAPI로 작성할 것!

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import aiosqlite
import sqlite3

BoardDB_NAME = "board.db"
MemberDB_NAME = "member.db"

# 데이터베이스 초기화/마무리를 비동기적으로 하는 코드
# 시작할 때 할 일과 끝날 때 할 일을 한 쌍으로 관리해 주는 라이프사이클 관리자
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiosqlite.connect(BoardDB_NAME) as db:
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

    async with aiosqlite.connect(MemberDB_NAME) as db:
        await db.execute("""
             CREATE TABLE IF NOT EXISTS member (
               memberid INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL,
               name TEXT,
               email TEXT UNIQUE,
               regdate TEXT DEFAULT (datetime('now','localtime'))
             )
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
    async with aiosqlite.connect(BoardDB_NAME) as db:
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
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute(
            "INSERT INTO board (title, username, contents) VALUES (?, ?, ?)",
            (title, username, contents))
        await db.commit()

    return RedirectResponse(url="/board", status_code=303)

# 게시판 본문글 처리
@app.get("/board/{bdno}", response_class=HTMLResponse)
async def board_detail(request: Request, bdno: int):
    async with aiosqlite.connect(BoardDB_NAME) as db:
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
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("DELETE FROM board WHERE bdno = ?", (bdno,))
        await db.commit()

    # 게시글 삭제 후 게시판 목록으로 전환
    return RedirectResponse(url="/board", status_code=303)


# 게시글 수정하기 폼
@app.get("/board/{bdno}/edit", response_class=HTMLResponse)
async def board_edit_form(request: Request, bdno: int):
    async with aiosqlite.connect(BoardDB_NAME) as db:
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

    return templates.TemplateResponse("board_edit.html", {
        "request": request,
        "bd": board
    })


# 게시글 수정하기 처리
@app.post("/board/{bdno}/edit")
async def board_edit(bdno: int, title: str = Form(...), contents: str = Form(...)):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("UPDATE board SET title = ?, contents = ? WHERE bdno = ?",
                         (title, contents, bdno))
        await db.commit()

    return RedirectResponse(url=f"/board/{bdno}", status_code=303)



# 요청이 들어오면 회원가입폼을 보여줌
@app.get("/join", response_class=HTMLResponse)
async def join_form(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})


# 회원정보를 입력하고 POST 요청하면 데이터베이스에 회원정보를 저장함
@app.post("/join", response_class=HTMLResponse)
async def joinok(request: Request, username: str = Form(...),
           password: str = Form(...), name: str = Form(""), email: str = Form("")):

    try:
        async with aiosqlite.connect(MemberDB_NAME) as db:
            await db.execute(
                "INSERT INTO member (username, password, name, email) VALUES (?, ?, ?, ?)",
                (username, password, name, email)
            )
            await db.commit()
    except sqlite3.IntegrityError:
        # username/email UNIQUE 중복 등
        return templates.TemplateResponse("join.html", {
            "request": request,
            "error": "이미 사용 중인 username 또는 email 입니다."
        })

    return templates.TemplateResponse("join_ok.html", {
        "request": request,
        "username": username,
        "name": name
    })


@app.get("/list", response_class=HTMLResponse)
async def member_list(request: Request):
    async with aiosqlite.connect(MemberDB_NAME) as db:
        results = await db.execute_fetchall("""
            SELECT memberid, username, name, email, regdate
            FROM member ORDER BY memberid DESC
            """)

    members = []
    for rs in results:
        member = { "memberid": rs[0], "username": rs[1],
                   "name": rs[2], "email": rs[3], "regdate": rs[4] }
        members.append(member)

    return templates.TemplateResponse("list.html", {
        "request": request,
        "members": members
    })


# 요청이 들어오면 로그인 폼을 보여줌
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 요청이 들어오면 입력한 로그인정보가 테이블에 존재하는지 여부 확인
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    async with aiosqlite.connect(MemberDB_NAME) as db:
        async with db.execute(
            "SELECT username, name, email, regdate FROM member WHERE username=? AND password=?",
            (username, password) ) as cur:
            member = await cur.fetchone()

    if member is None:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        })

    # 조회한 데이터를 JSON형식으로 생성
    member = {
        "username": member[0],
        "name": member[1],
        "email": member[2],
        "regdate": member[3],
    }

    return templates.TemplateResponse("loginok.html", {
        "request": request,
        "member": member
    })


# 스크립트를 직접 실행할 때만 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("04bMemberBoard_FastAPI:app", host="0.0.0.0", port=8000, reload=True)
