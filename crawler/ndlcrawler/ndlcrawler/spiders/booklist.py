import scrapy
import json

URL_LIST = "https://dl.ndl.go.jp/api/item/search"

class BooklistSpider(scrapy.Spider):
    name = "booklist"
    allowed_domains = ["dl.ndl.go.jp"]
    # start_urls = ["https://dl.ndl.go.jp"]

    def __init__(
        self,
        classic_facet=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.classic_facet = classic_facet

    def start_requests(self):
        yield scrapy.http.JsonRequest(URL_LIST, data=genparams(1, self.classic_facet), meta={'next_page': 2})

    def parse(self, response):
        page = response.meta['next_page']
        self.logger.info(f"Fetched page {page}")
        d = json.loads(response.text)
        if d.get('success') == False:
            logger.info(f"Ended at {page}")
            return
        if not d.get('searchHits'):
            logger.info(f"No more books on {page}")
        for item in d['searchHits']:
            self.logger.info(f"VALID_ID: " + item['id'])
        yield scrapy.http.JsonRequest(URL_LIST, data=genparams(page, self.classic_facet), meta={'next_page': page + 1})

def genparams(page, classic_facet=None):
    null = None
    true = True
    false = False
    params = {"collection":["A00003"],"accessRestrictions":["internet"],"keyword":"","title":"","creator":"","publisher":"","eraType":null,"collectionEraType":null,"publicationPlace":"","tableOfContents":"","ndc":[],"ndlc":"","identifierItem":"PID","identifier":"","callNumber":"","subject":"","subCollection":[],"kotenSubject":"","classicMaterialTypeList":[],"classicManuscriptionList":[],"provenance":"","series":"","musicType":"","subjectKanpo":"","volumeSubtitle":"","partTitleKanpo":"","partTitleKanpoNumber":"","federalRegisterTypeList":[],"volumeFederalRegisterItemType":"","volumeFederalRegister":"","publicationName":"","publicationVolume":"","description":"","provider":"","bibliographicLevel":[],"pageNum":page,"pageSize":"100","sortKey":"SCORE","order":"DESC","fullText":true,"pid":"","bibId":"","releaseNumber":"","permission_facet":["internet"],"excludeVolumeNum":false}
    if classic_facet:
        params['classic_facet'] = [classic_facet]
    return params
