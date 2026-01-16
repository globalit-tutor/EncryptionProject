import aiosqlite, sqlite3
from settings import templates, MemberDB_NAME
from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse


# member 라우트 설정
router = APIRouter(prefix="/member", tags=["member"])


# 요청이 들어오면 회원가입폼을 보여줌
@router.get("/join", response_class=HTMLResponse)
async def join_form(request: Request):
    return templates.TemplateResponse("member/join.html", {"request": request})


# 회원정보를 입력하고 POST 요청하면 데이터베이스에 회원정보를 저장함
@router.post("/join", response_class=HTMLResponse)
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
        return templates.TemplateResponse("member/join.html", {
            "request": request,
            "error": "이미 사용 중인 username 또는 email 입니다."
        })

    return templates.TemplateResponse("member/join_ok.html", {
        "request": request,
        "username": username,
        "name": name
    })


@router.get("/list", response_class=HTMLResponse)
async def member_list(request: Request):
    # 로그인하지 않았다면 /member/login 으로 이동
    if request.session.get("user") is None:
        return RedirectResponse(url="/member/login", status_code=303)

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

    return templates.TemplateResponse("member/list.html", {
        "request": request,
        "members": members
    })


# 요청이 들어오면 로그인 폼을 보여줌
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    # 이미 로그인 상태면 /board/list로 이동
    if request.session.get("user"):
        return RedirectResponse(url="/board/list", status_code=303)

    return templates.TemplateResponse("member/login.html", {"request": request})


# 요청이 들어오면 입력한 로그인정보가 테이블에 존재하는지 여부 확인
@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    async with aiosqlite.connect(MemberDB_NAME) as db:
        async with db.execute(
                "SELECT username, name, email, regdate FROM member WHERE username=? AND password=?",
                (username, password) ) as cur:
            member = await cur.fetchone()

    if member is None:
        return templates.TemplateResponse("member/login.html", {
            "request": request,
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        })

    # 세션에 저장(필요한 최소 정보만)
    request.session["user"] = {
        "username": member[0],
        "name": member[1]
    }

    # 조회한 데이터를 JSON형식으로 생성
    member = {
        "username": member[0],
        "name": member[1],
        "email": member[2],
        "regdate": member[3],
    }

    return templates.TemplateResponse("member/loginok.html", {
        "request": request,
        "member": member
    })


# 로그아웃 처리
@router.get("/logout")
async def logout(request: Request):
    request.session.clear()     # 세션변수 제거
    return RedirectResponse(url="/member/login", status_code=303)

