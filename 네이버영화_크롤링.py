from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os


# def all_scrolling(driver):
#     while True:
#         try:
#             body = driver.find_element_by_css_selector("body")
#             time.sleep(0.3)
#             driver.find_element_by_css_selector(
#                 '#content > div.article > div:nth-child(1) > div.lst_wrap > ul').click()
#         #
#             for i in range(50):  # 첫페이지의 길이만큼이나 안에 있는 숫자를 늘려주고 줄여줄 수 있다.
#                 time.sleep(0.2)
#                 body.send_keys(Keys.PAGE_DOWN)
#             break
#         except:
#             driver.refresh()
#             time.sleep(1)


def click_nolink_for_scrollDown(driver):
    while True:
        try:
            for i in range(5):
                time.sleep(0.2)
                driver.find_element_by_css_selector(
                    "body").send_keys(Keys.PAGE_DOWN)
            break
        except:
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            break


def check(file_name):
    file_ext = '.csv'
    output_path = 'D:/파이썬 공부/web/crawling/movie/%s%s' % (
        file_name, file_ext)
    uniq = 1
    while os.path.exists(output_path):
        output_path = 'D:/파이썬 공부/web/crawling/movie/%s(%d)%s' % (
            file_name, uniq, file_ext)
        uniq += 1
    return output_path


def save_to_place(name, place):
    f = open(name, 'w+', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    for i in place:
        writer.writerow(list(i.values()))
    return


URL = "https://movie.naver.com/movie/running/current.naver"
driver = webdriver.Chrome(
    executable_path="D:/파이썬 공부/web/crawling/chromedriver.exe")
driver.implicitly_wait(20)
driver.get(URL)

file_name = check("영화리스트")
num = 0
stop = 0
count = 0
movie = []
while True:
    num += 1
    try:
        driver.find_element_by_xpath(
            f'//*[@id="content"]/div[1]/div[1]/div[3]/ul/li[{num}]/dl/dt/a').send_keys(Keys.CONTROL + "\n")
        count += 1
        stop = 0
    except:
        print("No search listclick")
        driver.execute_script('window.scrollTo(0, 400);')
        time.sleep(0.5)
        stop += 1
        print('멈추는 횟수 : ', stop)
        if stop == 3:
            break
        continue
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(0.5)
    click_nolink_for_scrollDown(driver)
    print("창의 개수 :  ", len(driver.window_handles))
    if(len(driver.window_handles) == 1):
        continue
    time.sleep(0.1)
    html = driver.page_source
    so = bs(html, 'html.parser')
    info = so.find('div', {'class': 'mv_info_area'})
    title = info.find('h3', {'class': 'h_movie'}).find_all('a')[0].text
    image = so.find_all('div', {'class': 'poster'})
    image_url = image[1].find('img')['src']
    info_sec = info.find(
        'dl', {'class': 'info_spec'}).find_all('dd')
    if len(info_sec) == 3 or len(info_sec) == 4:
        count -= 1
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        continue
    span = info_sec[0].find_all('span')
    if len(span) == 3:
        count -= 1
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        continue
    result = span[0].find_all('a')
    res = [i.text for i in result]
    grec = ','.join(res)
    result = span[1].find_all('a')
    c_r = [i.text for i in result]
    country = ','.join(c_r)
    runningtime = span[2].text
    open_movie = span[3].text.strip().replace("\n", "").replace(" ", "")[0:10]
    director = info_sec[1].text
    actor = info_sec[2].text.rstrip("더보기")
    age = info_sec[3].find('a').text
    try:
        content = so.find('p', {'class': 'con_tx'}).text
    except:
        content = ""
    movie.append({"index": count, "title": title, "open_movie": open_movie, "director": director, "actor": actor, "grec": grec,
                  "country": country, "age": age, "runningtime": runningtime, "content": content, "img_url": image_url})
    print(f'{count} : {title}')
    save_to_place(file_name, movie)
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
driver.close()
