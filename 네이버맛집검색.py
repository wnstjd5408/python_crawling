from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os
import sys
import re
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import logging

# 페이지 들어간 후에 클릭하는거
now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d(%H,%M,%S)')


def click_nolink_for_scrollDown(driver):
    while True:
        try:

            # time.sleep(1)

            # plus = driver.find_element_by_css_selector(
            #     "#app-root > div > div > div > div.place_fixed_maintab > div > div > div > div > div > div > div > div > a:nth-child(1)")

            # plus.click()
            # print('클릭plus', plus)
            time.sleep(1)
            # 시간 클릭
            element = driver.find_element_by_css_selector(
                '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._2KHqk > div > a')
            # app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._2KHqk > div > a
            # app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._2KHqk > div > a
            print('클릭: ', element)

            element.click()
            # driver.execute_script(
            #     "arguments[0].setAttribute('aria-expanded', True)", pl)
            time.sleep(0.5)
            for i in range(10):
                time.sleep(0.2)
                driver.find_element_by_css_selector(
                    "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(0.4)

        except:
            plus = None
            pl = None
            print('클릭이 안됨')
        finally:
            break


# 파일을 csv 파일에 저장


def save_to_place(name, place):
    f = open(name, 'w+', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    writer.writerow(['가게명', '가게정보', '평점', '방문자리뷰',
                     '블로그리뷰', '위치', '근처 지하철역', '시간', 'SNS 사이트', '이미지 URL', '등록날짜'])
    for i in place:
        writer.writerow(list(i.values()))
    return

# 이름명이 동일한 csv 파일명을 바꾸어주는 메서드


def check(file_name):
    file_ext = '.csv'
    output_path = 'D:/파이썬 공부/web/crawling/place/%s(%s)%s' % (
        file_name, nowDatetime, file_ext)
    # uniq = 1
    # while os.path.exists(output_path):

    #     output_path = 'D:/파이썬 공부/web/crawling/place/%s(%d)%s' % (
    #         file_name, uniq, file_ext)
    #     uniq += 1
    return output_path


# body라는 것을 find_element_by_css_selector로 찾고나서 ul을 한 번 눌려준다
def all_scrolling(driver):
    while True:
        try:
            body = driver.find_element_by_css_selector("body")
            time.sleep(0.3)
            for i in range(500):  # 첫페이지의 길이만큼이나 안에 있는 숫자를 늘려주고 줄여줄 수 있다.
                time.sleep(0.2)
                body.send_keys(Keys.PAGE_DOWN)
            break
        except:
            driver.refresh()
            time.sleep(1)


def driver_open(place):
    URL = "https://m.place.naver.com/restaurant/list?x=129.1023126&y=35.1385167&query="
    URL = URL + place
    driver = webdriver.Chrome(
        executable_path="D:/파이썬 공부/web/crawling/chromedriver.exe")
    driver.implicitly_wait(20)
    driver.get(URL)

    all_scrolling(driver)

    html = driver.page_source
    place = check(place)
    one_scrolling(driver, html, place)

    driver.quit()


def one_scrolling(driver, ht, plus):
    subway_location = ""
    opentime = []
    place = []
    num = 0
    stop = 0
    count = 0
    so = bs(ht, 'html.parser')

    while True:
        opentime.clear()
        num += 1
        score = ""
        blog = ""
        visit = ""
        try:
            # find_element_by_xpath로 위치를 찾아서 클릭을 해준다
            driver.find_element_by_xpath(
                f'//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[{num}]/div[1]/a[1]').send_keys(Keys.CONTROL + "\n")
            # driver.find_element_by_css_selector(
            #     f"#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({num}) > div.Ow5Yt > a:nth-child(1)").send_keys(Keys.CONTROL + "\n")
            stop = 0
            count += 1
        except:
            # 찾지를 못하면 stop의 숫자를 늘려주고 5가 되면 break문을 걸어서 종료
            print("No search listclick")
            driver.execute_script('window.scrollTo(0, 400);')
            stop += 1
            print('멈추는 횟수 : ', stop)
            if stop == 3:
                break
            continue

        # 열어준 탭이동을 합니다

        driver.switch_to_window(driver.window_handles[-1])

        time.sleep(0.5)

        click_nolink_for_scrollDown(driver)
        print("창의 개수 : ", len(driver.window_handles))
        if(len(driver.window_handles) == 1):
            continue
        time.sleep(0.1)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        try:
            im = soup.find('div', {'class': 'cb7hz'})['style']
        except:
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            continue
        else:
            found = im.find('(')
            imagefirst = im[found+2::]
            backfound = imagefirst.find(')')
            imageurl = imagefirst[0: backfound-1]
            # 이미지 검색
            name = soup.find('span', {'class': '_3XamX'}).text
            info = soup.find('span', {'class':  '_3ocDE'}).text
            # 점수, 방문자, 블로그 리뷰
            avg = soup.find('div', {'class': '_20Ivz'})
            score_visit_blog = avg.find_all('span',  {'class': '_1Y6hi'})

            if len(score_visit_blog) == 1:
                if '방문자리뷰' in score_visit_blog[0].find('a').text:
                    visit = score_visit_blog[0].find('em').text
                elif '블로그리뷰' in score_visit_blog[0].find('a').text:
                    blog = score_visit_blog[0].find('em').text
            elif len(score_visit_blog) == 2:
                try:
                    if score_visit_blog[0].find('span', {'class': 'place_blind'}).text == '별점':
                        if "블로그리뷰" in score_visit_blog[1].find('a').text:
                            score = score_visit_blog[0].find('em').text
                            blog = score_visit_blog[1].find('em').text
                        else:
                            score = score_visit_blog[0].find('em').text
                            visit = score_visit_blog[1].find('em').text
                except:
                    visit = score_visit_blog[0].find('em').text
                    blog = score_visit_blog[1].find('em').text

            elif len(score_visit_blog) == 3:
                score = score_visit_blog[0].find('em').text
                visit = score_visit_blog[1].find('em').text
                blog = score_visit_blog[2].find('em').text

            data = soup.find_all('div', {'class': '_1h3B_'})
            location = data[0].find('span', {'class': '_2yqUQ'}).text
            try:
                subway_location = data[0].find('div', {'class': '_2P6sT'})
                # subway_number = subway_location.find(
                #     'span', {'class': '_12Coj'}).text
                subway_location = subway_location.text
            except:
                subway_location = None
            # 영엽시간 검색
            try:
                timelen = soup.find_all('div', {'class': '_1h3B_'})[1].find_all(
                    'div', {'class': '_2ZP3j'})
                print('갯수  :',  len(timelen))
                if len(timelen) == 1:
                    print(timelen[0].text)
                    tt = timelen[0].text
                else:
                    for i in timelen[1::]:
                        try:

                            etc = i.find('span', {'class': '_20pEw'}).text
                        except:
                            etc = i.find('span', {'class': '_20pEw'}).text

                        opentime.append(etc)

                    tt = ",".join(opentime)
            except:
                tt = None
                # place를 리스트에 딕셔너리 형태로 저장을 시킨다
            try:
                sns_site = soup.find('div', {'class': '_14J59'}).text
            except:
                sns_site = None
            print('sns_site : ', sns_site)
            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            place.append({"name": name, "info": info, "score": score, "visit": visit, "blog": blog,
                          "location": location, "subway_location": subway_location, "clock":  tt, "sns_site": sns_site, "imageurl": imageurl, "nowDate": nowDate})
            print(f'{count} : {name}')
            save_to_place(plus, place)
            # driver를 종료하고 전에있던 탭을 켜줍니다.
            driver.close()
            driver.switch_to_window(driver.window_handles[0])


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
