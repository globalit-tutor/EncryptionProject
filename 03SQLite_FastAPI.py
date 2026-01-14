# 파일명은 03SQLite_FastAPI로 작성할 것!

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# DB 파일 지정
DB_NAME = "member.db"

# member 테이블 생성 함수
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS member (
          memberid INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL,
          name TEXT,
          email TEXT UNIQUE,
          regdate TEXT DEFAULT (datetime('now','localtime')) 
          )
        """)
    conn.commit()
    conn.close()

# 테이블 생성 함수 호출
init_db()


# 루트 경로("/")에 GET 요청이 들어오면 실행될 함수 정의
@app.get("/", response_class=HTMLResponse)
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>회원로그인</title>
        </head>
    <body>
        <h1>회원관리 웹앱</h1>
        <ul>
            <li><a href="/login">로그인</a></li>
            <li><a href="/join">회원가입</a></li>
            <li><a href="/list">회원목록조회</a></li>
        </ul>
    </body>
    </html>
    """
    return html_content


# 요청이 들어오면 회원가입폼을 보여줌
@app.get("/join", response_class=HTMLResponse)
def join_form(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})


# 회원정보를 입력하고 POST 요청하면 데이터베이스에 회원정보를 저장함
@app.post("/join", response_class=HTMLResponse)
def joinok(request: Request, username: str = Form(...),
        password: str = Form(...), name: str = Form(""), email: str = Form("")):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO member (username, password, name, email) VALUES (?, ?, ?, ?)",
            (username, password, name, email)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # username/email UNIQUE 중복 등
        conn.close()
        return templates.TemplateResponse("join.html", {
            "request": request,
            "error": "이미 사용 중인 username 또는 email 입니다."
        })

    conn.close()

    return templates.TemplateResponse("join_ok.html", {
        "request": request,
        "username": username,
        "name": name
    })


@app.get("/list", response_class=HTMLResponse)
def member_list(request: Request):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT memberid, username, name, email, regdate
        FROM member
        ORDER BY memberid DESC
        """)
    members = cur.fetchall()
    conn.close()

    return templates.TemplateResponse("list.html", {
        "request": request,
        "members": members
    })


# 요청이 들어오면 로그인 폼을 보여줌
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 요청이 들어오면 입력한 로그인정보가 테이블에 존재하는지 여부 확인
@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT username, name, email, regdate FROM member WHERE username=? AND password=?",
        (username, password)
    )
    member = cur.fetchone()
    conn.close()

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("03SQLite_FastAPI:app", host="0.0.0.0", port=8000, reload=True)
    
    