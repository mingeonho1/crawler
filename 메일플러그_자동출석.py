import time
import slack_sdk
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from 크롬드라이버_자동_업데이트 import chrome_driver

driver = chrome_driver()

# DB에서 가져와도 됨
login_info_list = [
    {'id': 'test@company.co.kr', 'pw': 'test1234'},
    {'id': 'test2@company.co.kr', 'pw': 'test1234'},
    {'id': 'test3@company.co.kr', 'pw': 'test1234'}]

SLACK_TOKEN = 'test-test-test'
SLACK_CHANNEL = '#test'


# slack Bot 도입
def slack_bot(message):
    client = slack_sdk.WebClient(token=SLACK_TOKEN)
    client.chat_postMessage(channel=SLACK_CHANNEL,
                            text=message)


def driver_sleep(n=0.5):
    driver.implicitly_wait(10)
    time.sleep(n)


def id_security(user_id):
    _id = user_id.split('@')[0]
    _id = _id[:-2] + '**'
    return _id


def login(user_id, user_pw):
    try:
        driver.get('https://m109.mailplug.com/member/login')
        driver_sleep()
        driver.find_element(By.ID, 'login_input').send_keys(user_id)
        driver_sleep()
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/input').click()
        driver_sleep()
        driver.find_element(By.ID, 'cpw').send_keys(user_pw)
        driver_sleep()
        driver.find_element(By.XPATH, '//*[@id="btnlogin"]').click()
        driver_sleep()
        slack_bot(f"{id_security(user_id)}님 로그인 성공.")
    except Exception as e:
        slack_bot(f"{id_security(user_id)}님 로그인 실패.")


def logout():
    driver.find_element(By.XPATH, '//*[@id="profile_detail"]/button/img').click()
    driver_sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-app"]/div[2]/div[2]/div[2]/ul/li[2]').click()
    driver_sleep(1)
    driver.delete_all_cookies()
    print('로그아웃 성공 !')


def main():
    for info in login_info_list:
        try:
            login(info['id'], info['pw'])
            driver.get('https://m109.mailplug.com/ra/worknote/users/check/')
            driver_sleep(2)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            if soup.select_one('button.commute-button.able').text.strip() == '출근':
                driver.find_element(By.XPATH, '//*[@id="commute-check"]/div[1]/div[1]/div[2]/div[3]/button[1]').click()
                slack_bot(f"{id_security(info['id'])}님 출석 성공.")
            else:
                slack_bot(f"{id_security(info['id'])}님 이미 출석.")
            logout()
        except Exception as e:
            continue
    driver.quit()


main()
