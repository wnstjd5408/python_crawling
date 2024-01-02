import csv
import datetime
import sys
import time
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup as bs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

# 페이지 들어간 후에 클릭하는거
now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d(%H,%M,%S)')


# 시간 클릭 하는 메서드
def click_nolink_for_scrollDown(driver):
    while True:
        try:
            time.sleep(1)
            # 시간 클릭
            element =driver.find_element(By.XPATH, f'//*[@id="app-root"]/div/div/div/div[5]/div/div[2]/div[1]/div/div[2]/div/a')
            # driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');",element)
            # print("aria-expanded 수정",element.get_attribute('aria-expanded'))

            element.click()
            """ 
            클릭 후에 스크롤링 주석처리 
            """
            time.sleep(0.1)

        except NoSuchElementException as e:
            print('클릭이 안됨 :', e)
            pass
        finally:
            break


# 파일을 csv 파일에 저장


def save_to_place(name, place):
    f = open(name, 'a', newline='', encoding='utf-8-sig')
    writer = csv.writer(f)

    print("save_to_place 넘어가나요.")

    writer.writerow(place.values())

    return

# 이름명이 동일한 csv 파일명을 바꾸어주는 메서드


def file_path(file_name):
    file_ext = '.csv'
    output_path = '/Users/dustion/Desktop/모두싸인/django/django crawling/Food_store/%s(%s)%s' % (
        file_name, nowDatetime, file_ext)
    
    f = open(output_path, 'w', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    header_list = ['가게명', '가게정보', '평점', '방문자리뷰',
                     '블로그리뷰', '위치', '근처 지하철역', '시간', 'SNS 사이트', '이미지 URL', '등록날짜']
    writer.writerow(header_list)

    return output_path
    

# body라는 것을 find_element_by_css_selector로 찾고나서 ul을 한 번 눌려준다
def all_scrolling(driver):
    while True:
        try:
            body = driver.find_element_by_xpath(f'//*[@id="_place_portal_root"]/div/a/svg/path').click()
            

            time.sleep(0.3)
            for _ in range(300):  # 첫페이지의 길이만큼이나 안에 있는 숫자를 늘려주고 줄여줄 수 있다.
                time.sleep(0.2)
                body.send_keys(Keys.PAGE_DOWN)
            break
        except:
            driver.refresh()
            time.sleep(1)


def start_crawling(place):
    URL = "https://m.place.naver.com/restaurant/list?x=129.1023126&y=35.1385167&query=" + place
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

    driver.implicitly_wait(20)
    driver.get(URL)

    # all_scrolling(driver)
    html = driver.page_source

    out_path = file_path(place)
    collect_data(driver,  out_path)
    driver.quit()

# 자세한 페이지 데이터 수집
    
# 검색 페이지에서 상세 페이지로 이동하는 함수
def navigate_to_detail(driver, num):
    try:
        target = driver.find_element(By.XPATH, f'//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[{num}]/div[1]/a[1]')
        target.send_keys(Keys.COMMAND + "\n")
        return True
    except NoSuchElementException:
        print("No search listclick")
        driver.execute_script('window.scrollTo(0, 400);')
        return False

# 검색 페이지에서 데이터 수집하는 함수
def collect_data(driver, out_path):
    num = 0
    while True:
        num += 1
        stop = 0
        if not navigate_to_detail(driver, num):
            if (stop == 3):
                break
            stop += 1
            continue
            
        driver.switch_to.window(driver.window_handles[-1])
        # 데이터 수집 후 데이터 저장
        place_data = extract_data(driver)
        print(f"{num}:",place_data["name"])
        save_to_place(out_path, place_data)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def extract_data(driver):
        visit = ""
        score = ""
        blog = ""

        click_nolink_for_scrollDown(driver)
        print("창의 개수 : ", len(driver.window_handles))
        if(len(driver.window_handles) == 1):
            return
        time.sleep(0.1)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        try:
            im = soup.find('div', {'class': 'K0PDV'})['style']
        except:
            print('이미지 없음')
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            return
        else:
            found = im.find('(')
            imagefirst = im[found+2::]
            backfound = imagefirst.find(')')
            imageurl = imagefirst[0: backfound-1]
            # 이미지 검색
            name = soup.find('span', {'class': 'Fc1rA'}).text
            info = soup.find('span', {'class':  'DJJvD'}).text
            # 점수, 방문자, 블로그 리뷰
            avg = soup.find('div', {'class': 'dAsGb'})
            score_visit_blog = avg.find_all('span',  {'class': 'PXMot'})
            if len(score_visit_blog) == 1:
                review1 = score_visit_blog[0].text
                if '방문자리뷰' in score_visit_blog[0].find('a').text:
                    visit = review1
                elif '블로그리뷰' in score_visit_blog[0].find('a').text:
                    blog = review1
            elif len(score_visit_blog) == 2:
                review1 = score_visit_blog[0].text
                review2 = score_visit_blog[1].text
                try:
                    if score_visit_blog[0].find('span', {'class': 'place_blind'}).text == '별점':
                        if "블로그리뷰" in score_visit_blog[1].find('a').text:
                            score = review1
                            blog = review2
                        else:
                            score = review1
                            visit = review2
                except:
                    visit = review1
                    blog = review2

            elif len(score_visit_blog) == 3:
                score = score_visit_blog[0].text
                visit = score_visit_blog[1].text
                blog = score_visit_blog[2].text
            # print(f'점수 : {score} , 방문자리뷰 : {visit}, 블로그 리뷰 : {blog}')
            data = soup.find_all('div', {'class': 'O8qbU'})
            location = data[0].find('span', {'class': 'LDgIH'}).text
            subway_location = data[0].find('div', {'class': 'nZapA'}).text if data[0].find('div', {'class': 'nZapA'}) else None

            # 영엽시간 검색
            try:
                time.sleep(0.5)
                timelen = data[1].find_all('div', {'class': 'w9QyJ'})
                print('갯수  :',  len(timelen))
                if len(timelen) == 1:
                    tt = timelen[0].text
                else:
                    opentime = []
                    for i in timelen[1::]:
                        element_A_cdD = i.find('span', {'class': 'A_cdD'})
                        if element_A_cdD:
                            text_time = element_A_cdD.text
                        else:
                            text_time = i.find('span', {'class': 'h1ryO'}).text
                        print("text_time : ",text_time)
                        opentime.append(text_time)
                    # opentime = [i.find('span', {'class': 'A_cdD'}).text for i in timelen[1::]]
                    tt = ",".join(opentime)
                    opentime.clear()

            except:
                print("click NO")
                tt = None
                # place를 리스트에 딕셔너리 형태로 저장을 시킨다
            sns_site = soup.find('div', {'class': 'jO09N'}).text if soup.find('div', {'class': 'jO09N'}) else None
            print('sns_site : ', sns_site)
            nowDate = now.strftime('%Y-%m-%d')
            print({"name": name, "info": info, "score": score, "visit": visit, "blog": blog,
                          "location": location, "subway_location": subway_location, "clock":  tt, "sns_site": sns_site, "imageurl": imageurl, "nowDate": nowDate})
            return {"name": name, "info": info, "score": score, "visit": visit, "blog": blog,
                          "location": location, "subway_location": subway_location, "clock":  tt, "sns_site": sns_site, "imageurl": imageurl, "nowDate": nowDate}
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

    def check_pressed(self):
        start_crawling(self.qle.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())




