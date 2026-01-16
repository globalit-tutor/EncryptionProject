from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
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
        await db.execute(
            """insert into sungjuk (name,kor,eng,mat,tot,avg,grd) 
               values (?, ?, ?, ?, ?, ?, ?)""",
            (name, kor, eng, mat, tot, avg, grd))
        await db.commit()

    return RedirectResponse(url="/sungjuk/list", status_code=303)


@router.get("/{sjno}", response_class=HTMLResponse)
async def sungjuk_detail(request: Request, sjno: int):
    pass


@router.get("/{sjno}/delete", response_class=HTMLResponse)
async def sungjuk_delete(sjno: int):
    pass


@router.get("/{sjno}/edit", response_class=HTMLResponse)
async def sungjuk_editform(request: Request, sjno: int):
    pass


@router.post("/{sjno}/edit", response_class=HTMLResponse)
async def sungjuk_edit(request: Request, sjno: int,
    kor: int = Form(...), eng: int = Form(...), mat: int = Form(...)):
    pass


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
