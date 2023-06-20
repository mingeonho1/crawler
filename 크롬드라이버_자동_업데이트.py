from selenium import webdriver
import chromedriver_autoinstaller
from user_agent import generate_user_agent


def chrome_driver(headless=True, image_enabled=False, maximized=False):
    options = webdriver.ChromeOptions()

    # headless
    if headless:
        options.add_argument("--headless=new")
    
    # 최대화
    if maximized:
        options.add_argument('--start-maximized')

    # image 로딩 X
    if not image_enabled:
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

    # 네이버 카페 패스
    # 경로는 잘 보고 설정 !
    # options.add_argument(r'--load-extension=C:\Users\user\AppData\Local\Google\Chrome\User'
    #                      r' Data\Default\Extensions\jojlddfolpiejckahpinefdikdogenjg\1.6.0_0')
    
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
