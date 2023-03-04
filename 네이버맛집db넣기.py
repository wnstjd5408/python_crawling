import pandas as pd
import pymysql
import csv
import datetime
import re


def cleanText(data):
    extracts = re.compile('[^ 가-힣|a-z|A-Z|0-9|\[|\]|(|)|-|~|?|!|.|,|:|;|%]+')
    data = extracts.sub('', data)

    return data


def db_input():
    conn = pymysql.connect(host='localhost', user='root',
                           password='1', db='django_board', charset='utf8')
    curs = conn.cursor()
# ['번호', '가게명', '가게정보', '평점', '방문자리뷰','블로그리뷰', '위치', '근처 지하철역', '시간', '이미지 URL', '등록날짜']
    sql = 'insert into place_place(place_name, place_info, place_review_score, place_review_visit, place_review_blog, place_location, place_subway, place_time, place_sns_site, place_imageurl, place_register, location_id) values ( %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# (place_name, place_info, place_review_score, place_review_visit, place_review_blog, place_location, place_subway, place_time, place_sns_siste, place_imageurl, place_register)
    f = open('./place/부산대카페(2023-03-04(17,28,53)).csv', 'r',
             encoding='utf-8-sig')
    rdr = csv.reader(f)
    delete_sql = 'delete from place_place where location_id = %s'
    curs.execute(delete_sql, '1')

    next(rdr)
    count = 0
    for line in rdr:
        count += 1
        print(count, ":", line)
        if line[3] == '':
            line[3] = '0'
        else:
            line[3] = line[3].replace(",", "")
        if line[4] == '':
            line[4] = '0'
        else:
            line[4] = line[4].replace(",", "")

        line[7] = cleanText(line[7])
        curs.execute(sql, (line[0], line[1], line[2], line[3],
                           line[4], line[5], line[6], line[7], line[8], line[9], line[10], '1'))
    print('CSV Insert')
    conn.commit()
    conn.close()
    f.close()
    print('OK')


db_input()
