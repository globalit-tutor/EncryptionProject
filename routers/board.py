from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import BoardDB_NAME, templates
import aiosqlite


router = APIRouter(prefix="/board", tags=["board"])


# 게시트 리스트
@router.get("/list", response_class=HTMLResponse)
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

    return templates.TemplateResponse("board/board_list.html", {
        "request": request,
        "boards": boards,
        "user": request.session["user"]
    })

# 게시판 글쓰기 폼
@router.get("/new", response_class=HTMLResponse)
def board_new_form(request: Request):
    # 만일 로그인이 안되었다면 /member/login으로 이동
    if request.session.get("user") is None:
        return RedirectResponse(url="/member/login", status_code=303)

    # 세션변수 user에서 username을 뽑아서 board_new.html로 넘김
    return templates.TemplateResponse("board/board_new.html",
          {"request": request, "username":request.session.get("user")['username']})

# 게시판 글쓰기 처리
@router.post("/new")
async def board_new(title: str = Form(...), username: str = Form(...), contents: str = Form(...)):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute(
            "INSERT INTO board (title, username, contents) VALUES (?, ?, ?)",
            (title, username, contents))
        await db.commit()

    return RedirectResponse(url="/board/list", status_code=303)

# 게시판 본문글 처리
@router.get("/{bdno}", response_class=HTMLResponse)
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

    session_user = None
    if request.session.get("user"):
        session_user = request.session.get("user")['username']

    return templates.TemplateResponse("board/board_detail.html", {
        "request": request, "bd": board,
        "session_user": session_user # 세션 사용자를 템플릿에 넘김
    })

# 게시글 삭제하기
@router.post("/{bdno}/delete")
async def board_delete(bdno: int):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("DELETE FROM board WHERE bdno = ?", (bdno,))
        await db.commit()

    # 게시글 삭제 후 게시판 목록으로 전환
    return RedirectResponse(url="/board/list", status_code=303)


# 게시글 수정하기 폼
@router.get("/{bdno}/edit", response_class=HTMLResponse)
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

    return templates.TemplateResponse("board/board_edit.html", {
        "request": request,
        "bd": board
    })


# 게시글 수정하기 처리
@router.post("/{bdno}/edit")
async def board_edit(bdno: int, title: str = Form(...), contents: str = Form(...)):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("UPDATE board SET title = ?, contents = ? WHERE bdno = ?",
                         (title, contents, bdno))
        await db.commit()

    return RedirectResponse(url=f"/board/{bdno}", status_code=303)
