from fastapi import APIRouter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import os
import shutil
import json
import time
from pathlib import Path
import secrets
from oneloader_runner.modules.one_logging import OneLogger
from oneloader_runner.modules.api_description import Oneloader_api_desc
from selenium.webdriver.common.by import By
from typing import Union


ROUTER_NAME = 'aliexpress'
log = OneLogger(logfile=f'{ROUTER_NAME}.log', logger_name=f'{ROUTER_NAME}')
ali = APIRouter(prefix=f"/{ROUTER_NAME}")

api_tags = Oneloader_api_desc()

@ali.get('/product/detail', tags = ['Aliexpress'])
def ali_get_product_detail(product_detail_url: str, lang_code: Union[str, None] = None):
    sid = secrets.token_hex(8 // 2)
    metadatas = {
        'chrome_data_path': f'chrome-ali-{sid}-data',
        'cookie_name': f'cookie_ali_{sid}.json',
        'product_detail_url': product_detail_url,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    }
    log.info(f'Start collect product detail: config{metadatas}')

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument(
        f'--user-data-dir={metadatas["chrome_data_path"]}')
    chrome_options.add_argument(f'user-agent={metadatas["user-agent"]}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    search_url = f"{product_detail_url}"
    driver.get(search_url)

    Path(metadatas["cookie_name"]).write_text(
        json.dumps(driver.get_cookies(), indent=2)
    )
    # Test
    # retrieve cookies from a json file
    for cookie in json.loads(Path(metadatas["cookie_name"]).read_text()):
        driver.add_cookie(cookie)

    if lang_code == "en":
        log.info(f'+========================= 팝업 클릭 시작')
        language_popup_xpath = '//*[@id="_full_container_header_23_"]/div[2]/div/div[2]/div[2]/div[1]/div/div/span'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, language_popup_xpath))).click()

        #driver.find_element(By.XPATH, language_popup_xpath).click()
        log.info(f'클릭 했음')
        #time.sleep(1)

        language_code_css = '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(6) > div > div.select--text--1b85oDo'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, language_code_css))).click()

        #driver.find_element(By.CSS_SELECTOR, language_code_css).click()
        #time.sleep(1)
        language_code_en_css = '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(6) > div > div.select--popup--W2YwXWt.select--visiblePopup--VUtkTX2 > div:nth-child(2)'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, language_code_en_css))).click()
        #driver.find_element(By.CSS_SELECTOR, language_code_en_css).click()
        log.info(f'랭퀴지코드 클릭 했음')

        currency_code_css = '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(8) > div > div.select--text--1b85oDo'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, currency_code_css))).click()
        currency_code_usd_css = '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(8) > div > div.select--popup--W2YwXWt.select--visiblePopup--VUtkTX2 > div:nth-child(2)'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, currency_code_usd_css))).click()
        #driver.find_element(By.CSS_SELECTOR, currency_code_css).click()
        #time.sleep(1)
        #driver.find_element(By.CSS_SELECTOR, currency_code_usd_css).click()
        log.info(f'재화코드 클릭 했음')

        language_popup_save_css = '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div.es--saveBtn--w8EuBuy'
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, language_popup_save_css))).click()
        #driver.find_element(By.CSS_SELECTOR, language_popup_save_css).click()
        time.sleep(1)


    scroll_steps = 15
    page_height = driver.execute_script("return document.body.scrollHeight")
    step_height = page_height // scroll_steps

    for step in range(scroll_steps):
        scroll_height = (step + 1) * step_height
        driver.execute_script(f"window.scrollTo(0, {scroll_height})")

    # 검색된 페이지 BeautifulSoup 로 변환
    # search_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

    variable_name = "window.runParams"

    # JavaScript 변수의 값을 가져오는 스크립트 실행
    js_script = f"return {variable_name};"
    product_detail_data = driver.execute_script(js_script)

    driver.close()

    if os.path.exists(metadatas['cookie_name']):
        os.remove(metadatas['cookie_name'])
    if os.path.exists(metadatas['chrome_data_path']):
        shutil.rmtree(metadatas['chrome_data_path'])

    log.info(f'Success collect product(SID): {sid}')
    return product_detail_data


