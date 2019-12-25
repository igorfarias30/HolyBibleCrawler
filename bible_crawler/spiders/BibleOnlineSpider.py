from bible_crawler.items import BibleCrawlerItem
from scrapy.http import Request
import warnings
import scrapy

warnings.filterwarnings('ignore')

class AlmeidaCorrigidaSpider(scrapy.Spider):

    name = "almeida_corrigida"
    custom_settings = {
        'filename': 'holy_bible'
    }

    def start_requests(self):

        start_urls = [
            "https://www.bibliaonline.com.br/acf/gn/1"
        ]

        for url in start_urls:
            yield Request(url=url, callback=self.parseBibliaOnline)

    def joinVerse(self, verses):
        return '-'.join([element for element in verses if element != ' '])
        
    def parseBibliaOnline(self, response):

        book = response.css('article > h1 ::text').get(default='not-found')
        for verse_ in response.css('article > div > div > p'):
            yield BibleCrawlerItem(book=book,
                                    verse=self.joinVerse(verse_.css('::text').getall()),
                                    version="almeida_corrigida_fiel")

        next_cap_page = response.css('button a::attr("href")').getall()[-1]
        yield response.follow(url=next_cap_page, callback=self.parseBibliaOnline)