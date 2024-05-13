import random

#from selenium import webdriver
from seleniumwire import webdriver
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
from oneloader_runner.modules.one_logging import OneLogger

log =OneLogger(logfile=f's1688_libs.log', logger_name=f's1688_libs')
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
def collectProductDetail(metadatas):

    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'--user-data-dir={metadatas["chrome_data_path"]}')
    chrome_options.add_argument(f'user-agent={metadatas["user-agent"]}')
    chrome_options.add_argument('--refer=https://detail.1688.com')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.header_overrides = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'cna=6B2NFMQceWkCATy/9iZmJ/r2; ali_ab=60.191.246.38.1543910908671.4; lid=%E4%B9%89%E4%B9%8C2010; __last_userid__=375685501; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16b40021a50161-08fe1f8fb068e8-37657e03-1fa400-16b40021a51abb; ali_apache_id=11.15.106.128.1564454978766.321081.5; h_keys="%u7537%u68c9%u670d#%u73a9%u5177#%u4e49%u4e4c%u5e02%u4e00%u6db5%u5236%u7ebf#%u91d1%u5b9d%u8d1d#%u4e00%u6db5%u5236%u7ebf#2017%u5723%u8bde%u9996%u9970#%u5723%u8bde%u9996%u9970#%u9996%u9970#%u7ea2%u85af#%u4e49%u4e4c%u817e%u535a%u793c%u54c1"; ad_prefer="2019/08/08 09:38:58"; ali_beacon_id=60.191.246.38.1566810215744.002451.6; ali_apache_track=c_mid=b2b-375685501ncisr|c_lid=%E4%B9%89%E4%B9%8C2010|c_ms=1|c_mt=2; taklid=9d140935ba3b4a8f9c20e255b4a99dd0; _csrf_token=1569548292989; cookie2=11e8d4b69091a1157b038c714385c9a6; t=4c47e32627e4d9d5c08008789ed65a34; _tb_token_=ab7d81831375; uc4=id4=0%40UgDLKslxx%2F5KKbIzCKEbS9CpADM%3D&nk4=0%40s5u8VZNrKh1Ipk4a6%2FKiHZj80A%3D%3D; __cn_logon__=false; alicnweb=homeIdttS%3D99025414611281355176293308315884802540%7Ctouch_tb_at%3D1569548305483%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E4%25B9%2589%25E4%25B9%258C2010%7Cshow_inter_tips%3Dfalse; l=cBMFFQcuvPgtaQebKOfalurza77T5IRb4sPzaNbMiICP_j1y5CQAWZCBm382CnGVp626R3zP_tquBeYBc1bnLjDSik2H9; isg=BNTUjkpcdQqEKuDNKwS17J7fpRRMK8akMa0MD261lt_jWXSjlj_fp6CTWRHkoTBv',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

    try:
        driver.get(metadatas["product_detail_url"])
        print(f'user agent : {metadatas["user-agent"]}')
        Path(metadatas['cookie_name']).write_text(
            json.dumps(driver.get_cookies()))
        for cookie in json.loads(Path(metadatas['cookie_name']).read_text()):
            driver.add_cookie(cookie)
            print(cookie)

    except Exception as e:
        log.error(f'S1688 Product detail page fail: {e}')

    ## 페이지 스크롤
    page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_steps = 15
    scroll_cnt = 0
    while True:
        # Scroll down to bottom
        step_height = page_height // scroll_steps
        # cur_height = 0
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

        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'img-list-wrapper')))
        thumb_img_div_tag = driver.find_element(By.CLASS_NAME, 'img-list-wrapper')
        thumb_img_lists = thumb_img_div_tag.find_elements(By.CLASS_NAME, 'detail-gallery-img')
        for idx, val in thumb_img_lists:
            print(val.get_attribute('src'))

