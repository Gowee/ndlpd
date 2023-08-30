import json
import logging

import scrapy
from scrapy.dupefilters import RFPDupeFilter

BOOK_INFO_URL = "https://dl.ndl.go.jp/api/item/search/info:ndljp/pid/"


class NDLDupeFilter(RFPDupeFilter):

    def request_fingerprint(self, request):
        if id := request.meta.get("id"):
            id = str(id)
            assert request.url.endswith("/" + id)
            return id
        return super().request_fingerprint(request)


class AllIdSpider(scrapy.Spider):
    name = "allid"
    allowed_domains = ["dl.ndl.co.jp"]
    start_urls = ["https://ndl.com"]

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "FEEDS": {
            "allbooks.json": {
                "format": "jsonl",
                "encoding": "utf8",
                "overwrite": False,
                "store_empty": False,
            },
        },
        "DUPEFILTER_CLASS": "ndlcrawler.spiders.allid.NDLDupeFilter",
        "DUPEFILTER_DEBUG": True,
    }

    def __init__(self, *args, **kwargs):
        self.start = int(kwargs.get("start", 0))
        self.end = int(kwargs.get("end", 20000000))
        self.log(f"Start at {self.start} till {self.end}")

    def start_requests(self):
        for id in range(self.start, self.end + 1):
            yield scrapy.Request(
                BOOK_INFO_URL + str(id), callback=self.parse, meta={"id": id}
            )

    def parse(self, response):
        id = response.meta["id"]
        d = json.loads(response.text)
        if item := d.get("item"):
            yield item
        else:
            if d.get("status") == 404:
                self.log(f"{id} not existing", level=logging.DEBUG)
            else:
                self.log(f"failed to parse {id}: {d}", level=logging.WARN)
