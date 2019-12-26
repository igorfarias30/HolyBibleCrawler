from bible_crawler.items import BibleCrawlerItem
from scrapy.http import Request
import warnings
import scrapy
import re

warnings.filterwarnings('ignore')

class AlmeidaCorrigidaSpider(scrapy.Spider):

    name = "almeida_corrigida"
    custom_settings = {
        'filename': 'holy_bible_portuguese'
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

        if book != 'Apocalipse 22':
            next_cap_page = response.css('button a::attr("href")').getall()[-1]
            yield response.follow(url=next_cap_page, callback=self.parseBibliaOnline)


class KingJamesSpider(scrapy.Spider):

    name = "king_james"
    custom_settings = {
        'filename': 'holy_bible_kj_english'
    }

    def start_requests(self):

        start_urls = [
            "https://www.kingjamesbibleonline.org/Genesis-Chapter-1"
        ]

        for url in start_urls:
            yield Request(url=url, callback=self.parseKingJamesOnline)
    
    def joinVerses(self, verses):
        verses = [verse.strip() for verse in verses]
        return '-'.join([verses[0], ' '.join(verses[1:])])

    def parseKingJamesOnline(self, response):

        book = ' '.join(response.css('div.chapters_div_in h3 ::text').getall()).strip()
        book = re.sub(r"([\t\r\n])", "", book)

        for verse_ in response.css('div.in_slider p'):
            yield BibleCrawlerItem(book=book,
                                    verse=self.joinVerses(verse_.css('::text').getall()),
                                    version="king_james")

        if book != 'Revelation Chapter 22':
            next_cap_page = response.css('div.right_buttons a ::attr("href")').get(default=None)
            if next_cap_page:
                yield response.follow(url=response.urljoin(next_cap_page), 
                                    callback=self.parseKingJamesOnline)
            else:
                exit(f"An error occured in a moment to get the next link in the page {response.url}.")