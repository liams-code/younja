from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pyperclip
import pandas as pd
import os
import traceback
# 봇 확인 창 없애기
#import pyautogui #account > div.MyView-module__my_menu___eF24q.MyView-module__is_open____qWM1 > div > div > ul > li:nth-child(3) > a > span.MyView-module__item_text___VTQQM
def write_blog_post(title, content):
    try:
        # 블로그 글쓰기 페이지 접속
        print("블로그 글쓰기 페이지로 이동 중...")
        driver.get('https://blog.naver.com/liamsss?Redirect=Write')
        time.sleep(5)  # 페이지 로딩을 위해 충분한 시간 대기
        
        # iframe 확인
        print("iframe 찾는 중...")
        try:
            iframe = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainFrame'))
            )
            print("iframe 찾음, 전환 시도 중...")
            driver.switch_to.frame(iframe)
            print("iframe 전환 성공")
        except TimeoutException:
            print("iframe을 찾을 수 없습니다. 현재 페이지 소스:")
            print(driver.page_source[:500])  # 페이지 소스의 일부만 출력
            return False
        
        # 팝업 취소 버튼이 있다면 클릭
        try:
            cancel_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.se-popup-button-cancel'))
            )
            cancel_button.click()
            print("팝업 닫기 성공")
            time.sleep(1)
        except:
            print("팝업이 없거나 닫을 수 없습니다.")
            pass

        # 도움말 패널 닫기 버튼이 있다면 클릭
        try:
            help_close_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.se-help-panel-close-button'))
            )
            help_close_button.click()
            print("도움말 패널 닫기 성공")
            time.sleep(1)
        except:
            print("도움말 패널이 없거나 닫을 수 없습니다.")
            pass

        # 제목 입력
        print("제목 입력 시도 중...")
        try:
            title_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.se-section-documentTitle'))
            )
            title_element.click()
            actions = ActionChains(driver)
            for char in title:
                actions.send_keys(char)
                actions.pause(0.1)
            actions.perform()
            print("제목 입력 성공")
            time.sleep(1)
        except TimeoutException:
            print("제목 입력란을 찾을 수 없습니다.")
            return False

        # 본문 입력
        print("본문 입력 시도 중...")
        try:
            content_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.se-section-text'))
            )
            content_element.click()
            actions = ActionChains(driver)
            # 내용이 너무 길면 일부만 입력
            content_to_input = content[:5000] if len(content) > 5000 else content
            for char in content_to_input:
                actions.send_keys(char)
                actions.pause(0.02)  # 0.01초에서 0.03초로 증가
            actions.perform()
            print("본문 입력 성공")
            time.sleep(2)
        except TimeoutException:
            print("본문 입력란을 찾을 수 없습니다.")
            return False

        # 저장 버튼 클릭
        print("저장 버튼 클릭 시도 중...")
        try:
            save_button = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.save_btn__bzc5B'))
            )
            driver.execute_script("arguments[0].click();", save_button)
            print("저장 버튼 클릭 성공")
            time.sleep(10)
            return True
        except TimeoutException:
            print("저장 버튼을 찾을 수 없습니다.")
            return False
            
    except Exception as e:
        print(f"글 작성 중 오류 발생: {e}")
        traceback.print_exc()
        return False

# 엑셀 파일 경로 확인
excel_path = 'blogauto/data.xlsx'
if not os.path.exists(excel_path):
    excel_path = 'data.xlsx'  # 상대 경로로도 시도
    if not os.path.exists(excel_path):
        print(f"엑셀 파일을 찾을 수 없습니다. 현재 작업 디렉토리: {os.getcwd()}")
        exit(1)

# 엑셀 파일 읽기
print(f"엑셀 파일 읽기 시도: {excel_path}")
df = pd.read_excel(excel_path)  # 헤더 자동 감지
print(f"엑셀 파일 읽기 성공. 총 {len(df)} 행 데이터 로드됨")
print(f"데이터 미리보기: \n{df.head()}")  # 데이터 구조 확인
print(f"열 이름: {df.columns.tolist()}")

# 데이터가 비어있는지 확인 - 실제 데이터가 있는지 확인하는 방식으로 수정
if len(df) < 1:  # 완전히 비어있는 경우만 종료
    print("엑셀 파일에 데이터가 없습니다.")
    exit(1)
