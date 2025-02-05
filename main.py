from config.db_config import get_db_connection
from src.preprocess.main_preprocess import preprocess_scholarships
from src.data_insert import insert_full_scholarship
import pprint

def main():
    """
    1) CSV 파일을 전처리하여 DataFrame과 List[Dict] 변환
    2) DB에 전처리된 데이터를 삽입
    """
    # 1) 전처리 실행 및 저장
    result_df, result_list = preprocess_scholarships("scholarships.csv")
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(result_list[:15])
    result_df.to_csv(f"data/scholarships_preprocessed.csv", index=False, encoding="utf-8-sig")
    print(f"전처리 후 총 {len(result_list)}건 저장 완료.")

    # 3) DB에 삽입
    insert_scholarships_to_db(result_list)
    print(f"총 {len(result_list)}건 삽입 완료.")


def insert_scholarships_to_db(scholarships):
    """
    리스트 형태의 장학금 데이터를 MySQL DB에 삽입
    """
    connection = get_db_connection()
    try:
        for idx, scholarship in enumerate(scholarships, start=1):
            scholarship_id = insert_full_scholarship(connection, scholarship)
            print(f"[{idx}/{len(scholarships)}] Inserted scholarship with ID: {scholarship_id}")
    finally:
        connection.close()
        print("[DB] DB 연결 종료")

if __name__ == "__main__":
    main()