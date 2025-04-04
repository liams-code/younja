# 블로그 글쓰기 페이지 진입 후 #mainFrame 셀렉터로 iframe 전환해
#.se-popup-button-cancel 셀렉터가 존재하면 클릭하고 없으면 넘어가
#.se-help-panel-close-button 셀렉터가 존재하면 클릭하고 없으면 넘어가

#.se-section-documentTitle 셀렉터를 클릭 후 "제목 테스트" 라고 입력해
#.se-section-text 셀렉터를 클릭후 "안녕하세요 내용을 입력하고 있습니다." 를 5줄 입력해

#.save_btn__bzc5B 셀렉터를 클릭해

#모든 입력은 send_keys를 사용하지 말고 actionchains 로 0.01초에 1글자씩 입력해


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time


driver = webdriver.Chrome()

# 네이버 로그인 페이지 접속
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
    pass  # 팝업이 없으면 넘어감

# 도움말 패널 닫기 버튼이 있다면 클릭
try:
    help_close_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.se-help-panel-close-button'))
    )
    help_close_button.click()
    time.sleep(1)
except:
    pass  # 도움말 패널이 없으면 넘어감

# 제목 입력
title_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.se-section-documentTitle'))
)
title_element.click()
actions = ActionChains(driver)
for char in "제목 테스트":
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
for _ in range(5):
    for char in "안녕하세요 내용을 입력하고 있습니다.":
        actions.send_keys(char)
        actions.pause(0.1)
    actions.send_keys(Keys.ENTER)
    actions.pause(0.5)
actions.perform()
time.sleep(2)

# 저장 버튼 클릭
save_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.save_btn__bzc5B'))
)
driver.execute_script("arguments[0].click();", save_button)
time.sleep(10)

driver.quit()

