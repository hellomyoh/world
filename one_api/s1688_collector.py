from fastapi import APIRouter
import secrets
from oneloader_runner.modules.s1688_libs import *
from oneloader_runner.modules.api_description import Oneloader_api_desc

api_desc = Oneloader_api_desc()

ROUTER_NAME = 's1688'
log = OneLogger(logfile=f'{ROUTER_NAME}.log', logger_name=f'{ROUTER_NAME}')
s1688 = APIRouter(prefix= f"/{ROUTER_NAME}")


@s1688.get('/product/detail', tags=["S1688"])
def vvic_get_product_detail(product_detail_url: str):
    sid = secrets.token_hex(8 // 2)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
        # Add more User-Agent strings as needed
    ]
    random_user_agent = random.choice(user_agents)
    metadatas = {
        'chrome_data_path': f'data/chrome-{ROUTER_NAME}-{sid}-data',
        'cookie_name': f'cookie/cookie_{ROUTER_NAME}_{sid}.json',
        'product_detail_url': product_detail_url,
        'user-agent': random_user_agent,
    }
    log.info(f'Start collect product detail: config{metadatas}')

    product_detail_datas = collectProductDetail(metadatas)

    return product_detail_datas


@s1688.get('/product/search', tags=["S1688"])
def vvic_get_product_search(keyword: str, count: int, region_code: str, ad_filter: bool, page_range=None):

    sid = secrets.token_hex(8 // 2)
    if count is None:
        count = 0
    metadatas = {
        'keyword': keyword,
        'search_count': count,  # 원하는 검색 개수
        'page_range': page_range,  # 원하는 검색 페이지 범위
        'ad_filter': ad_filter,
        'region_code': region_code,
        'base_search_url': "https://www.vvic.com/%s/search/index.html?sort=default&merge=1&algo=0&pid=1&q=%s&searchCity=gz&pageId=search_index&queryType=1&vcid=&currentPage=%s",
        'chrome_data_path': f'chrome-ali-{sid}-data',
        'cookie_name': f'cookie_ali_{sid}.json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    }

    log.info(f'set meta datas: {metadatas}')
    if int(count) > 1 and page_range is not None:
        return {'error': 'Both  set count and page_range value'}
    elif int(count) == 0 and page_range is None:
        return {'error': 'Both not set count and page_range value'}
    else:
        pass

    log.info(f'Start collect product detail: config{metadatas}')

    if metadatas['page_range'] is not None:
        page_range_links = collectProductLinkForPageRange(metadatas)
        return page_range_links
    elif metadatas['search_count'] > 1:
        search_count = collectProductLinkForSearchCount(metadatas)
        return search_count
    else:
        return {"error": "Unknown error"}
