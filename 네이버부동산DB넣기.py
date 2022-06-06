import csv
import pandas as pd
import pymysql


def db_input():
    conn = pymysql.connect(host='localhost', user='root',
                           password='1', db='naver_real_estate', charset='utf8')
    curs = conn.cursor()

    sql = 'insert into locations_apartment(apt_name, apt_dong, apt_transaction_type, apt_price, apt_category, apt_flat, apt_real_flat, apt_height, apt_wind, apt_comment, apt_feature, apt_confirm, apt_confirm_date, apt_link, apt_register, apt_change_price, location_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

    f = open('./부동산/대연동전처리데이터(2022-06-03(21,48,53)).csv',
             'r', encoding='utf-8-sig')

    rdr = csv.reader(f)
    next(rdr)

    for line in rdr:
        curs.execute(sql, (line[0], line[1], line[2], line[3],
                           line[4], line[5], line[6], line[7], line[8],
                           line[9], line[10], line[11], line[12], line[13], line[14], line[15], '1'))

    print('CSV Insert')
    conn.commit()
    conn.close()
    f.close()
    print('OK')


db_input()
