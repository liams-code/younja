#아래 조건에 맞는 엑셀기반자동글쓰기.py 파일을 생성하고 실행해
#1. @블로그글쓰기.py @gemini_test.py  파일을 분석해
#2. data.xlsx 파일의 2행부터 마지막행까지 반복하며 a열 제목, b열 내용을 읽어
#3. 네이버 로그인 후 각 행별 제목, 내용으로 글을 작성하고 저장 버튼을 눌러

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import pandas as pd
import time

def write_blog_post(title, content):
    # 블로그 글쓰기 페이지 접속
    driver.get('https://blog.naver.com/GoBlogWrite.naver')
    time.sleep(3)

    # iframe으로 전환
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainFrame'))
    )
    driver.switch_to.frame(iframe)

    # 팝업 취소 버튼이 있다면 클릭
    try:
        cancel_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.se-popup-button-cancel'))
        )
        cancel_button.click()
        time.sleep(1)
    except:
        pass

    # 도움말 패널 닫기 버튼이 있다면 클릭
    try:
        help_close_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.se-help-panel-close-button'))
        )
        help_close_button.click()
        time.sleep(1)
    except:
        pass

    # 제목 입력
    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.se-section-documentTitle'))
    )
    title_element.click()
    actions = ActionChains(driver)
    for char in title:
        actions.send_keys(char)
        actions.pause(0.1)
    actions.perform()
    time.sleep(1)

    # 본문 입력
    content_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.se-section-text'))
    )
    content_element.click()
    actions = ActionChains(driver)
    for char in content:
        actions.send_keys(char)
        actions.pause(0.01)
    actions.perform()
    time.sleep(2)

    # 저장 버튼 클릭
    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.save_btn__bzc5B'))
    )
    driver.execute_script("arguments[0].click();", save_button)
    time.sleep(10)

# 엑셀 파일 읽기
df = pd.read_excel('data.xlsx', header=0)  # 첫 번째 행을 열 이름으로 사용

# 네이버 로그인
driver = webdriver.Chrome()
driver.get('https://nid.naver.com/nidlogin.login')

# 로그인 정보
naver_id = 'yunjadong'
naver_pw = 'test1111'

# ID 입력
id_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'id'))
)
id_input.click()
pyperclip.copy(naver_id)
id_input.send_keys(Keys.CONTROL + 'v')
time.sleep(1)

# 비밀번호 입력
pw_input = driver.find_element(By.ID, 'pw')
pw_input.click()
pyperclip.copy(naver_pw)
pw_input.send_keys(Keys.CONTROL + 'v')
time.sleep(1)

# 로그인 버튼 클릭
login_button = driver.find_element(By.ID, 'log.login')
login_button.click()
time.sleep(2)

# 엑셀의 각 행에 대해 블로그 글 작성
for index, row in df.iloc[1:].iterrows():
    title = str(row.iloc[0])  # 첫 번째 열의 제목
    content = str(row.iloc[1])  # 두 번째 열의 내용
    
    print(f"글 작성 중: {title}")
    write_blog_post(title, content)
    time.sleep(5)  # 다음 글 작성 전 대기

driver.quit() 
