import pandas as pd
from typing import List, Dict

def rename_and_filter_columns(df: pd.DataFrame, rename_map: Dict[str, str]) -> pd.DataFrame:
    """
    1) rename_map에 정의된 컬럼들만 추출하고
    2) 해당 컬럼들을 영문명으로 변경합니다.
    """
    # 1) 실제 df에 존재하는 컬럼만 추려냅니다.
    existing_cols = [col for col in rename_map.keys() if col in df.columns]

    # 2) 기존 컬럼들만 남긴 뒤
    #    rename_map으로 컬럼명을 변경합니다.
    df = df[existing_cols].rename(columns=rename_map)
    
    return df

def convert_date_columns(df: pd.DataFrame, date_cols: List[str]) -> pd.DataFrame:
    """
    date_cols로 지정된 컬럼을 날짜 형식으로 변환합니다.
    """
    
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                format="%m/%d/%y",  # 11/14/23 → 2023-11-14
                errors="coerce"
            )  # datetime 객체 (ISO 형식의 YYYY-MM-DD HH:MM:SS)
    return df

def convert_numeric_columns(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    """
    numeric_cols로 지정된 컬럼을 숫자로 변환합니다. 변환 불가한 데이터는 0으로 채웁니다.
    """
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df

def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    다음 조건에 해당하는 모든 셀을 빈 문자열("")로 통일합니다.
    1) NaN(결측치)
    2) "정보 없음"
    3) "제한없음"
    """
    # 1) 특정 키워드를 결측치(pd.NA)로 변환
    keywords_to_null = ["정보 없음", "제한없음"]
    df = df.replace(to_replace=keywords_to_null, value=pd.NA)
    
    # 2) 결측치(NaN 또는 pd.NA)를 빈 문자열("")로 변환
    df = df.fillna("")

    return df


def dataframe_to_records(df: pd.DataFrame) -> List[Dict]:
    """
    DataFrame을 List[Dict] 형태로 변환.
    DB 삽입 등의 후속 작업에 활용하기 좋습니다.
    """
    records = df.to_dict(orient="records")
    return records
