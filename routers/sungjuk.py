from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from db import SungJuk_New_SQL
from settings import SungJukDB_NAME, templates
import aiosqlite


router = APIRouter(prefix="/sungjuk", tags=["sungjuk"])


@router.get("/list", response_class=HTMLResponse)
async def sungjuk_list(request: Request):
    async with aiosqlite.connect(SungJukDB_NAME) as db:
        results = await db.execute_fetchall("""
        SELECT sjno, name, kor, eng, mat
        FROM sungjuk ORDER BY sjno DESC""")

    # 조회된 결과집합을 html에서 처리하기 편하게 JSON형식으로 변환
    sungjuks = []
    for rs in results:
        sungjuk = {
            "sjno": rs[0],
            "name": rs[1],
            "kor": rs[2],
            "eng": rs[3],
            "mat": rs[4]
        }
        sungjuks.append(sungjuk)

    return templates.TemplateResponse("sungjuk/sungjuk_list.html", {
        "request": request,
        "sungjuks": sungjuks
    })


@router.get("/new", response_class=HTMLResponse)
async def sungjuk_newform(request: Request):
    return templates.TemplateResponse("sungjuk/sungjuk_new.html", {"request": request})


@router.post("/new", response_class=HTMLResponse)
async def sungjuk_new(request: Request, name: str = Form(...),
       kor: int = Form(...), eng: int = Form(...), mat: int = Form(...)):
    # 성적 처리 (총점/평균/학점 계산)
    tot, avg, grd = compute_sungjuk(kor, eng, mat)

    async with aiosqlite.connect(SungJukDB_NAME) as db:
        await db.execute(SungJuk_New_SQL,
            (name, kor, eng, mat, tot, avg, grd))
        await db.commit()

    return RedirectResponse(url="/sungjuk/list", status_code=303)


@router.get("/{sjno}", response_class=HTMLResponse)
async def sungjuk_detail(request: Request, sjno: int):
    async with aiosqlite.connect(SungJukDB_NAME) as db:
        # 상세 조회
        async with db.execute("SELECT * FROM sungjuk WHERE sjno = ?", (sjno,)) as cur:
            result = await cur.fetchone()

    if result is None:
        #return HTMLResponse("해당 글이 존재하지 않습니다.", status_code=404)
        return RedirectResponse("/sungjuk/list", status_code=303)

    sungjuk = {
        "sjno": result[0],
        "name": result[1],
        "kor": result[2],
        "eng": result[3],
        "mat": result[4],
        "tot": result[5],
        "avg": result[6], #round(result[6], 1),
        "grd": result[7],
        "regdate": result[8]
    }

    return templates.TemplateResponse("sungjuk/sungjuk_detail.html", {
        "request": request,
        "sj": sungjuk
    })


# @router.get 으로 설정하는 경우, 405 Method not allow 오류 발생!!
@router.post("/{sjno}/delete", response_class=HTMLResponse)
async def sungjuk_delete(sjno: int):
    async with aiosqlite.connect(SungJukDB_NAME) as db:
        await db.execute("DELETE FROM sungjuk WHERE sjno = ?", (sjno,))
        await db.commit()

    # 게시글 삭제 후 게시판 목록으로 전환
    return RedirectResponse(url="/sungjuk/list", status_code=303)


@router.get("/{sjno}/edit", response_class=HTMLResponse)
async def sungjuk_editform(request: Request, sjno: int):
    async with aiosqlite.connect(SungJukDB_NAME) as db:
        async with db.execute("SELECT * FROM sungjuk WHERE sjno = ?", (sjno,)) as cur:
            result = await cur.fetchone()

    if result is None:
        # return HTMLResponse("해당 글이 존재하지 않습니다.", status_code=404)
        return RedirectResponse("/sungjuk/list", status_code=303)

    sungjuk = {
        "sjno": result[0],
        "name": result[1],
        "kor": result[2],
        "eng": result[3],
        "mat": result[4],
        "tot": result[5],
        "avg": result[6], #round(result[6], 1),
        "grd": result[7],
        "regdate": result[8]
    }

    return templates.TemplateResponse("sungjuk/sungjuk_edit.html", {
        "request": request,
        "sj": sungjuk
    })



@router.post("/{sjno}/edit", response_class=HTMLResponse)
async def sungjuk_edit(request: Request, sjno: int,
    kor: int = Form(...), eng: int = Form(...), mat: int = Form(...)):
    # 총점, 평균, 학점 재계산
    tot, avg, grd = compute_sungjuk(kor, eng, mat)

    async with aiosqlite.connect(SungJukDB_NAME) as db:
        await db.execute(
            """UPDATE sungjuk SET kor = ?, eng = ?, mat = ?,
            tot = ?, avg = ?, grd = ? WHERE sjno = ?""",
            (kor, eng, mat, tot, avg, grd, sjno))
        await db.commit()

    return RedirectResponse(url=f"/sungjuk/{sjno}", status_code=303)



def compute_sungjuk(kor, eng, mat):
    """
    성적 데이터에 대한 총점,평균,학점 처리

    :return:
    """
    tot = kor + eng + mat
    avg = tot / 3
    grd = ('A' if (avg >= 90) else
           'B' if (avg >= 80) else
           'C' if (avg >= 70) else
           'D' if (avg >= 60) else 'F')

    return tot, avg, grd
