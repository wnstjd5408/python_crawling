from tkinter.font import names
from traceback import print_exception
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import re
import time
import requests
import sys
import csv
from datetime import date, datetime
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from 네이버맛집검색 import one_scrolling
'''
========================부동산 크롤링 ==========================
 1. 네이버 부동산 모바일 버전을 불러옵니다.
'''
now = datetime.now()
nowDatetime = now.strftime('%Y-%m-%d(%H,%M,%S)')


def click_nolink_for_scrollDown(driver):
    try:
        plus = driver.find_element_by_css_selector(
            '#_article_list_tab_cd')
    except:
        driver.close()
        time.sleep(1)
    plus.click()
    time.sleep(0.1)
    for _ in range(50):
        time.sleep(0.2)
        plus.send_keys(Keys.PAGE_DOWN)

# CSV 파일로 저장


def save_to_csv(place, name):
    columns_name = ['매물명', '동', '거래유형', '가격', '유형', '전체면적', '실제면적',
                    '높이', '방향', '설명', '특징', '확인', '확인날짜', '링크', '크롤링날짜']
    CSV_file = pd.DataFrame(place)
    out_path = 'D:/파이썬 공부/web/crawling/부동산/%s(%s).csv' % (name, nowDatetime)
    # uniq = 1
    # while os.path.exists(out_path):
    #     out_path = 'D:/파이썬 공부/web/crawling/부동산/%s(%s).csv' % (
    #         place, uniq)
    #     uniq += 1

    CSV_file.to_csv(out_path, header=None,
                    index=False, encoding='utf-8-sig', mode='a')

# 들어가서 전체 아파트 전체 크로링


def one_scrolling(driver, place):
    html = driver.page_source
    num = 0
    a = 0
    stop = 0
    count = 0
    item_area_num = 1
    p = 0
    n = 1
    pl = []
    etc = ""
    soup = bs(html, 'html.parser')

    while True:
        num += 1

# //*[@id="_listContainer"]/div/div[3]/div[3]/div[1]/div[1]/a
# //*[@id="_listContainer"]/div/div[3]/div[1]/div[1]/div[1]/a
# //*[@id="_listContainer"]/div/div[3]/div[1]/div[5]/div[1]/a
        try:
            driver.find_element_by_xpath(
                f'//*[@id="_listContainer"]/div/div[3]/div[{item_area_num}]/div[{num}]/div/a'
            ).send_keys(Keys.CONTROL + "\n")
            stop = 0
            count += 1
        except:
            num = 0
            item_area_num += 1
            print("No search listclick")
            driver.execute_script('window.scrollTo(0, 400);')
            stop += 1
            print('item_area_num 의 수 : ', item_area_num)
            print('멈추는 횟수 : ', stop)
            if stop == 3:
                break
            continue

        driver.switch_to_window(driver.window_handles[-1])

        time.sleep(0.5)

        click_nolink_for_scrollDown(driver)
        print("창의 개수 : ", len(driver.window_handles))
        if(len(driver.window_handles) == 1):
            continue
        time.sleep(0.1)
        new_html = driver.page_source
        so = bs(new_html, 'html.parser')
        all = so.find_all('div', {'class': 'item_inner'})
        name = so.find('strong', {'class': 'detail_complex_title'}).text
        print('건물 이름 : ', name)
        count = 1
        for b in all:
            b_title = b.find('em', {'class': 'title_place'}).text  # 건물이름
            dong = b.find('span', {'class': 'title_building'}).text  # 건물 동호수
            info = b.find('div', {'class': "price_area"}).find(
                'span', {'class': 'type'}).text  # 건물에 대한 거래(매매,전세,월세)
            # print(count, '거래방법 :', info)
            price = b.find('div', {'class': "price_area"}).find_all(
                'strong')
            # print('개수 :', len(price))
            if len(price) == 2:
                price = price[0].text + '~' + price[1].text
            else:
                price = price[0].text
            # print('price : ', price)
            kinds = b.find('strong', {'class': 'type'}).text
            # print('kinds :', kinds)
            spec = b.find_all('span', {'class': 'spec'})
            area, height, wind = spec[0].text.split(',')

            supply_area, private_area = area.split('/')
            private_area = private_area.strip('㎡')
            # print('supply_area :', supply_area, 'private_area : ',
            #       private_area, 'height :', height, 'wind :', wind)
            if len(spec) == 2:
                etc = spec[1].text

            # print('etc: ', etc)
            tags = b.find('div', {'class': 'tag_area'})
            tag = []
            for _ in tags.find_all('em'):
                tag.append(_.string)
            tag = ','.join(tag)
            merit_area = b.find('div', {'class': 'merit_area'})
            merit_title = merit_area.find('em', {'class': 'label_title'}).text
            merit_date = merit_area.find('em', {'class': 'label_data'}).text
            # print(merit_title, ':', merit_date)
            link = b.find('a', {'class': 'item_link'})
            if(link != None):
                link = link['href']
                link = f"https://m.land.naver.com{link}"
            # print(link)
            now = datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            pl.append([b_title]+[dong]+[info] + [price] + [kinds] + [supply_area] + [private_area] + [height] + [wind] + [etc] + [tag] + [merit_title]
                      + [merit_date] + [link] + [nowDate])
            count += 1
        save_to_csv(pl, place)
        pl.clear()
        driver.close()
        driver.switch_to_window(driver.window_handles[0])


def first_page_scrolling(driver):
    while True:
        try:
            body = driver.find_element_by_css_selector(
                'body')
            time.sleep(0.3)
            for _ in range(100):
                time.sleep(0.2)
                body.send_keys(Keys.PAGE_DOWN)
            break
        except:
            driver.quit()
            time.sleep(1)


def driver_open(place):
    URL = "https://m.land.naver.com/search/result/"
    URL += place
    driver = webdriver.Chrome(
        executable_path="D:/파이썬 공부/web/crawling/chromedriver.exe"
    )
    driver.implicitly_wait(20)
    driver.get(URL)
    time.sleep(0.5)
    try:
        plus = driver.find_element_by_xpath(
            '//*[@id="_countContainer"]')
        plus.click()
        time.sleep(1)

    except:
        print("No search listClick")
    first_page_scrolling(driver)
    one_scrolling(driver, place)

    driver.quit()
# gubun = 4

# url = "https://m.land.naver.com/search/result/" + keyword
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; ; NCLIENT50_AAP0DCF421A65F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}

# res = requests.get(url, headers=headers)
# time.sleep(3)
# res.raise_for_status()
# soup = bs(res.text, "lxml")
# # print("res.text = ", type(res.text), res.text)
# # print("soup", type(soup))
# # print(url)

# filter1 = res.text.split("filter: {", 1)
# filter2 = filter1[1].split('},', 1)
# filter3 = filter2[0].lstrip().rstrip()


# regex = re.compile("{}(.*){}".format(re.escape("'"), re.escape("'")))
# filter_lists = regex.findall(filter3)
# print(filter_lists)


class MyApp(QWidget):
    qle = ""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        check = QPushButton('검색', self)
        grid = QGridLayout()
        self.setLayout(grid)
        self.qle = QLineEdit(self)
        check.pressed.connect(self.check_pressed)

        grid.addWidget(QLabel('지역검색 :'), 0, 0)
        grid.addWidget(self.qle, 0, 1)
        grid.addWidget(check, 0, 2)

        self.setWindowTitle('Crawling')
        self.setGeometry(800, 350, 400, 300)

        self.show()

    # def (self):
    #     driver_open(qle.text())

    def check_pressed(self):
        driver_open(self.qle.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
