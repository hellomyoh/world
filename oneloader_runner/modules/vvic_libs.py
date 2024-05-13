from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pathlib import Path
from time import sleep
import hashlib
import os
import json
import shutil
import requests


from oneloader_runner.modules.one_logging import OneLogger

log =OneLogger(logfile=f'vvic_libs.log', logger_name=f'vvic_libs')
def getPagingCount(bs4_data_raw):
    bs4_data = BeautifulSoup(bs4_data_raw, 'html.parser')
    get_paging = bs4_data.find_all('li', {'class': 'number'})
    last_page = 0
    for v in get_paging:
        #log.info(f'paging count : {v.get_text()}')
        last_page = int(v.get_text(strip=True))
    return last_page
def deleteSessionFiles(cookie_file: str, chrome_folder: str):
    print(f'cookie_file: {cookie_file}')
    if os.path.exists(cookie_file):
        print(f'delete cookie_file: {cookie_file}')
        os.remove(cookie_file)
    if os.path.isdir(chrome_folder):
        print(f'delte chrome: {cookie_file}')
        shutil.rmtree(chrome_folder)
def getNextbtnUrl(bs4_data_raw):
    bs4_data = BeautifulSoup(bs4_data_raw, 'html.parser')
    get_paging = bs4_data.find_all('li', {'class': 'number'})
def genHash(url: str):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()

