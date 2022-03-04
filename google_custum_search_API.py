#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import json
from googleapiclient.discovery import build

GOOGLE_API_KEY = input("API key")
CUSTOM_SEARCH_ENGINE_ID = input("search engine id")
KEYWORD = input("search word")

if __name__ == '__main__':
    # Google Customサーチ結果を取得
    s = build("customsearch","v1",
    developerKey = GOOGLE_API_KEY)
    r = s.cse().list(q = KEYWORD,
    cx = CUSTOM_SEARCH_ENGINE_ID,
    lr = 'lang_ja',
    num = 10,
    searchType = "image",
    start = 1).execute()

    # レスポンスをjson形式で保存
    s = json.dumps(r, ensure_ascii = False, indent = 4)
    now = datetime.today().strftime("%Y%m%d%H%M%S")
    with open('./res_' + now + '.json', mode='w') as f:
        f.write(s)