from pymysql import connect
from tqdm import tqdm

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()

sql = 'select author_user_id from vedio' \
      'where author_user_id not in user.uid '

row_count = cur.execute(sql)

row_sample = cur.fetchmany(10)

for row in row_sample:
      print(row[0])