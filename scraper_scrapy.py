import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from pydispatch import dispatcher
from twisted.internet import reactor, defer

class TextSpider(scrapy.Spider):
    name = "text_spider"

    def __init__(self, url=None, *args, **kwargs):
        super(TextSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.collected_text = None  # Attribute to store the extracted text

    def parse(self, response):
        # Extract the text content of the entire page
        text = response.xpath('//body//text()').getall()
        text = ' '.join(text).strip()
        
        # Store the extracted text
        self.collected_text = text

        # Return the extracted text
        yield {'text': text}

@defer.inlineCallbacks
def scrape_text_from_url_scrapy(url):
    settings = {
        "LOG_LEVEL": "ERROR",  # Set log level to ERROR to reduce log output
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"  # Update to avoid deprecation warning
    }
    runner = CrawlerRunner(settings=settings)
    
    results = []
    
    def item_scraped(item, response, spider):
        results.append(item['text'])
    
    dispatcher.connect(item_scraped, signal=signals.item_scraped)
    
    yield runner.crawl(TextSpider, url=url)
    
    reactor.stop()
    
    return results[0] if results else None

def main():
    url = "http://example.com"  # Replace with your URL
    text = None
    
    def run_scrapy():
        nonlocal text
        text = scrape_text_from_url_scrapy(url)
    
    reactor.callWhenRunning(run_scrapy)
    reactor.run()
    
    print(text)

if __name__ == "__main__":
    main()



'''import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from pydispatch import dispatcher

class TextSpider(scrapy.Spider):
    name = "text_spider"

    def __init__(self, url=None, *args, **kwargs):
        super(TextSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.collected_text = None  # Attribute to store the extracted text

    def parse(self, response):
        # Extract the text content of the entire page
        text = response.xpath('//body//text()').getall()
        text = ' '.join(text).strip()
        
        # Store the extracted text
        self.collected_text = text

        # Return the extracted text
        yield {'text': text}

def scrape_text_from_url_scrapy(url):
    # Set up the CrawlerProcess with the desired settings
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR"  # Set log level to ERROR to reduce log output
    })
    
    # Set up a signal to catch the item scraped signal and store the result
    results = []
    
    def item_scraped(item, response, spider):
        results.append(item['text'])
    
    dispatcher.connect(item_scraped, signal=signals.item_scraped)
    
    # Schedule the spider for running with the given URL
    process.crawl(TextSpider, url=url)
    
    # Start the crawling process (it will block until all spiders are done)
    process.start()
    
    # Return the collected text
    return results[0] if results else None'''