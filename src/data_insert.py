# TODO: DB에 삽입하는 로직 구현

# 1. 그대로 삽입
def insert_scholarship(connection, scholarship_data: dict) -> int:
    """
    Scholarship 테이블에 기본 정보를 INSERT하고, 생성된 scholarship_id (auto_increment)를 반환합니다.
    
    """
    sql = """
    INSERT INTO scholarship
    (application_end_date, application_start_date,
     description, income_level, name, note, organization, type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (
            scholarship_data.get("applicationEndDate") or None,  # NULL 가능(수정)
            scholarship_data.get("applicationStartDate") or None,  # NULL 가능
            scholarship_data["description"],                      # NOT NULL
            scholarship_data["incomeLevel"],                      # NOT NULL
            scholarship_data["name"],                             # NOT NULL
            scholarship_data.get("note"),                         # NULL 가능
            scholarship_data["organization"],                     # NOT NULL
            scholarship_data["type"]                              # ENUM ("TUITION", "LIVING_DUPLICATE", ...)
        ))
        connection.commit()
        return cursor.lastrowid  # AUTO_INCREMENT 된 PK


# 2. 정보 조작하여 넣기 (2) 대학
def insert_scholarship_universities(connection, scholarship_id: int, university_str: str):
    """
    쉼표로 구분된 university_str을 분리하여,
    university 테이블에서 university_id를 조회 후
    scholarship_university 테이블에 (scholarship_id, university_id) INSERT.
    
    예: university_str = "서울대학교, 고려대학교"
    """
    
    # 대학명이 쉼표로 구분되어 있을 수 있으니 split
    university_names = [u.strip() for u in university_str.split(",") if u.strip()]
    
    select_uni_sql = "SELECT id FROM university WHERE name = %s"
    insert_uni_sql = """
        INSERT INTO scholarship_university (scholarship_id, university_id, created_at)
        VALUES (%s, %s, NOW())
    """

    for uni_name in university_names:
        print(f"[DEBUG] 대학명: {uni_name}")


    with connection.cursor() as cursor:
        for uni_name in university_names:
            # 1) 대학 테이블에서 id 조회
            cursor.execute(select_uni_sql, (uni_name,))
            row = cursor.fetchone()
            
            if row:
                uni_id = row["id"]
                # 2) 연결 테이블에 삽입
                cursor.execute(insert_uni_sql, (scholarship_id, uni_id))
            else:
                # DB에 없는 대학명이라면(오탈자 등) 경고 or 무시
                print(f"[WARN] '{uni_name}' 대학을 찾지 못했습니다.")
        
        connection.commit()


# 3. 정보 조작하여 넣기 (3) 지역
def insert_scholarship_regions(connection, scholarship_id: int, region_big: str, region_small: str):
    """
    장학금-지역 관계 테이블에 데이터 삽입
    """
    if not region_big or region_big.strip() == "제한없음":
        return

    region_big = region_big.strip()
    region_small = region_small.strip() if region_small else None  # 소분류가 빈 값이면 None 처리

    select_region_sql = """
        SELECT id FROM region WHERE major_name = %s AND (minor_name = %s OR minor_name IS NULL)
    """
    insert_region_sql = """
        INSERT INTO scholarship_region (region_id, scholarship_id, created_at)
        VALUES (%s, %s, NOW())
    """

    with connection.cursor() as cursor:
        cursor.execute(select_region_sql, (region_big, region_small))
        row = cursor.fetchone()

        if row:
            region_id = row["id"]
            cursor.execute(insert_region_sql, (region_id, scholarship_id))
            connection.commit()
        else:
            print(f"[WARN] 지역정보 '{region_big}, {region_small}'가 region 테이블에 없습니다.")

def insert_full_scholarship(connection, scholarship_data: dict) -> int:
    """
    하나의 장학금(row_data)에 대해
      1) Scholarship 테이블에 기본 정보를 삽입하고 scholarship_id를 반환하고,
      2) 'university' 정보가 있다면, 쉼표로 분리하여 scholarship_university 테이블에 연결 정보를 삽입하며,
      3) 'region_big' (대분류)와 'region_small' (소분류) 정보가 있다면, scholarship_region 테이블에 연결 정보를 삽입합니다.
    
    각 단계에서 정보가 없거나(예: region_big가 없거나 "제한없음"이면) 해당 삽입은 생략됩니다.
    
    :param connection: PyMySQL 연결 객체
    :param scholarship_data: 장학금 정보를 담은 dict. 예시 키:
           "applicationEndDate", "applicationStartDate", "description",
           "incomeLevel", "name", "note", "organization", "type",
           "university", "region_big", "region_small"
    :return: 삽입된 Scholarship의 auto_increment id
    """
    # 1) Scholarship 테이블에 기본 정보 삽입
    scholarship_id = insert_scholarship(connection, scholarship_data)
    
    # 2) 대학 연결: 'university' 값이 있으면 처리
    university_str = scholarship_data.get("university", "").strip()
    if university_str:  # 값이 있다면
        insert_scholarship_universities(connection, scholarship_id, university_str)
    
    # 3) 지역 연결: region_big 값이 존재하고 "제한없음"이 아니라면 처리
    majorName = scholarship_data.get("majorName", "").strip()
    minorName = scholarship_data.get("minorName", "").strip()
    if majorName and majorName != "제한없음":
        insert_scholarship_regions(connection, scholarship_id, majorName, minorName)
    
    return scholarship_id