import csv
import pandas as pd
import pymysql
from datetime import datetime

oc_date = "2023-01-01"  # 이 날 이후 데이터만 DB에 넣기
oc_todate_date = datetime.strptime(oc_date, "%Y-%m-%d")


def db_input():
    count = 0
    conn = pymysql.connect(host='localhost', user='root',
                           password='1', db='naver_real_estate', charset='utf8')
    curs = conn.cursor()

    sql = 'insert into locations_apartment values (null ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

    f = open('./부동산/대연동전처리데이터(2023-04-19(03,01,20)).csv',
             'r', encoding='utf-8-sig')

    rdr = csv.reader(f)
    next(rdr)

    for line in rdr:
        line[12] = datetime.strptime(line[12], "%Y-%m-%d")
        if line[12] > oc_todate_date:
            count += 1
            curs.execute(sql, (line[0], line[1], line[2], line[3],
                               line[4], line[5], line[6], line[7], line[8],
                               line[9], line[10], line[11], line[12], line[13], line[14], line[15], '1'))
        else:
            continue

    print('CSV Insert')
    conn.commit()
    conn.close()
    f.close()
    print('OK')
    print('총 들어간수: ', count)


if __name__ == '__main__':
    db_input()