else:
    print(f"총 {len(df)} 행의 데이터가 발견되었습니다.")

#브라우저 꺼짐 방지
options = Options()
options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 없애기
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(options=options)
url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"

# 웹페이지 해당주소로 이동
driver.get(url)
driver.implicitly_wait(5)
driver.maximize_window() #화면 최대화
time.sleep(1)

# """
# <input id="query" name="query" type="text" title="검색어 입력" maxlength="255" class="input_text" tabindex="1" accesskey="s" style="ime-mode:active;" autocomplete="off" placeholder="검색어를 입력해 주세요." onclick="document.getElementById('fbm').value=1;" value="" data-atcmp-element="">
# """

id = driver.find_element(By.CSS_SELECTOR, "#id").send_keys("liamsss")

time.sleep(1)
#pw

driver.find_element(By.CSS_SELECTOR, "#pw").send_keys("ksw2003357^^")
time.sleep(1)

driver.find_element(By.CSS_SELECTOR, "#log\.login > span").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#qrcode > span > span").click()
time.sleep(9)

# 네이버 블로그 페이지로 직접 접속
driver.get('https://blog.naver.com/liamsss')
time.sleep(3)

# 블로그 글쓰기 페이지로 직접 이동하지 않고 UI를 통해 접근
try:
    print("블로그 글쓰기 버튼 찾는 중...")
    # 다양한 선택자 시도
    selectors = [
        "a.btn_write",  # 일반적인 글쓰기 버튼
        "a.btn_edit",   # 편집 버튼
        "a[href*='Redirect=Write']",  # Write 파라미터가 있는 링크
        "a.link_write"  # 다른 가능한 클래스
    ]
    
    for selector in selectors:
        try:
            write_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            print(f"글쓰기 버튼 찾음: {selector}")
            write_button.click()
            print("글쓰기 버튼 클릭 성공")
            time.sleep(5)
            break
        except:
            continue
    else:  # for 루프가 break 없이 끝난 경우
        print("UI를 통한 글쓰기 버튼을 찾지 못했습니다. URL로 직접 접근합니다.")
        driver.get('https://blog.naver.com/liamsss?Redirect=Write')
        time.sleep(5)
        
except Exception as e:
    print(f"블로그 글쓰기 페이지 접근 중 오류: {e}")
    driver.get('https://blog.naver.com/liamsss?Redirect=Write')
    time.sleep(5)

# 현재 URL 확인
current_url = driver.current_url
print(f"현재 URL: {current_url}")

# 엑셀의 각 행에 대해 블로그 글 작성
print("블로그 글 작성 시작...")
success_count = 0
fail_count = 0

# 열 확인
columns = df.columns.tolist()
print(f"사용 가능한 열: {columns}")

# 첫 번째, 두 번째 열 이름 (제목과 내용에 해당하는 열) 가져오기
title_column = columns[0] if len(columns) > 0 else None
content_column = columns[1] if len(columns) > 1 else None

if title_column is None or content_column is None:
    print("제목과 내용을 포함하는 열을 찾을 수 없습니다.")
    exit(1)

print(f"제목 열: {title_column}, 내용 열: {content_column}")

# 각 행 처리
for index, row in df.iterrows():
    try:
        # 데이터 확인 및 디버깅
        print(f"행 {index} 데이터 처리 중...")
        
        # 제목과 내용이 있는지 확인 - 열 이름으로 접근
        if pd.isna(row[title_column]) or pd.isna(row[content_column]):
            print(f"행 {index}에 빈 데이터가 있습니다. 건너뜁니다.")
            continue
            
        title = str(row[title_column])  # 제목 열
        content = str(row[content_column])  # 내용 열
        
        print(f"글 작성 시도 중 ({index+1}/{len(df)}): {title[:30]}...")  # 제목 일부만 출력
        result = write_blog_post(title, content)
        
        if result:
            print(f"글 작성 성공: {title[:30]}...")
            success_count += 1
        else:
            print(f"글 작성 실패: {title[:30]}...")
            fail_count += 1
            
        time.sleep(5)  # 다음 글 작성 전 대기
    except Exception as e:
        print(f"처리 중 오류 발생: {e}")
        traceback.print_exc()
        fail_count += 1
        continue

print(f"작업 완료: 성공 {success_count}건, 실패 {fail_count}건")
driver.quit() 
