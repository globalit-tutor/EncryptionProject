# 데이터베이스/템플릿 관련 설정
from fastapi.templating import Jinja2Templates

BoardDB_NAME = "board.db"
MemberDB_NAME = "member.db"
SungJukDB_NAME = "sungjuk.db"

templates = Jinja2Templates(directory="templates")
