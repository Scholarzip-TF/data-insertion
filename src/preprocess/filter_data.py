import pandas as pd

def filter_scholarships(df: pd.DataFrame, EXCLUDED_COLUMNS, EXCLUDED_COLUMNS_GRADE) -> pd.DataFrame:
    """
    df에서 EXCLUDED_COLS 중 하나라도
    '제한없음'이 아닌 값이 들어 있다면 해당 row(장학금) 제거.
    """
    # 조건: 모든 배제 컬럼의 값이 "제한없음"일 때만 남긴다.
    # -> any(...) or all(...)
    # 여기서는 "제한없음" 외 값이 하나라도 있으면 제거해야 하므로,
    # all(...)을 사용해 '모두 "제한없음"인지' 체크.
    
    # df.apply()를 이용한 방법
    def has_no_other_filters(row):
        # 1) '제한없음' 문자 칼럼 체크
        for col in EXCLUDED_COLUMNS:
            # 해당 col이 실제 df에 없을 수도 있으니 체크
            if col in row.index:
                val = str(row[col]).strip()
                # 배제 조건: val != "제한없음" 이면 제외
                if val != "제한없음":
                    return False
        # 2) 숫자 칼럼 체크
        for col in EXCLUDED_COLUMNS_GRADE:
            if col in row.index:
                grade_val = str(row[col]).strip()
                if grade_val != "0.0":
                    return False
        return True
    
    def is_not_interest(row):
        if row["지원유형"] == "이자지원":
            return False
        return True

    # 유효한 row만 필터링
    filtered_df = df[df.apply(lambda row: has_no_other_filters(row) and is_not_interest(row), axis=1)]
    return filtered_df