def collectProductLinkForPageRange(metadatas):
    start_page = int(metadatas['page_range'].split('-')[0])
    end_page = int(metadatas['page_range'].split('-')[1]) + 1

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'--user-data-dir={metadatas["chrome_data_path"]}') # 우분투에선 옵션 비활성화시 에러
    chrome_options.add_argument(f'user-agent={metadatas["user-agent"]}') # 우분투에선 옵션 비활성화시 에러
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    log.info(f'base_search_url : {metadatas["base_search_url"]}')

    product_detail_url = {}
    product_detail_url['filter_ad_applied'] = metadatas['ad_filter']
    product_detail_url['request_count'] = metadatas['search_count']
    product_detail_url['page_range'] = metadatas['page_range']
    product_detail_url['lists'] = {}

    searched_ad_product_cnt, searched_non_ad_product_cnt, failtocollect, cnt = 0, 0, 0, 0

    ad_img_hash = genHash(
        'data:image/png;base64,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')

    failed_search_tag = '//*[@id="app"]/div/div[4]/div/div[2]/div/div/div[3]/div[1]/div/div/div[1]/p/text()[1]'
    request_region = metadatas["region_code"].split(",")
    if 'all' in request_region:
        request_region = ["gz","pn","hz","xt","hznz","jfn"]

    ## request search page
    for rg in request_region:
        product_detail_url['lists'][rg] = []
        for pg in range(start_page, end_page):
            search_url = metadatas["base_search_url"] % (rg.strip(), metadatas['keyword'], pg)
            log.info(f'search url ({rg}) : {search_url}')
            try:
                driver.get(search_url)
            except Exception as e:
                log.error(f'VVIC search request fail: {e}')

            product_lists_div_tag = '//*[@id="app"]/div/div[4]/div/div[2]/div/div[1]/div[3]/div'

            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, product_lists_div_tag)))

            # 페이지 스크롤, 스크롤을 페이지 하단까지 내리지 않으면 인식 안되는 태그 있음(?)
            """ scroll_steps = 15
            page_height = driver.execute_script("return document.body.scrollHeight")
            step_height = page_height // scroll_steps
            for step in range(scroll_steps):    
                sleep(0.3)        
                scroll_height = (step + 1) * step_height
                driver.execute_script(f"window.scrollTo(0, {scroll_height})")"""

            page_height = driver.execute_script("return document.body.scrollHeight")
            scroll_steps = 15
            scroll_cnt = 0
            while True:
                # Scroll down to bottom
                step_height = page_height // scroll_steps
                #cur_height = 0
                for step in range(scroll_steps):
                    sleep(0.2)
                    scroll_cnt += 1
                    scroll_height = (step + 1) * step_height
                    driver.execute_script(f"window.scrollTo(0, {scroll_height})")

                cur_height = driver.execute_script("return document.body.scrollHeight")
                log.info(f'scroll down step {scroll_cnt}: {page_height}, {cur_height}')
                if page_height <= cur_height:
                    break
                else:
                    page_height = driver.execute_script("return document.body.scrollHeight")
            # 검색 페이지내 상품 전체 영역
            try:
                product_lists_div = driver.find_element(By.XPATH, product_lists_div_tag)
            except Exception as e:
                log.info(f'product lists page loading failed. try again: {e}')
                return {'error': f'product lists page loading failed. try again: {e}'}

            # 전체 상품 영역 내 개별 상품 영역
            product_lists_good_item = product_lists_div.find_elements(By.CLASS_NAME, 'goods-item')
            # 상품 이미지에 광고 상품 워터 마크

            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'strength-top-img')))
            try:
                product_lists_ad_img = product_lists_div.find_elements(By.CLASS_NAME, 'strength-top-img')
            except Exception as e:
                log.info(f'product adv. image detect failed. try again: {search_url}{e}')
                #product_detail_url['error'] = f'product adv. image detect failed. try again: {e}'
                #return product_detail_url

            # 전체 상품 리스트내에서 상품 하나씩 꺼내 비교
            for val in product_lists_good_item:
                log.info(f'ad filter option is : {metadatas["ad_filter"]}')
                if metadatas['ad_filter'] is True:
                    try:
                        ## 상세 페이지 url 을 찾는다
                        detail_link = val.find_element(By.CLASS_NAME, 'img-box')
                        link = detail_link.get_attribute("href")
                        item_vid = link.split('?')[0].split('/')
                        hash_id = genHash(item_vid[len(item_vid) - 1])
                        log.info(f'found link : {link}')
                    except NoSuchElementException as e:
                        # 상세 페이지 url 이 없는경우 link 를 None 처리, 왜 인지는 파악안됨
                        log.info(f'Occer error not found img-box class:')
                        link = None
                        hash_id = 'abcdefg12345'
                    try:
                        # 광고 워터마크가 있는지 검사한다.
                        ad_img = val.find_element(By.CLASS_NAME, 'strength-top-img')
                        is_ad_img_hash = genHash(ad_img.get_attribute("src"))
                        # 광고 워터마크 이미지는 img src 에 바이너리로 되어 있어 hash   변환 후 비교한다.
                        if ad_img_hash == is_ad_img_hash:
                            log.info(f'Found Ad image, hash the same With ad watermark {searched_ad_product_cnt}!')
                        else:
                            # 워터 마크가 있지만 광고가 아닌 상품을 담는다
                            log.info(f'Found image but not ad img, hash is difference {searched_non_ad_product_cnt}')
                            if link is not None:
                                product_detail_url['lists'][rg].append(link)
                    except NoSuchElementException as e:
                        # 워터 마크 정보가 없으면 non ad 로 넣는다
                        log.info(f'Not exists ad watermark on image {searched_non_ad_product_cnt}')
                        if link is not None:
                            product_detail_url['lists'][rg].append(link)
                else:
                    try:
                        ## 상세 페이지 url 을 찾는다
                        detail_link = val.find_element(By.CLASS_NAME, 'img-box')
                        link = detail_link.get_attribute("href")
                        item_vid = link.split('?')[0].split('/')
                        hash_id = genHash(item_vid[len(item_vid) - 1])
                        log.info(f'found link : {link}')
                    except NoSuchElementException as e:
                        # 상세 페이지 url 이 없는경우 link 를 None 처리, 왜 인지는 파악안됨
                        log.info(f'Occer error not found img-box class:')
                        link = None
                        hash_id = 'abcdefg12345'

                    log.info(f'Collect Count: {searched_ad_product_cnt}')
                    if link is not None:
                        product_detail_url['lists'][rg].append(link)
                    else:
                        failtocollect += 1
                    searched_ad_product_cnt += 1
    driver.quit()

    return product_detail_url
