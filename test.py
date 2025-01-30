from config.db_config import get_db_connection
import pytest

def test_db_connection():
    """
    PyMySQL DB 연결이 정상적으로 되는지 테스트합니다.
    """
    conn = get_db_connection()
    assert conn is not None, "DB 연결에 실패했습니다."
    conn.close()

def test_sql_select():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM region"
    cursor.execute(sql)
    # fetch 메서드(조회결과 콘솔창에서 보기 위함)
    result = cursor.fetchall() # fetchall() : 전부 가져오기
    # 실행 결과 콘솔창에서 출력
    for data in result:
        print(data)
    # commit 및 연결 해제
    # conn.commit() # 커밋은 반복할 필요 없음
    conn.close()

    