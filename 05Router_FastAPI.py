from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from db import init_db
from routers.member import router as router_member
from routers.board import router as router_board
from starlette.middleware.sessions import SessionMiddleware
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_member)
app.include_router(router_board)
# 보안사항 : 보안키는 절대! 하드코딩하지 말고, 반드시 환경변수등에 등록해서 사용할 것!
# app.add_middleware(SessionMiddleware, secret_key="CHANGE_ME_TO_A_LONG_RANDOM_SECRET_KEY")
# 윈도우에서는 시스템 속성 - 환경변수 - 시스템변수에서 환경변수 등록 후 인텔리제이 재시작
# 터미널에서 환경변수 조회 : echo %SESSION_SECRET_KEY%
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))
print(os.getenv("SESSION_SECRET_KEY"))

@app.get("/", response_class=HTMLResponse)
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>FastAPI 회원/게시판앱</title>            
        </head>
    <body>
        <h1>FastAPI 회원/게시판앱</h1>
        <ul>
            <li><a href="/member/list">회원정보</a></li>
            <li><a href="/board/list">게시판 목록</a></li>
        </ul>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05Router_FastAPI:app", host="0.0.0.0", port=8000, reload=True)

