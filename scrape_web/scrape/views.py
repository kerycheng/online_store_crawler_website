from django.shortcuts import render
from .models import products
from .scrape_shopee import scrape_shopee
from .scrape_ruten import scrape_ruten

import threading
import pandas as pd
import sqlite3
from datetime import datetime

# 網頁首頁
def index(request):
    # 如果有得到關鍵字和頁數
    if 'keyword' in request.GET:
        # 讀出關鍵字
        keyword = request.GET.get('keyword')
        # 讓頁數默認為2
        pages = 2
        # 檢查資料庫, 回傳找到的資料
        details = check_database(keyword, pages)
        print(details)

        return render(request, 'search.html', {'details': details})

    return render(request, 'index.html')

# 檢查資料庫
def check_database(keyword, pages):
    print(keyword)
    # 現在日期
    today = str(datetime.today().date())

    # 當如果table中的資料有包含到輸入的關鍵字, 並且資料更新時間是今天時, 直接將SQL內的資料回傳出來
    if products.objects.filter(title__icontains=keyword, time__contains=today):
        details = products.objects.filter(title__icontains=keyword, time__contains=today)

        return details

    # 當如果table中的資料沒有包含到輸入的關鍵字時, 或是資料更新時間不是今天時, 則開始執行爬蟲
    else:
        # 蝦皮爬蟲多線程
        thread_scrape_shopee = threading.Thread(target=scrape_shopee_controller, args=(keyword, pages))
        thread_scrape_shopee.start()

        # 露天爬蟲多線程
        thread_scrape_ruten = threading.Thread(target=scrape_ruten_controller, args=(keyword, pages))
        thread_scrape_ruten.start()

        # 當蝦皮爬蟲完成
        thread_scrape_shopee.join()
        # 當露天爬蟲完成
        thread_scrape_ruten.join()

        # 把剛才爬好的資料讀取出來
        details = products.objects.filter(title__icontains=keyword, time__contains=today)

        return details

# 執行蝦皮爬蟲
def scrape_shopee_controller(keyword, pages):
    # 宣告scrape_shopee物件
    ss = scrape_shopee(keyword, pages)
    # 獲取關鍵字連結
    urls = ss.get_url()
    # 儲存資料用的陣列
    dt_all = []
    # 遍歷每一個連結的商品資訊
    for i in range(0, len(urls)):
        # 獲取商品資訊
        scrapes = ss.scrape(urls[i])
        print(scrapes)
        # 將資訊存進dt_all
        dt_all.extend(scrapes)

    df2sql(dt_all)

# 執行露天爬蟲
def scrape_ruten_controller(keyword, pages):
    # 宣告scrape_ruten物件
    sr = scrape_ruten(keyword, pages)
    # 獲取關鍵字連結
    urls = sr.get_url()
    # 儲存資料用的陣列
    dt_all = []
    # 遍歷每一個連結的商品資訊
    for i in range(0, len(urls)):
        # 獲取商品資訊
        scrapes = sr.scrape(urls[i])
        # 將資訊存進dt_all
        dt_all.extend(scrapes)

    df2sql(dt_all)

def df2sql(data):
    # 建立dataframe '商品標題', '商品最低價', '商品最高價', '已售出', '關鍵字', '賣場名稱', '資料建立時間', '商品連結'
    df = pd.DataFrame(data, columns=['title', 'price_min', 'price_max', 'sold', 'keyword', 'store', 'time', 'link'])
    # 連結資料庫
    conn = sqlite3.connect('db.sqlite3')
    # 將df的資料倒進scrape_products的table裡, 並且當表已存在的話則用添加資料
    df.to_sql('scrape_products', conn, if_exists='append', index=False)
    conn.close()