@ali.get('/product/search', tags = ['Aliexpress'])
def ali_get_product_search(keyword: str, count: int, page_range=None):
    sid = secrets.token_hex(8 // 2)
    if count is None:
        count = 0
    metadatas = {
        'keyword': keyword,
        'search_count': count,  # 원하는 검색 개수
        'page_range': page_range,  # 원하는 검색 페이지 범위
        'base_url': f"https://www.aliexpress.com/wholesale?SearchText={keyword}",
        'chrome_data_path': f'chrome-ali-{sid}-data',
        'cookie_name': f'cookie_ali_{sid}.json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
        'product_detail_a_tag_pattern': r'[A-Za-z0-9]+--[A-Za-z0-9]+--[A-Za-z0-9]+\s+[A-Za-z0-9]+--[A-Za-z0-9]+--[A-Za-z0-9]+\s+search-card-item',
    }
    log.info(f'set meta datas: {metadatas}')
    if int(count) > 1 and page_range is not None:
        return {'error': 'Both  set count and page_range value'}
    elif int(count) == 0 and page_range is None:
        return {'error': 'Both not set count and page_range value'}
    else:
        pass

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument(
        f'--user-data-dir={metadatas["chrome_data_path"]}')
    chrome_options.add_argument(f'user-agent={metadatas["user-agent"]}')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enble-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(metadatas["base_url"])

    # 쿠키 파일저장
    Path(metadatas["cookie_name"]).write_text(
        json.dumps(driver.get_cookies(), indent=2)
    )

    # 파일에서 webdriver 로 쿠키 저장
    for cookie in json.loads(Path(metadatas["cookie_name"]).read_text()):
        driver.add_cookie(cookie)

    # 페이지 스크롤, 스크롤을 페이지 하단까지 내리지 않으면 인식 안되는 태그 있음(?)
    scroll_steps = 7
    page_height = driver.execute_script("return document.body.scrollHeight")
    step_height = page_height // scroll_steps

    for step in range(scroll_steps):
        scroll_height = (step + 1) * step_height
        driver.execute_script(f"window.scrollTo(0, {scroll_height})")
    search_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    a_href_pattern = re.compile(metadatas["product_detail_a_tag_pattern"])

    try:
        # 첫번째 페이지에서 상품 링크 추출
        product_a_tag_list = search_page_soup.find_all(
            'a', class_=a_href_pattern)
        log.info(
            f"Product count of the searched page: {len(product_a_tag_list)}")
    except Exception as e:
        log.error(f"Get product_a_tag_list fail: {e}")

    product_count = 1
    product_detail_url = []
    stop_flag = False
    start_page = 2

    # 페이지 하단 paging 숫자 추출
    get_paging = search_page_soup.find_all('a', {'rel': 'nofollow'})
    last_page = 0
    for v in get_paging:
        if v.get_text(strip=True).isdigit():
            last_page = int(v.get_text(strip=True))

    log.info(f'Last number of the paging : {last_page}')

    # search count(원하는 검색 개수) 설정되어 있을경우; 검색된 페이지에서 데이터 추출
    if metadatas["search_count"] > 0:
        end_page = last_page + 1
        log.info(f'Search Count is Set: {metadatas["search_count"]}')
        for a_tag in product_a_tag_list:
            # log.info(f'product_count: count val : {product_count}, set val: {metadatas["search_count"]}, product length : {len(product_detail_url)}')
            # 상세페이지 링크만 추출
            linked_url = a_tag["href"].replace("https:", '')
            if 'aliexpress.com/gcp/' in linked_url:
                log.info(f'found 1$ discount product!')
            else:
                product_detail_url.append(f'https:{linked_url}')
                if len(product_detail_url) >= metadatas["search_count"]:
                    log.info(
                        f'To Collect set of the search count : collected product {product_count}, Set search count{int(metadatas["search_count"])}')
                    return {'total_count': len(product_detail_url), 'product_detail_url': product_detail_url}
                product_count += 1

    # page range 가 설정되어 있을 경우;
    elif metadatas["page_range"] is not None:
        start_page = int(metadatas["page_range"].split('-')[0])
        end_page = int(metadatas["page_range"].split('-')[1]) + 1
        log.info(
            f'Page Range is Set, start_page: {start_page}, end_page: {end_page}')

    # 1번 페이지는 검색 링크에서 추출 그 2페이지부터 추출 시작
    for c in range(start_page, end_page):
        log.info(f'page range start, stop flag = {stop_flag}')
        if stop_flag is True:
            return {'total_count': len(product_detail_url), 'product_detail_url': product_detail_url}

        next_search_url = metadatas["base_url"] + f"&page={c}"
        driver.get(next_search_url)
        # 두번째 이후 페이지에서도 쿠키 파일저장
        Path(metadatas["cookie_name"]).write_text(
            json.dumps(driver.get_cookies(), indent=2)
        )

        # 파일에서 webdriver 로 쿠키 저장
        for cookie in json.loads(Path(metadatas["cookie_name"]).read_text()):
            driver.add_cookie(cookie)

        # 페이지 스크롤, 스크롤을 페이지 하단까지 내리지 않으면 인식 안되는 태그 있음(?)
        scroll_steps = 7
        page_height = driver.execute_script(
            "return document.body.scrollHeight")
        step_height = page_height // scroll_steps

        for step in range(scroll_steps):
            scroll_height = (step + 1) * step_height
            driver.execute_script(f"window.scrollTo(0, {scroll_height})")

        search_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        a_href_pattern = re.compile(metadatas["product_detail_a_tag_pattern"])
        try:
            # 두번째 페이지에서 상품 링크 추출
            product_a_tag_list = search_page_soup.find_all('a', class_=a_href_pattern)
        except Exception as e:
            log.error(f"product_a_tag_list: {e}")

        # 상품링크에서 상세 페이지 링크만 추출
        for a_tag in product_a_tag_list:
            product_count += 1
            product_detail_url.append(f'https:{a_tag["href"]}')

            if product_count >= metadatas["search_count"] and metadatas["search_count"] > 0:
                return {'total_count': len(product_detail_url), 'product_detail_url': product_detail_url}

    driver.close()

    if os.path.exists(metadatas['cookie_name']):
        os.remove(metadatas['cookie_name'])
    if os.path.exists(metadatas['chrome_data_path']):
        shutil.rmtree(metadatas['chrome_data_path'])

    log.info(f'Success collect product(SID): {sid}')
    return {'total_count': len(product_detail_url), 'product_detail_url': product_detail_url}
