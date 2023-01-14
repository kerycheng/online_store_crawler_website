from datetime import datetime

from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.service import Service as ChromeSerive
from subprocess import CREATE_NO_WINDOW
import json
import time

chrome_service = ChromeSerive('chromedriver')
chrome_service.creation_flags = CREATE_NO_WINDOW
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-3d-apis")
chrome_options.add_argument('--log-level=3')

driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options, service=chrome_service)

class scrape_shopee(object):
    def __init__(self, keyword, pages):
        self.keyword = keyword
        self.store = '蝦皮'
        self.time = datetime.today().date()
        self.pages = int(pages)

    # 將要抓取的頁面連結存到urls[]裡
    def get_url(self):
        urls = []
        if self.pages == 1:
            url = f'https://shopee.tw/search?keyword={self.keyword}&page=0'
            urls.append(url)
        else:
            for i in range(0, self.pages - 1): # 蝦皮頁面是從page=0開始算，所以這邊做-1
                url = f'https://shopee.tw/search?keyword={self.keyword}&page={i}'
                urls.append(url)

        return urls

    # 抓取資料
    def scrape(self, url):
        print('[蝦皮]讀取網頁資訊')
        driver.get(url) # 瀏覽器取得網頁連結
        time.sleep(5)
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword='): # 若網頁成功跳轉到目標頁面才開始執行
                    response = request.response
                    body = decode(response.body, response.headers.get('Content-Encoding', 'Identity'))
                    decode_body = body.decode('utf8')
                    json_data = json.loads(decode_body) # 將網頁資料全部存進json_data裡

                    data = []
                    rows = json_data['items'] # 總共獲取幾筆資料
                    for i in range(0, len(rows)): # 遍歷每一筆商品
                        product_name = json_data['items'][i]['item_basic']['name'] # 商品標題
                        price_min = str(json_data['items'][i]['item_basic']['price_min'])[:-5] # 商品最低價
                        price_max = str(json_data['items'][i]['item_basic']['price_max'])[:-5] # 商品最高價
                        historical_sold = json_data['items'][i]['item_basic']['historical_sold'] # 已售出
                        shop_id = json_data['items'][i]['item_basic']['shopid'] # 店家id
                        item_id = json_data['items'][i]['itemid'] # 商品id
                        link = f'https://shopee.tw/{product_name} -i.{shop_id}.{item_id}' # 商品連結

                        # 儲存資料: 商品標題 最低價 最高價 已售出數量 搜尋關鍵字 賣場名稱 當前搜尋時間 商品連結
                        data.append(
                            (product_name, price_min, price_max, historical_sold, self.keyword, self.store, self.time, link)
                        )
        print('[蝦皮]完成')
        return data
