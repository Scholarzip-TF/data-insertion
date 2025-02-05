from config.db_config import get_db_connection
from datetime import date
from src.data_insert import insert_full_scholarship  # 통합 함수 import
from dotenv import load_dotenv

def test_db_connection():
    """
    PyMySQL DB 연결이 정상적으로 되는지 테스트합니다.
    """
    conn = None
    try:
        conn = get_db_connection()
        assert conn is not None, "DB 연결에 실패했습니다."
        print("[DB] DB 연결 성공")
    except Exception as e:
        print(f"[DB] DB 연결 실패: {e}")
    finally:
        if conn:
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


def test_insert_single_scholarship():
    # 테스트용 장학금 데이터 (CSV 한 행에 해당)
    scholarship_data = {
        "organization": "(재)음성군장학회",
        "name": "군민 평생 장학생",
        # DB 스키마의 ENUM 값: ('등록금', '생활비 - 타 장학 중복 O', '생활비 - 타 장학 중복 X', '이자지원')
        "type": "LIVING_DUPLICATE",
        "description": "300,000원",
        "applicationStartDate": date(2023, 9, 14),
        "applicationEndDate": date(2023, 9, 27),
        "note": "공고일(2023. 9. 14.) 현재 1년 이상 음성군에 주소를 두고 계속 거주하는 군민",
        "incomeLevel": 10,
        # 여러 대학이 쉼표로 구분되어 있다면
        "university": "서울대학교, 고려대학교",
        # 지역 정보: Region 테이블의 major_name, minor_name
        "majorName": "부산광역시",
        "minorName": "북구"
    }
    
    # DB 연결 정보 (실제 환경에 맞게 수정)
    connection = get_db_connection()
    
    try:
        scholarship_id = insert_full_scholarship(connection, scholarship_data)
        print(f"Inserted scholarship with ID: {scholarship_id}")
    finally:
        connection.close()

if __name__ == "__main__":
    # test_db_connection()
    # test_sql_select()
    test_insert_single_scholarship()