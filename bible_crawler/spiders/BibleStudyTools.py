from bible_crawler.items import BibleCrawlerItem
from scrapy.http import Request
import warnings
import scrapy

warnings.filterwarnings('ignore')

class BibleStudyNIVSpider(scrapy.Spider):

    name = "niv_english"
    custom_settings = {
        'filename': 'holy_bible_niv_eng'
    }

    def start_requests(self):

        start_urls = [
            "https://www.biblestudytools.com/genesis/1.html"
            #"https://www.biblestudytools.com/genesis/10.html"
        ]

        for url in start_urls:
            yield Request(url=url, callback=self.parseBibleNIV)

    def joinVerse(self, verses):
        verses = [verse.strip() for verse in verses]
        verses = [verse for verse in verses if verse != '']
        return '-'.join([verses[0], ' '.join(verses[1:])])

    def parseBibleNIV(self, response):
        
        book = response.css('h1 ::text').get(default='not-found')

        for verse_ in response.css('div.scripture > div'):
            item = BibleCrawlerItem()

            item['book'] = book
            item['verse'] = self.joinVerse(verse_.css('span ::text').getall())
            item['version'] = 'niv'

            yield item
        
        if book != 'Revelation 22':
            next_cap_page = response.xpath('//*[@id="content-column"]/div[3]/div/div[5]/div/div/a[2]')\
                                    .css('::attr("href")')\
                                    .get(default='not-found')
            
            yield response.follow(url=next_cap_page, callback=self.parseBibleNIV)