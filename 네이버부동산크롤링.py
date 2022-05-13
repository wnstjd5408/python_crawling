from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


file_ext = '.csv'
URL_link = []
# link = "https://m.land.naver.com/complex/info/109359?tradTpCd=A1:B1:B2:B3&ptpNo=&bildNo=&articleListYN=Y"


def click_nolink_for_scrollDown(driver):
    url = driver.current_url
    while True:
        try:
            body = driver.find_element_by_css_selector(
                '#_article_list_tab_cd')
        except:
            driver.refresh()
            time.sleep(1)
        body.click()
        time.sleep(0.1)
        if url == driver.current_url:
            break
        else:
            driver.execute_script("window.history.go(-1)")

    time.sleep(0.1)
    for i in range(50):
        time.sleep(0.2)
        body.send_keys(Keys.PAGE_DOWN)


def check(file_name):
    output_path = 'D:/파이썬 공부/web/crawling/부동산/%s%s' % (
        file_name, file_ext)
    uniq = 1
    while os.path.exists(output_path):
        output_path = 'D:/파이썬 공부/web/crawling/부동산/%s(%d)%s' % (
            file_name, uniq, file_ext)
        uniq += 1
    return output_path


def save_to_land(name, land):
    f = open(name, 'w+', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    writer.writerow(['번호', '매물명', '동', '거래유형', '가격', '유형', '전체면적', '실제면적',
                     '높이', '방향', '설명', '제공', '확인날짜', '확인', '건물특징', '링크'])
    for i in land:
        writer.writerow(list(i.values()))
    return


def csv_save(html):
    place = []
    soup = bs(html, 'html.parser')
    all = soup.find_all('div', {'class': 'item_inner'})

    name = soup.find('strong', {'class': 'detail_complex_title'}).text
    name = check(name)
    num = 0
    for apt in all:
        a = 0
        p = 0
        n = 1
        num += 1
        link = ""
        etc = []
        etc2 = ""
        characteristic = ""
        title = apt.find('em', {'class': 'title_place'}).text
        dong = apt.find('span', {'class': 'title_building'}).text
        info = apt.find('div', {'class': "price_area"}).find(
            'span', {'class': 'type'}).text
        price = apt.find('div', {'class': "price_area"}
                         ).find('strong').text

        if info == '매매':
            if '억' in price:
                price = price.replace('억', '00000000')
                if ',' in price:
                    price = price.replace(',', '')

                price = price.split()

                for x in price:
                    if(n == 2):
                        x = x + "0000"
                    p += int(x)
                    n += 1

            else:
                if ',' in price:
                    price = price.replace(',', '')

                    price = price + "0000"
                    p += int(price)

        elif info == '전세':
            if '억' in price:
                price = price.replace('억', '00000000')
                if ',' in price:
                    price = price.replace(',', '')

                price = price.split()

                for x in price:
                    if(n == 2):
                        x = x + "0000"
                    p += int(x)
                    n += 1

            else:
                if ',' in price:
                    price = price.replace(',', '')

                    price = price + "0000"
                    p += int(price)
        else:
            p = price
        kinds = apt.find('strong', {'class': 'type'}).text
        spec = apt.find_all('span', {'class': 'spec'})
        etc2 = apt.find('em', {'class': 'label_data'}).text
        etc3 = apt.find('em', {'class': 'label_title'}).text
        etc4 = apt.find('div', {'class': 'tag_area'}).text
        for s in spec:
            a += 1
            if a == 2:
                characteristic = s.text
                break
            area, height, wind = s.text.split(',')

        source = apt.find_all('span', {'class':  'agent_info'})
        for i in source:
            # print(i.text)
            etc.append(i.text)

        etc = "/".join(etc)
        supply_area, private_area = area.split('/')
        private_area = private_area.strip('㎡')
        spec = apt.find('span', {'class': 'spec'}).text
        link = apt.find('a', {'class': 'item_link'})
        if(link != None):
            link = link['href']
            link = f"https://m.land.naver.com{link}"
        place.append({'num ': num, "title": title, "dong": dong, "info": info, "price": p, "kinds": kinds,
                      "supply_area": supply_area, "private_area":  private_area, "height": height,
                      "wind": wind, "characteristic": characteristic, "etc": etc, "etc2": etc2, "etc3": etc3, "etc4": etc4, "link": link})
        print(num)
        save_to_land(name, place)


def driver_open(URL):
    driver = webdriver.Chrome(
        executable_path="D:/파이썬 공부/web/crawling/chromedriver.exe")
    driver.implicitly_wait(14)
    driver.get(URL)
    time.sleep(2)

    click_nolink_for_scrollDown(driver)

    html = driver.page_source

    driver.close()
    csv_save(html)


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

        grid.addWidget(QLabel('URL:'), 0, 0)
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
