from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def load_csv(filename: str) -> pd.DataFrame:
    """
    CSV를 DataFrame으로 로드하는 함수.
    """
    csv_path = DATA_DIR / filename
    print(f"Load CSV from {csv_path}")
    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
        return df
    except Exception as e:
        # 상황에 따라 로깅하거나, 특정 예외를 던지도록 처리 가능
        raise RuntimeError(f"CSV 파일을 불러오는 중 오류 발생: {e}")
