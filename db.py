# 데이터베이스 초기화 관련 함수 정의
from settings import BoardDB_NAME, MemberDB_NAME, SungJukDB_NAME
import aiosqlite


async def init_db():
    async with aiosqlite.connect(SungJukDB_NAME) as db:
        await db.execute("""
         CREATE TABLE IF NOT EXISTS sungjuk (
             sjno INTEGER PRIMARY KEY AUTOINCREMENT,
             name varchar(10) NOT NULL,
             kor int not null,
             eng int not null,
             mat int not null,
             tot int default 0,
             avg float default 0.0,
             grd char(2) default 'F',
             regdate datetime default current_timestamp
             )
         """)
        await db.commit()

    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("""
         CREATE TABLE IF NOT EXISTS board (
              bdno INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              username TEXT NOT NULL,
              regdate TEXT DEFAULT (datetime('now','localtime')),
             views INTEGER DEFAULT 0,
             contents TEXT NOT NULL)
         """)
        await db.commit()

    async with aiosqlite.connect(MemberDB_NAME) as db:
        await db.execute("""
         CREATE TABLE IF NOT EXISTS member (
           memberid INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL UNIQUE,
           password TEXT NOT NULL,
           name TEXT,
           email TEXT UNIQUE,
           regdate TEXT DEFAULT (datetime('now','localtime'))
           )
         """)
        await db.commit()
