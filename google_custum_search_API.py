#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import json
import pickle
import copy
from googleapiclient.discovery import build

def search_image(api_key,cse_key,search_word,page_limit=10):
    # Google Customサーチ結果を取得
    s = build("customsearch","v1",developerKey = api_key)
    response = []
    startIndex = 1

    search_result = []

    for nPage in range(0,page_limit):
        print('reading page number :',nPage+1)

        try:
            response.append(s.cse().list(
                q = search_word,
                cx = cse_key,
                dateRestrict = 'w[1]',
                num = 10,
                searchType = "image",
                start = startIndex
                ).execute())

            startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")

        except Exception as e:
            print(e)

    today = datetime.today().strftime("%Y%m%d%H%M%S")

    with open('./data/google_api_response/'+today+'.pickle', mode='wb') as f:
        pickle.dump(response, f)

    for nRes in range(len(response)):
        if len(response[nRes]['items']) > 0:
            for item in response[nRes]['items']:
                search_result.append({
                    'page_url':item['image']['contextLink'],
                    'image_url':item['link'],
                    'title':item['title'],
                    'search_date':today
                })

    return search_result

def find_new_image_and_update(search_result):
    data_path = 'data/url_data.json'
    # jsonファイルが存在するなら読み込む
    if os.path.exists(data_path):
        with open(data_path,encoding='utf-8') as f:
            url_data = json.load(f)

    else:
        url_data = {}
    
    new_items = []
    
    for item in search_result:
        if not url_data.get(item['page_url']):
            new_items.append(copy.deepcopy(item))
            url_data[item['page_url']] = {
                'image_url':item['image_url'],
                'title':item['title'],
                'search_date':item['search_date']
            }

    with open(data_path,'w',encoding='utf-8') as f:
        json.dump(url_data,f,ensure_ascii=False,indent=2)

    return new_items

if __name__ == "__main__":
    GOOGLE_API_KEY = input("API key:")
    CUSTOM_SEARCH_ENGINE_ID = input("search engine id:")
    KEYWORD = input("search word:")

    search_result = search_image(GOOGLE_API_KEY,CUSTOM_SEARCH_ENGINE_ID,KEYWORD,page_limit=2)
    new_items = find_new_image_and_update(search_result)
    print(new_items)


