from psycopg2.extras import RealDictCursor
from . import connectionUtils

def getWithPassword(memberDTO):
    conn = connectionUtils.get_database_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT mid, mpw, mname FROM tbl_member WHERE mid = %s and mpw = %s"
            cursor.execute(query, (memberDTO.mid, memberDTO.mpw, ))
            memberDTO_n = cursor.fetchone()    
            return memberDTO_n
    finally:
        conn.close()