from psycopg2.extras import RealDictCursor
from . import connectionUtils

def selectAll():
    conn = connectionUtils.get_database_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT tno, title, duedate, finished FROM tbl_todo")
            todos = cursor.fetchall()
            return todos
    finally:
        conn.close()

def selectOne(tno : int):
    conn = connectionUtils.get_database_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            sql = "SELECT * FROM tbl_todo WHERE tno = %s"
            cursor.execute(sql, (tno,))  # 튜플 형태로 파라미터 전달
            todo = cursor.fetchone()    
            return todo
    finally:
        conn.close()


def register(todoDTO):
    conn = connectionUtils.get_database_connection()
    try:
        with conn.cursor() as cursor:
            # INSERT 쿼리를 준비합니다. tno는 데이터베이스에서 자동 생성되므로 여기서는 명시하지 않습니다.
            # 데이터베이스에 따라 'RETURNING tno' 절을 추가하여 새로 생성된 tno 값을 받아올 수 있습니다.
            query = """
            INSERT INTO tbl_todo (title, duedate, finished)
            VALUES (%s, %s, %s)
            """
            # 쿼리를 실행하고 데이터를 데이터베이스에 삽입
            cursor.execute(query, (todoDTO.title, todoDTO.dueDate, todoDTO.finished))
            conn.commit()  # 트랜잭션 커밋            
    finally:
        conn.close()

def modify(todoDTO):
    conn = connectionUtils.get_database_connection()
    try:
        with conn.cursor() as cursor:
            query = "UPDATE tbl_todo SET title = %s, duedate = %s, finished = %s WHERE tno = %s"
            cursor.execute(query, (todoDTO.title, todoDTO.dueDate, todoDTO.finished, todoDTO.tno, ))            
            conn.commit()
    finally:
        conn.close()

def delete(tno : int):
    conn = connectionUtils.get_database_connection()
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM tbl_todo WHERE tno = %s"
            cursor.execute(query, (tno,))
            conn.commit()
    finally:
        conn.close()
