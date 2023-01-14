# 網拍賣場搜尋網站 Online Store Crawler Website
更新日期： 2023/1/14

* [概述](#overview)  
  * [專案前身](#previous)
  * [說明](#illustrate)
* [環境介紹](#env)
* [程式架構](#architecture)
* [程式說明](#program)
* [資料說明](#data)

<h2 id="overview">概述</h2>

<h3 id="previous">專案前身：</h3>
本專案是從之前做的這個專案變化而來，對爬蟲功能稍加修改，有興趣的也可以去參考看看

[網拍賣場爬蟲程式](https://github.com/kerycheng/onlineshop_crawler)

<h3 id="illustrate">說明：</h3>
本專案透過Django框架與網路爬蟲做結合，並配合自帶的SQLite資料庫，實現了簡易的網拍賣場爬蟲搜尋網站。

<h2 id="env">基本環境</h3>

* 程式語言： `Python`
* 網頁框架： `Django`
* Web瀏覽器： `Selenium`
* 資料庫： `SQLite`

<h2 id="architecture">程式架構</h2>

![image](https://imgur.com/C6Uedqp.jpg) 

<h2 id="program">程式說明</h2>
當在首頁上輸入商品關鍵字之後，如下圖所示

![image](https://imgur.com/6Ktit71.jpg)

後台會先把關鍵字與資料庫的資料進行比對
* 若有資料包含此關鍵字資料"且"資料更新日期為最新日期(今日)，便會將資料顯示於結果頁面。
* 若查無包含此關鍵字資料"或"資料更新日期不是最新日期，則會先進行一次爬蟲更新資料庫之後，再將資料顯示於結果頁面。

結果頁面如下圖所示

![image](https://imgur.com/3xP213Q.jpg)

使用者可透過點擊欄位來進行資料排序，並且每樣商品的標題都附帶賣場超連結，可直接點擊進入商品頁面。

<h2 id="data">資料說明</h2>
爬蟲所爬取的資料有：

* 商品標題(title)
* 最低售價(price_min)
* 最高售價(price_max)
* 已賣出數量(sold)
* 關鍵字(keyword)
* 賣場網站(store)
* 資料更新日期(time)
* 商品連結(link)

![image](https://imgur.com/sDZ2Wgm.jpg)
