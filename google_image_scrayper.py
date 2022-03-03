import requests, lxml, re, datetime
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "sierra cup",
    "tbm": "isch",
    "ijn": "0",
}
url = "https://www.google.co.jp/search?q=%E3%82%B7%E3%82%A7%E3%83%A9%E3%82%AB%E3%83%83%E3%83%97&tbm=isch&hl=ja&tbs=qdr:w&authuser=0&sa=X&ved=0CAMQpwVqFwoTCJjRpf3al_YCFQAAAAAdAAAAABAD&biw=1263&bih=873"
html = requests.get(url, headers=headers)
html_contents = html.text

with open("sample.html",mode = 'w',encoding='utf-8') as f:
    f.write(html_contents)

soup = BeautifulSoup(html_contents, 'html.parser')

table = soup.select('table.IkMU6e')

for item in table:
    
    page_link = print(item.select('a[href]')[0].get('href'))
    image_link = print(item.select('img')[0].get('src'))
    item_title = item.select('span.fYyStc')[0].text)

#TO DO データの保存形式を考える
#1ページしか読み取れていないので、次のページもすすめるようにする　1秒待つように
