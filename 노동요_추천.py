from time import sleep
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import random
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WebDriverManager:
    def __init__(self):
        self._set_chrome_options()

    def _set_chrome_options(self):
        self.selenium_options = ChromeOptions()
        self.selenium_options.add_argument('--headless=new')
        self.selenium_options.add_argument('--no-sandbox')
        self.selenium_options.add_argument('--disable-dev-shm-usage')
        self.selenium_options.add_argument('--start-maximized')
        self.selenium_options.add_argument('--disable-popup-blocking')

    def get_driver(self):
        driver = Chrome(
            service=Service('/usr/bin/google-chrome-stable'), version_main=113, options=self.selenium_options)
        driver.implicitly_wait(10)
        return driver


class SongRecommendation:
    def __init__(self, a_tag, slack_token, slack_channel, web_driver_manager):
        self._driver = web_driver_manager.get_driver()
        self._domain = "https://www.youtube.com"
        self._keyword = random.choice(["노동요 추천", "일할 때 듣는 플리", "노동요"])
        self._a_tag = a_tag
        self._soup = None
        self._url = None
        self._slack_token = slack_token
        self._slack_channel = slack_channel

    def _find_song_url(self):
        self._url = random.choice([self._domain + a['href'] for a in self._soup.select(self._a_tag)])

    def _page_scroll(self, count):
        for i in range(1, count + 1):
            self._driver.execute_script("return document.body.scrollHeight")
            sleep(1)
            self._driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        sleep(2)

    def _post_message_to_slack(self):
        client = WebClient(token=self._slack_token)
        client.chat_postMessage(channel=self._slack_channel, text=f"🙉 오늘의 노동요 추천 🙉\n{self._url}")

    def recommend_song(self):
        self._driver.get(f"{self._domain}/results?search_query={self._keyword}")
        self._page_scroll(5)
        self._soup = BeautifulSoup(self._driver.page_source, "html.parser")
        self._find_song_url()
        self._post_message_to_slack()


if __name__ == "__main__":
    while True:
        try:
            driver_manager = WebDriverManager()
            song_rec = SongRecommendation("h3 > a#video-title",
                                          "SLACK_TOKEN",    # 자신의 슬랙 토큰
                                          "SLACK_CHANNEL",  # 알림을 보내고 싶은 슬랙 체널 EX) #일반
                                          driver_manager)
            song_rec.recommend_song()
            break
        except Exception as e:
            print(e)
            continue
