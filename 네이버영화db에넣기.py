import pandas as pd
import pymysql
import csv
import datetime

# df = pd.read_csv('D:/파이썬 공부/web/crawling/movie/영화리스트(1).csv',
#                  encoding='utf-8-sig')

# conn = pymysql.connect(host=host, user=user,
#                        password=password, db=db, charset='utf8')
# cursor = conn.cursor()


# print('csv InSERT')

# for index, row in df.iterrows():
#     tu = (row['번호'], row['제목'], row['개봉날짜'],
#           row['감독'], row['배우'], row['장르'],
#           row['나라'], row['연령'], row['시간'],
#           row['줄거리'], row['이미지경로'])
#     cursor.execute('insert into main_movie(id, title, open_movie, director, actor, genre, country,age, content, img) values (%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
#                    tu)
# conn.commit()
# cursor.close()

print('OK')


def db_input():
    conn = pymysql.connect(host='localhost', user='root',
                           password='1', db='java_movie', charset='utf8')
    curs = conn.cursor()

    sql = 'insert into movie( title, openMovie, director, actor, genre, country,age,runningtime, content, img) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    f = open('D:/파이썬 공부/web/crawling/movie/영화리스트(5).csv',
             'r', encoding='utf-8-sig')
    rdr = csv.reader(f)
    for line in rdr:
        print(line)
        # line[0] = int(line[0])
        d = list(map(int, line[1].split('.')))
        date = datetime.date(d[0], d[1], d[2])
        formatted_date = date.strftime('%Y-%m-%d')
        print(formatted_date)
        curs.execute(sql, (line[0],  formatted_date, line[2], line[3],
                           line[4], line[5], line[6], line[7], line[8], line[9]))

    print('CSV Insert')
    conn.commit()
    conn.close()
    f.close()
    print('OK')


db_input()
