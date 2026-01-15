from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from db import init_db
from routers.member import router as router_member


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_member)


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