def collectProductLinkForSearchCount(metadatas):
    if metadatas['page_range'] is not None:
        start_page = int(metadatas['page_range'].split('-')[0])
        end_page = int(metadatas['page_range'].split('-')[1]) + 1
    else:
        start_page = 1
        end_page = 70

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'--user-data-dir={metadatas["chrome_data_path"]}')
    chrome_options.add_argument(f'user-agent={metadatas["user-agent"]}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    product_detail_url = {}
    product_detail_url['filter_ad_applied'] = metadatas['ad_filter']
    product_detail_url['request_count'] = metadatas['search_count']
    product_detail_url['page_range'] = metadatas['page_range']
    product_detail_url['lists'] = {}

    total_cnt = 0
    last_paging_count = 0
    searched_ad_product_cnt, searched_non_ad_product_cnt, failtocollect, cnt = 0, 0, 0, 0

    ad_img_hash = genHash(
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASQAAABQCAMAAACH4/i9AAADAFBMVEX/AGD96Z0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQnKYrAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC8ElEQVR4nO2b0XrDIAiFddv7vzK7aJJaA/GgwWA//otuM5roEdBgl9OS5KlP+5n6tEUJkQBCJIAQCSBEAgiRAEIkgBAJIEQCCJEA/oRyeN9PN3XEM2FJACESgORut5PTuq7JiaQaD1a5J7WR3ag6zZK6cKLTpJj0GqrKnnLR8GEicAPU7saGmNoCqPp95aCMYBKTRLc6XWhJayM9eNejt74DdxtovKPHBhGTAGpLOoUYLt6UZVI8ak7x3FOhIVZ3t34Uk7S6SOzCe7eRThSpsTtkR8YVzt9sdImEdzPXdcdH+MCGzHZ1yynlhQK0hKm75e2TnfyFtugmItHxc5MJEeRqn1GWPYDxZnIb5eI+17SkfXdZ/q2Aemffk6z2ryV0fCyLoUi7j9WJlYE7DrXux06k9/JPvdp4sT9odSs7CybYtknPX+BsdpZ0JAnudpEnBDdzNypzKXo8LW6WgXuXydV4u1DvuDWJf8p7iy7chDLbVAlhbyRn7K1P8wQLd+M36HC+yB9zj5RQUcbc9HaaIn3hwaN6OC6PlAR7e8w3XYqUUnJlvgYxiV3Q+CjD24a7aK7OJ7VRmMBFVeHSI/ZlfFqyo1mupixtqnmfE5OOLgHvu+bOptd/ikjHsSRwxOToC24HnLvRayhUFrCockvUOGKq6nrC/pi7SOLSnoq7lF3SCP8GGHshlxd1Pm0t0kfX3mcngkzuFv8XE05wUyrmdjcmTqZcV+bvNUaPJwsitbNGzXhUjOrzvESSiTlcSbU4NwUrpeI2lnQ5Ml4myYxIHlCPcXWpbCFSc/LPAz8KzrVJMMkuOr50n2xEIi4YsTVILBCaDfesC2hrV9z/YsrPza7qnGKa+H8k3M36wzh1NP69viz7Rbtda9rqbIGYDr9YCPXkrG9stQUADPsUogfupUEvsNG7m7P3ikFQWbFYNI25W3O/6VtHhEgAIRKA0/fuFhGT3BEiAYRIACESQIgEECIBhEgAIRJAiAQQIgGESAD/zymV5L5PC2UAAAAASUVORK5CYII=')

    failed_search_tag = '//*[@id="app"]/div/div[4]/div/div[2]/div/div/div[3]/div[1]/div/div/div[1]/p/text()[1]'
    ## request search page

    request_region = metadatas["region_code"].split(",")
    if 'all' in request_region:
        request_region = ["gz","pn","hz","xt","hznz","jfn"]

    for rg in request_region:
        product_detail_url['lists'][rg] = []
        for pg in range(start_page, end_page):
            if len(product_detail_url['lists'][rg]) >= metadatas['search_count']:
                break
            search_url = metadatas["base_search_url"] % (rg, metadatas['keyword'], pg)
            log.info(f'search url ({rg}) : {search_url}')
            try:
                driver.get(search_url)
            except Exception as e:
                log.error(f'VVIC search request fail: {e}')

            product_lists_div_tag = '//*[@id="app"]/div/div[4]/div/div[2]/div/div[1]/div[3]/div'

            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, product_lists_div_tag)))

            # 페이지 스크롤, 스크롤을 페이지 하단까지 내리지 않으면 인식 안되는 태그 있음(?)
            page_height = driver.execute_script("return document.body.scrollHeight")
            scroll_steps = 15
            scroll_cnt = 0
            while True:
                # Scroll down to bottom
                step_height = page_height // scroll_steps
                #cur_height = 0
                for step in range(scroll_steps):
                    sleep(0.2)
                    scroll_cnt += 1
                    scroll_height = (step + 1) * step_height
                    driver.execute_script(f"window.scrollTo(0, {scroll_height})")

                cur_height = driver.execute_script("return document.body.scrollHeight")
                log.info(f'scroll down step {scroll_cnt}: {page_height}, {cur_height}')
                if page_height <= cur_height:
                    break
                else:
                    page_height = driver.execute_script("return document.body.scrollHeight")

            # 검색 페이지내 상품 전체 영역
            try:
                product_lists_div = driver.find_element(By.XPATH, product_lists_div_tag)
            except Exception as e:
                log.info(f'product lists page loading failed. try again: {e}')
                product_detail_url['error'] = f'product lists page loading failed. try again: {e}'
                return product_detail_url

            # 전체 상품 영역 내 개별 상품 영역
            product_lists_good_item = product_lists_div.find_elements(By.CLASS_NAME, 'goods-item')
            # 상품 이미지에 광고 상품 워터 마크
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'strength-top-img')))
            try:
                product_lists_ad_img = product_lists_div.find_elements(By.CLASS_NAME, 'strength-top-img')
            except Exception as e:
                log.info(f'product adv. image detect failed. try again: {e}')
                #product_detail_url['error'] = f'product adv. image detect failed. try again: {e}'
                #return product_detail_url


            # 전체 상품 리스트내에서 상품 하나씩 꺼내 비교
            for val in product_lists_good_item:
                log.info(f'ad filter option is : {metadatas["ad_filter"]}')
                if metadatas['ad_filter'] is True:
                    try:
                        ## 상세 페이지 url 을 찾는다
                        detail_link = val.find_element(By.CLASS_NAME, 'img-box')
                        link = detail_link.get_attribute("href")
                        item_vid = link.split('?')[0].split('/')
                        hash_id = genHash(item_vid[len(item_vid) - 1])
                        log.info(f'found link : {link}')
                    except NoSuchElementException as e:
                        # 상세 페이지 url 이 없는경우 link 를 None 처리, 왜 인지는 파악안됨
                        log.info(f'Occer error not found img-box class:')
                        link = None
                        hash_id = 'abcdefg12345'
                    try:
                        # 광고 워터마크가 있는지 검사한다.
                        ad_img = val.find_element(By.CLASS_NAME, 'strength-top-img')
                        is_ad_img_hash = genHash(ad_img.get_attribute("src"))
                        # 광고 워터마크 이미지는 img src 에 바이너리로 되어 있어 hash   변환 후 비교한다.
                        if ad_img_hash == is_ad_img_hash:
                            log.info(f'Found Ad image, hash the same With ad watermark {searched_ad_product_cnt}!')
                        else:
                            # 워터 마크가 있지만 광고가 아닌 상품을 담는다
                            log.info(f'Found image but not ad img, hash is difference {searched_non_ad_product_cnt}')
                            if link is not None:
                                product_detail_url['lists'][rg].append(link)
                    except NoSuchElementException as e:
                        # 워터 마크 정보가 없으면 non ad 로 넣는다
                        log.info(f'Not exists ad watermark on image {searched_non_ad_product_cnt}')
                        if link is not None:
                            product_detail_url['lists'][rg].append(link)

                    if len(product_detail_url['lists'][rg]) >= metadatas['search_count']:
                        log.info(f'collected count : {len(product_detail_url["lists"][rg])}, region set : {request_region}, searched {rg}, searched page : {pg}')
                        break
                else:
                    try:
                        ## 상세 페이지 url 을 찾는다
                        detail_link = val.find_element(By.CLASS_NAME, 'img-box')
                        link = detail_link.get_attribute("href")
                        item_vid = link.split('?')[0].split('/')
                        hash_id = genHash(item_vid[len(item_vid) - 1])
                        log.info(f'found link : {link}')
                    except NoSuchElementException as e:
                        # 상세 페이지 url 이 없는경우 link 를 None 처리, 왜 인지는 파악안됨
                        log.info(f'Occer error not found img-box class:')
                        link = None
                        hash_id = 'abcdefg12345'

                    log.info(f'Collect Count: {searched_ad_product_cnt}')
                    if link is not None:
                        product_detail_url['lists'][rg].append(link)
                    else:
                        failtocollect += 1
                    searched_ad_product_cnt += 1
                    if len(product_detail_url['lists'][rg]) >= metadatas['search_count']:
                        log.info(f'region set : {request_region}, searched {rg}')
                        break
    driver.quit()

    return product_detail_url
