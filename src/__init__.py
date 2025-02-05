import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

# 현재 파일(__init__.py)의 상위 폴더가 'src' 디렉토리임
# 더 상위(프로젝트 루트)까지 가려면 .parent를 추가로 호출
BASE_DIR = Path(__file__).resolve().parent.parent