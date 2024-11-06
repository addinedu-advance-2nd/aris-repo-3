import pymysql
import pandas as pd

# MySQL 데이터베이스 연결 설정
connection = pymysql.connect(
    host='localhost',        # MySQL 서버 주소
    user='jyh',     # MySQL 사용자 이름
    password='1', # MySQL 비밀번호
    database='BARTENDROID', # 사용할 데이터베이스 이름
    charset='utf8mb4',        # 문자 인코딩 설정
    cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리 형태로 반환
)

query = "SELECT * FROM ICECREAM"
icecream_df = pd.read_sql(query, connection)

# print(icecream_df)
# print(icecream_df.columns)
# print(icecream_df.head())
# print(icecream_df.describe())

# 특정열
# selected_columns = icecream_df[['CATEGORY', 'NAME']]
# print(selected_columns.head())

# 필터링 (특정열 + 특정조건)
# remium_icecreams = icecream_df[icecream_df['category'] == 'Premium']
# print(premium_icecreams)

# INSERT

# UPDATE

# DELETE

connection.close()
