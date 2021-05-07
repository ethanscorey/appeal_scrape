import re
import io


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


from ..items import Article


class AppealSpider(CrawlSpider):
    name = "appeal"
    allowed_domains = ["theappeal.org"]
    start_urls = [
        "http://theappeal.org",
    ]

    rules = [
        Rule(LinkExtractor(
            allow='/topic/',
        )),
        Rule(LinkExtractor(
            allow='/region/'
        )),
        Rule(LinkExtractor(
            allow="/authors/"
        )),
        Rule(LinkExtractor(
            deny='^mailto'
            ),
             callback='parse_article'
        )
    ]

    def parse_article(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.xpath('//article/h1//text()').get()

        text = response.xpath('//article').get()
        text = re.sub(r'<iframe.+</iframe>', '', text)
        article['text'] = re.sub(r'="/', r'="https://theappeal.org/', text)

        if article['title'] is not None:
            with io.open(self.hash_title(article['title']),
                         'w',
                         encoding='utf-8') as f:
                f.write('<head><meta charset="utf-8"></head>')
                f.write(article['text'])

    @staticmethod
    def hash_title(title):
        if title is not None:
            return re.sub(r'\W', '', title) + ".html"



