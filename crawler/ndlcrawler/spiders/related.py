from pathlib import Path
import json

import scrapy

IDLIST = Path(__file__).parent / '../../ids.txt'
TARGET_COLLECTIONS = {f"A0000{n}" for n in range(3, 8 + 1)}

RELATED_URL = "https://dl.ndl.go.jp/api/item/related/info:ndljp/pid/"

class ReleatedSpider(scrapy.Spider):
    name = "related"
    allowed_domains = ["dl.ndl.go.jp"]
    # start_urls = ["https://dl.ndl.go.jp/pid/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(IDLIST, 'r') as f:
            ids = f.read()
        ids = sorted(map(int, ids.splitlines()))
        self.logger.info(f"Known ids: {len(ids)}")
        self.ids = set(ids)
        

    def start_requests(self):
        for i in self.ids:
            yield scrapy.Request(RELATED_URL + str(i), meta={'i': i})

    def parse(self, response):
        i = response.meta['i']
        self.logger.debug(f"Checking {i}")
        d = json.loads(response.text)
        if d.get('success') == False:
            return
        for entry in d:
            for item in d.get('list', []):
                if 'itemId' in item:
                    ri = int(item['itemId'])
                    if any(clc in TARGET_COLLECTIONS for clc in item.get('collections', None) or []) and item.get('permission', {}).get('rule') == 'internet':
                        if ri not in self.ids:
                            assert item['pid'] == str(ri), str(ri)
                            assert item.get('permission', {}).get('type') == 'internet', str(i)
                            self.logger.info(f"RELATED: {i}")
