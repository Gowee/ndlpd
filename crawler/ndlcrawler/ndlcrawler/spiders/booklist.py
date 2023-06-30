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
        sort_key=None,
        order=None,
        year=None,
        collection_facet=None,
        title=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.classic_facet = classic_facet
        self.sort_key = sort_key
        self.order = order
        self.year = None
        if year and "-" in year:
            self.year = tuple(year.split("-", maxsplit=1))
        elif year is not None:
            self.year = (year, year)
        self.collection_facet = collection_facet
        self.title = title

    def start_requests(self):
        yield scrapy.http.JsonRequest(URL_LIST, data=genparams(1, self.classic_facet, self.sort_key, self.order, self.year, self.collection_facet, self.title), meta={'page': 1})

    def parse(self, response):
        page = response.meta['page']
        self.logger.info(f"Fetched page {page}")
        d = json.loads(response.text)
        if d.get('success') == False:
            self.logger.info(f"Ended at {page}")
            return
        if not d.get('searchHits'):
            self.logger.info(f"No more books on {page}")
            return
        for item in d['searchHits']:
            self.logger.info(f"VALID_ID: " + item['id'])
        page += 1
        yield scrapy.http.JsonRequest(URL_LIST, data=genparams(page, self.classic_facet, self.sort_key, self.order, self.year, self.collection_facet, self.title), meta={'page': page})

def genparams(page, classic_facet=None, sort_key=None, order=None, year=None, collection_facet=None, title=None):
    null = None
    true = True
    false = False
    params = {"collection":["A00003"],"accessRestrictions":["internet"],"keyword":"","title":"","creator":"","publisher":"","eraType":null,"collectionEraType":null,"publicationPlace":"","tableOfContents":"","ndc":[],"ndlc":"","identifierItem":"PID","identifier":"","callNumber":"","subject":"","subCollection":[],"kotenSubject":"","classicMaterialTypeList":[],"classicManuscriptionList":[],"provenance":"","series":"","musicType":"","subjectKanpo":"","volumeSubtitle":"","partTitleKanpo":"","partTitleKanpoNumber":"","federalRegisterTypeList":[],"volumeFederalRegisterItemType":"","volumeFederalRegister":"","publicationName":"","publicationVolume":"","description":"","provider":"","bibliographicLevel":[],"pageNum":page,"pageSize":"100","sortKey":"SCORE","order":"DESC","fullText":true,"pid":"","bibId":"","releaseNumber":"","permission_facet":["internet"],"excludeVolumeNum":false}
    if classic_facet is not None:
        params['classic_facet'] = [classic_facet]
    if sort_key is not None:
        params['sort_key'] = sort_key # e.g. CALL_NUMBER
    if order is not None:
        params['order'] = order # DESC
    if year is not None:
        params['fromYear_facet'] = year[0]
        params['toYear_facet'] = year[1]
    if collection_facet is not None:
        params['collection_facet'] = [collection_facet]
    if title is not None:
        params['title'] = title
        
    return params
