# 파일명은 01Hello_FastAPI로 작성할 것!
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse

app = FastAPI()

@app.get("/")
async def json_hello():
    return {"message": "Hello, World!"}


@app.get("/thello", response_class=PlainTextResponse)
def text_hello():
    # 텍스트로 응답
    return "Hello, World!"


@app.get("/hhello", response_class=HTMLResponse)
def html_hello():
    # html로 응답
    html_content = """
		<!DOCTYPE html>
		<html>
		    <head>
		        <title>Hello Page</title>
		    </head>
		    <body>
		        <h1>Hello, World!</h1>
		        <p>FastAPI로 만든 HTML 페이지입니다.</p>
		    </body>
		</html>
		"""
    return html_content


if __name__ == "__main__":
    import uvicorn  # uvicorn을 직접 임포트해서 사용
    uvicorn.run('01Hello_FastAPI:app', host="0.0.0.0", port=8000, reload=True)

