import pymysql

conn = pymysql.connect(
    host='000.000.000.000',  # 호스트명
    port=3306,  # 포트번호
    user='admin',  # 유져 아이디
    password='admin1234',  # 유저 비밀번호
    db='test',  # db명
    charset='utf8mb4',  # 인코딩 설정
    autocommit=True,  # 자동으로 커밋
    connect_timeout=3600
)


def select(col):
    with conn.cursor() as curs:
        try:
            sql = "SELECT col1, co12 FROM test where col=%s"
            curs.execute(sql, col)
            result = curs.fetchall()
            return result
        except Exception as e:
            print(e)


def update(any1, any2):
    conn.connect()  # pymysql에서 connect가 끊기는 이슈가 있어서 재 연결
    with conn.cursor() as curs:
        try:
            sql = "UPDATE test SET col1 = %s WHERE col2 = %s"
            curs.execute(sql, (any1, any2))  # %s 순서대로 입력 [ ex) col1 = any1 , col2 = any2 ]
            curs.commit()  # autocommit이 있어서 자동으로 commit 되긴 하지만 명시적으로 적어둠
        except Exception as e:
            print(e)
