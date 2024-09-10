import sys
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from pydispatch import dispatcher

class TextSpider(scrapy.Spider):
    name = "text_spider"

    def __init__(self, urls=None, *args, **kwargs):
        super(TextSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls
        self.collected_texts = []

    def parse(self, response):
        text = response.xpath('//body//text()').getall()
        text = ' '.join(text).strip()
        self.collected_texts.append(text)
        yield {'text': text}

def scrape_texts_from_urls(urls):
    process = CrawlerProcess(settings={"LOG_LEVEL": "ERROR"})
    results = []

    def item_scraped(item, response, spider):
        results.append(item['text'])

    dispatcher.connect(item_scraped, signal=signals.item_scraped)
    process.crawl(TextSpider, urls=urls)
    process.start()

    return results

if __name__ == "__main__":
    # URLs are passed in as a JSON-encoded list in the command line argument
    urls = json.loads(sys.argv[1])
    texts = scrape_texts_from_urls(urls)
    
    # Return the scraped texts as JSON
    print(json.dumps(texts))
