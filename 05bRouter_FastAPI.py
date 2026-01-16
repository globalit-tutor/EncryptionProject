from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from db import init_db
from routers.member import router as router_member
from routers.board import router as router_board
from routers.sungjuk import router as router_sungjuk


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_member)
app.include_router(router_board)
app.include_router(router_sungjuk)


@app.get("/", response_class=HTMLResponse)
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>FastAPI 회원/게시판/성적처리 앱</title>            
        </head>
    <body>
        <h1>FastAPI 회원/게시판/성적처리 앱</h1>
        <ul>
            <li><a href="/member/list">회원정보</a></li>
            <li><a href="/board/list">게시판 목록</a></li>
            <li><a href="/sungjuk/list">성적 목록</a></li>
        </ul>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05bRouter_FastAPI:app", host="0.0.0.0", port=8000, reload=True)

