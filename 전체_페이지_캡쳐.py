import logging
from 크롬드라이버_자동_업데이트 import chrome_driver
from openpyxl import load_workbook
import pandas as pd

driver = chrome_driver(image_enabled=True, maximized=True)

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)


def excel_date():
    load_wb = load_workbook(r"./example.xlsx")  # 엑셀 경로
    load_ws = load_wb['Sheet1']  # 시트명
    data = load_ws.values
    columns = next(data)[0:]
    f = pd.DataFrame(data, columns=columns)
    return f


def full_page_screenshot(url, image_name):
    try:
        # 페이지 이동
        driver.get(url)

        # 페이지 로드 대기
        driver.implicitly_wait(3)

        # 전체 페이지 크기 취득
        total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

        # 브라우저 창 크기 조정
        driver.set_window_size(total_width, total_height)

        # 스크린샷 저장
        driver.save_screenshot(fr"./img/{image_name}")

        logging.info(f"{image_name} 저장 성공")
    except Exception as e:
        logging.error(e)


def main():
    f = excel_date()
    for i, v in enumerate(zip(f['URL'], f['파일명'])):
        url, image_name = v
        full_page_screenshot(url, image_name)


main()
