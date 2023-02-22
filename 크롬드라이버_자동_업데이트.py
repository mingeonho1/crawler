from selenium import webdriver
import chromedriver_autoinstaller
from user_agent import generate_user_agent


def chrome_driver():
    options = webdriver.ChromeOptions()

    # headless
    # options.add_argument("--headless")

    # image 로딩 X
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    # mobile버전으로 chrome을 띄움
    # options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
    
    # javascript False 모드
    # options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

    # "Chrome이 자동화된 테스트 소프트웨어에 의해 제어되고 있습니다." 없애줌
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # 안전하지 않음 페이지 스킵하기
    options.add_argument("--ignore-certificate-errors")

    # 브라우저를 사용자 임의의 유저에이전트로 설정
    # generate_user_agent 모듈을 사용해 자동으로 user_agent를 넣어줬지만 임의로 넣어도 됨
    options.add_argument('user-agent=' + generate_user_agent(os='win', device_type='desktop'))

    # gpu(그래픽카드 가속)를 사용 X
    options.add_argument("disable-gpu")

    # 시크릿 모드
    options.add_argument('--incognito')
    try:
        path = chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(path, chrome_options=options)
    except FileNotFoundError as err:
        print(err)
    finally:
        return driver


# driver = chrome_driver()
#
# # 링크 접속
# driver.get("https://github.com/mingeonho1/Crawler")
#
# # 크롬드라이버 끄기
# driver.quit()