def collectProductDetail(metadatas):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')

    chrome_options.add_argument(f'--user-data-dir={metadatas["chrome_data_path"]}')
    chrome_options.add_argument(f'user-agent={metadatas["user-agent"]}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    if not os.path.exists(metadatas['cookie_name']):
        log.info(f'cookie file not exists, start login ... ')
        login_url = "https://www.vvic.com/login.html"

        try:
            driver.get(login_url)
        except Exception as e:
            log.error(f'VVIC Login page fail: {e}')

        ### 페이지 스크롤
        scroll_steps = 10
        page_height = driver.execute_script("return document.body.scrollHeight")
        step_height = page_height // scroll_steps
        for step in range(scroll_steps):
            scroll_height = (step + 1) * step_height
            driver.execute_script(f"window.scrollTo(0, {scroll_height})")

        # 로그인 시작, 계정의 이메일 인증이 먼저 되어야 함.
        id_pw_login_tag = '//*[@id="account"]'
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.XPATH, id_pw_login_tag)))
        id_pw_login_tag_click = driver.find_element(By.XPATH, id_pw_login_tag).click()

        input_id_tag = '//*[@id="username"]'
        input_pw_tag = '//*[@id="password"]'
        try_login_btn_tag = '//*[@id="submit"]'

        input_id = driver.find_element(By.XPATH, input_id_tag).send_keys(metadatas['username'])
        input_pw = driver.find_element(By.XPATH, input_pw_tag).send_keys(metadatas['password'])
        driver.find_element(By.XPATH, try_login_btn_tag).click()

        check_login_id_tag = '//*[@id="username"]/span'

        ## 페이지 스크롤
        scroll_steps = 15
        page_height = driver.execute_script("return document.body.scrollHeight")
        step_height = page_height // scroll_steps
        for step in range(scroll_steps):
            sleep(0.1)
            scroll_height = (step + 1) * step_height
            driver.execute_script(f"window.scrollTo(0, {scroll_height})")

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="username"]/span')))
            log.info(f'passed login and checked login id... ')
        except Exception as e:
            log.error(f'login failed at afeter id/pw insert and click')
            return {'error': 'login failed at afeter id/pw insert and click'}

        Path(metadatas['cookie_name']).write_text(
            json.dumps(driver.get_cookies()))
        log.info(f'cookie : {driver.get_cookies()}')
    else:
        log.info(f'cookie file already exist start collect detail page')


    '''
    ### 상세 페이지 읽어오기 (예전버전)
    try:
        driver.get(metadatas['product_detail_url'])
        for cookie in json.loads(Path(metadatas['cookie_name']).read_text()):
            driver.add_cookie(cookie)
    except Exception as e:
        log.error(f'Get product detail failed: {e}')
        return {'error': f'redirect to product detail page failed: {e}'}

    #sleep(1)
    ## 페이지 스크롤
    page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_steps = 15
    scroll_cnt = 0
    while True:
        # Scroll down to bottom
        step_height = page_height // scroll_steps
        #cur_height = 0
        for step in range(scroll_steps):
            sleep(0.2)
            scroll_cnt += 1
            scroll_height = (step + 1) * step_height
            driver.execute_script(f"window.scrollTo(0, {scroll_height})")

        cur_height = driver.execute_script("return document.body.scrollHeight")
        log.info(f'scroll down step {scroll_cnt}: {page_height}, {cur_height}')
        if page_height <= cur_height:
            break
        else:
            page_height = driver.execute_script("return document.body.scrollHeight")

    get_product_detail_url = metadatas['product_detail_url'].split('?')
    product_subject_class = 'detail-title'
    #shop_url_xpath = '//*[@id="app"]/div/div[4]/div/div[1]/div/div[1]/div/div[1]/div[1]/a'
    nav_xpath = '//*[@id="app"]/div/div[4]/div/div[2]/nav'
    product_subject = driver.find_element(By.CLASS_NAME, product_subject_class).text

    #shop_url = driver.find_element(By.XPATH, shop_url_xpath).get_attribute("href")
    category_nav_class = driver.find_element(By.XPATH, nav_xpath)
    category_nav = category_nav_class.find_elements(By.TAG_NAME, 'a')
    cat = []
    for c in  category_nav:
        cat.append(c.text)
    try:
        amount = driver.find_element(By.XPATH, '/html/body/div[6]/article/main/section[1]/div[2]/div[6]/div[2]/ul/li[3]').text
    except Exception as e:
        log.info(f'Can not found amount, amount is set default(9999): {e}')
        amount = 9999
    market_name, shop_url = "", ""
    shop_info_class = 'slzz-shop-name'
    try:
        shop_info = driver.find_element(By.CLASS_NAME, shop_info_class)
        shop_url = shop_info.find_element(By.TAG_NAME, 'a').get_attribute("href")
        market_name = shop_info.find_element(By.TAG_NAME, 'a').text
    except Exception as e:
        log.info(f'error get shop info.')

    '''
    get_product_item_code = metadatas["product_detail_url"].split("/")[-1].split("?")[0]
    get_product_detail_json_url = 'https://www.vvic.com/apif/item/' + get_product_item_code + "/detail"

    try:
        get_product_detail_json = driver.get(get_product_detail_json_url)
    except Exception as e:
        log.info(f'"error: URL {get_product_detail_json} requests Failed."')

    product_detail_datas = driver.find_element(By.TAG_NAME, 'body').text
    product_detail_datas_json = json.loads(product_detail_datas)

    log.info(f'GET DATAS from URL : {product_detail_datas_json["data"]["id"]}')

    categories = [item['name'] for item in product_detail_datas_json["data"]['breadCrumbs']]
    category = '/'.join(categories)

    color_pics = [item['name'] for item in product_detail_datas_json["data"]['breadCrumbs']]

    crypto_js_cdn = requests.get("https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js")
    crypto_js_text = crypto_js_cdn.text
    crypto_js = driver.execute_script(crypto_js_text)
    decode_scripts = """
    function decryptByDES (t, e, i) {
        var s = CryptoJS.enc.Utf8.parse(e)
          , a = CryptoJS.enc.Utf8.parse(i);
        return CryptoJS.DES.decrypt(t, s, {
            iv: a,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        }).toString(CryptoJS.enc.Utf8)
    }
"""
    decode_scripts = decode_scripts + f'const keyphrase = "item_detail_{product_detail_datas_json["data"]["vid"]}";'
    decode_scripts = decode_scripts + f'const iv = "{product_detail_datas_json["data"]["iv"]}";'
    decode_scripts = decode_scripts + f'const skumap = "{product_detail_datas_json["data"]["skumap"]}";'
    decode_scripts = decode_scripts + """
    return decryptByDES(skumap, keyphrase, iv);
    """
    #log.info(f'javascirpt : {decode_scripts}')
    skumap = driver.execute_script(decode_scripts)
    #log.info(f'SKUMAP  : {skumap}')

    product_detail = {}
    product_detail['product_detail'] = {}
    product_detail['product_detail']['product_detail_url'] = metadatas['product_detail_url']
    #product_detail['product_detail']['market_name'] = market_name
    product_detail['product_detail']['shop_url'] = f'https://www.vvic.com/shop/{product_detail_datas_json["data"]["shop_id"]}'
    product_detail['product_detail']['market_name'] = f'{product_detail_datas_json["data"]["shop_id"]}'
    product_detail['product_detail']['vi'] = product_detail_datas_json["data"]['iv']
    product_detail['product_detail']['category'] = category
    product_detail['product_detail']['amount'] = product_detail_datas_json["data"]['sales']
    product_detail['product_detail']['subject'] = product_detail_datas_json["data"]['title']
    product_detail['product_detail']['product_options'] = product_detail_datas_json["data"]["attrs_json"]
    product_detail['product_detail']['citycode'] = product_detail_datas_json["data"]["city_market_code"]
    product_detail['product_detail']['item_id'] = product_detail_datas_json["data"]["id"]
    product_detail['product_detail']['item_vid'] = product_detail_datas_json["data"]["vid"]

    product_detail['product_detail']['color'] = {}
    product_detail['product_detail']['color']['type'] = product_detail_datas_json["data"]["color"]
    product_detail['product_detail']['color']['color_img_urls'] = product_detail_datas_json["data"]["color_pics"]

    #product_detail['product_detail']['sold_out'] = product_detail_datas_json["data"]["status"]
    product_detail['product_detail']['price'] = {}
    product_detail['product_detail']['price']['currency_symbol'] = "¥"

    if product_detail_datas_json["data"]["price"] is None:
        product_detail['product_detail']['price']['display_price'] = float("0.00")
    else:
        product_detail['product_detail']['price']['display_price'] = float(product_detail_datas_json["data"]["price"])

    if product_detail_datas_json["data"]["originPrice"] is None:
        product_detail['product_detail']['price']['original_price'] = float("0.00")
    else:
        product_detail['product_detail']['price']['original_price'] = float(product_detail_datas_json["data"]["originPrice"])

    if product_detail_datas_json["data"]["discountPrice"] is None:
        product_detail['product_detail']['price']['discount_price'] = float("0.00")
    else:
        product_detail['product_detail']['price']['discount_price'] = float(product_detail_datas_json["data"]["discountPrice"])
    product_detail['product_detail']['price']['options'] = {}
    product_detail['product_detail']['price']['options']['service_fee'] = float(metadatas['service_fee'])
    product_detail['product_detail']['price']['options']['delivery_fee'] = float(metadatas['delivery_fee'])
    product_detail['product_detail']['size'] = product_detail_datas_json["data"]["size"]

    product_detail['product_detail']['item_status'] = product_detail_datas_json["data"]["status"]
    product_detail['product_detail']['product_imgs'] = {}
    product_detail['product_detail']['product_imgs']['index_img'] =  product_detail_datas_json["data"]["index_img_url"]

    product_detail['product_detail']['product_imgs']['thumb_imgs'] =  product_detail_datas_json["data"]["imgs"].split(',')
    product_detail['product_detail']['product_imgs']['contents_imgs'] = product_detail_datas_json["data"]["item_desc"]["desc"]
    product_detail['product_detail']['product_desc'] = product_detail_datas_json["data"]["item_desc"]["tags_desc"]
    product_detail['product_detail']['skumap'] = skumap
    log.info(f'DCODE SCRIPTS = >>>> {product_detail["product_detail"]["skumap"]}')

    '''
    # 상품 상세 이미지(예전버전)
    contents_imgs_div_tag = '//*[@id="info"]/div[1]'
    contents_imgs_div = driver.find_element(By.XPATH, contents_imgs_div_tag)
    contents_imgs = contents_imgs_div.find_elements(By.TAG_NAME, 'img')
    log.info(f'get contents images')
    for idx, img in enumerate(contents_imgs):
        if img.get_attribute('src') is not None:
            product_detail['product_detail']['product_imgs']['contents_imgs'][idx] = img.get_attribute('src')
    '''
    log.info(f'product_detail : {product_detail}')
    driver.quit()

    return product_detail
