from pathlib import Path
import json

import scrapy

IDLIST = Path(__file__).parent / '../../ids.txt'
TARGET_COLLECTIONS = {f"A0000{n}" for n in range(3, 8 + 1)}

BOOK_INFO_URL = "https://dl.ndl.go.jp/api/item/search/info:ndljp/pid/"
RIGHT_SIBLINGS = LEFT_SIBLINGS = 100

class MissingslotSpider(scrapy.Spider):
    name = "missingslot"
    allowed_domains = ["dl.ndl.go.jp"]
    # start_urls = ["https://dl.ndl.go.jp/pid/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(IDLIST, 'r') as f:
            ids = f.read()
        ids = sorted(map(int, ids.splitlines()))
        self.slots = find_slots(ids)
        # self.i = 0
        self.logger.info(f"Known ids: {len(ids)}")
        self.ids = set(ids)
        

    def start_requests(self):
        cnt = 0
        for sl, ss in self.slots: ## len, start of slot
            sl, ss = next(self.slots) 
            for i in siblings(sl, ss):
                yield scrapy.Request(BOOK_INFO_URL + str(i), callback=self.parse, meta={'i': i})
            cnt += 1
        self.logger.info(f"{cnt} slot blocks enumerated, no more middle slots to check")


    def parse(self, response):
        i = response.meta['i']
        self.logger.debug(f"Checking {i}")
        d = json.loads(response.text)['item']
        if d.get('success') != False and any(clc in TARGET_COLLECTIONS for clc in d.get('collections', None) or []) and d.get('permission', {}).get('rule') == 'internet':
            assert d.get('permission', {}).get('type') == 'internet', str(i)
            assert i not in self.ids, str(i)
            self.logger.info(f"RETRIEVED: {i}")

def find_slots(ids):
    for i, j in zip(ids, ids[1:]):
        if j - i > 1:
            yield j - i - 1, i + 1

def siblings(sl, ss):
    if sl > RIGHT_SIBLINGS + LEFT_SIBLINGS:
        for i in range(ss, ss + RIGHT_SIBLINGS):
            yield i
        for i in range(ss + sl - LEFT_SIBLINGS, ss + sl):
            yield i
    else:
        for i in range(ss, ss + sl):
            yield i