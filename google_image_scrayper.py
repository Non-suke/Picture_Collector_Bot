import requests, lxml, re, datetime
from bs4 import BeautifulSoup


def search_and_scraype(query):

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    params = {
        "q" : query,
        "tbm": "isch",#isch:image search
        "qdr": "w", #y:past year,m:month,w:week,d:24 hours
        "num": "100"
    }
    url = "https://www.google.co.jp/search"
    html = requests.get(url, headers=headers,params=params)
    html_contents = html.text

    with open("sample.html",mode = 'w',encoding='utf-8') as f:
        f.write(html_contents)

    soup = BeautifulSoup(html_contents, 'html.parser')

    table = soup.select('table.IkMU6e')

    for item in table:
        
        page_link = print(item.select('a[href]')[0].get('href'))
        image_link = print(item.select('img')[0].get('src'))
        item_title = item.select('span.fYyStc')[0].text

    #TO DO データの保存形式を考える一旦csvとかで、そのうちなれたらDBにしたい
    #1ページしか読み取れていないので、次のページもすすめるようにする　1秒待つように

query = "シエラカップ"
search_and_scraype("シエラカップ")
