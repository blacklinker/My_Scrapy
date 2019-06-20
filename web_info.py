import scrapy
from bs4 import BeautifulSoup
import re

class TheThingWant(scrapy.Spider):
    name = "MySpider"
    start_urls = [
        'https://www.sina.com.cn/'
    ]
    custom_settings = {
        'LOG_LEVEL': 'ERROR'
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        tags = soup.find_all('a', href=re.compile(r"sina.*\d{4}-\d{2}-\d{2}.*shtml$"))
        for tag in tags:
            url = tag.get('href')
            yield scrapy.Request(url, callback=self.details)

    def details(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        try:
            # Get title
            title = self.extract_title(soup)
            if title is None:
                raise Exception('Title not found for ' + response.url)
        except Exception as e:
            self.logger.error(str(e))

    def extract_title(self, soup):
        selectors = ['h1.main-title','h1.l_title',]
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                title = soup.select(selector)[0].text
                return title
