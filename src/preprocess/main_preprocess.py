from load_data import load_csv, DATA_DIR
from transform_data import (rename_and_filter_columns, convert_date_columns, clean_missing_values, convert_numeric_columns, dataframe_to_records)
from filter_data import filter_scholarships
import pprint

EXCLUDED_COLUMNS = [
    "학기", "추가자격", "계열", "학과", 
    "종교 조건", "진로 조건", "성별기준"
]
EXCLUDED_COLUMNS_GRADE = [
    "총(4.5)", "지난(4.5)", "총(4.3)", "지난(4.3)"
]

RENAME_MAP = {
    "운영기관명": "organization",
    "장학명": "name",
    "지원유형": "type",
    "지원내용": "description",
    "모집시작일": "applicationStartDate",
    "모집종료일": "applicationEndDate",
    "비고": "note",
    "소득기준": "incomeLevel",
    "학교": "university",
}

def preprocess_scholarships(csv_path: str):
    """
    장학금 CSV를 전처리하는 메인 함수.
    여러 단계 함수를 순서대로 호출하여 DataFrame을 가공한 뒤,
    최종적으로 List[Dict] 형태로 반환합니다.
    """

    # CSV 로드
    df = load_csv(csv_path)
    
    # 추가 조건 있는 장학금 제거
    df = filter_scholarships(df, EXCLUDED_COLUMNS, EXCLUDED_COLUMNS_GRADE)
    
    # 1) 컬럼명 변경
    df = rename_and_filter_columns(df, RENAME_MAP)
    # 2) 날짜 컬럼 변환
    df = convert_date_columns(df, ["applicationStartDate", "applicationEndDate"])
    # 3) 숫자 컬럼 변환
    df = convert_numeric_columns(df, ["incomeLevel"])
    # 4) 결측값 처리 (예: note가 NaN이면 빈 문자열로)
    df = clean_missing_values(df)

    # List[Dict] 형태로 변환
    records = dataframe_to_records(df)
    
    return df, records

if __name__ == "__main__":
    csv_path = "scholarships.csv"
    result_df, result_list = preprocess_scholarships(csv_path)

     # 1) 확인: Print first 15 records
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result_list[:15])

    result_df.to_csv(f"{DATA_DIR}/scholarships_preprocessed.csv", index=False, encoding="utf-8-sig")
    print(f"전처리 후 총 {len(result_list)}건 저장 완료.")
