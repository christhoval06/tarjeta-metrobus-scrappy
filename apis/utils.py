import collections

from twisted.internet.defer import Deferred
from scrapy import signals


def scrape_items(crawler_runner, crawler_or_spidercls, *args, **kwargs):
    """
    Start a crawl and return an object (ItemCursor instance)
    which allows to retrieve scraped items and wait for items
    to become available.

    Example:

    .. code-block:: python

        @inlineCallbacks
        def f():
            runner = CrawlerRunner()
            async_items = scrape_items(runner, my_spider)
            while (yield async_items.fetch_next):
                item = async_items.next_item()
                # ...
            # ...

    This convoluted way to write a loop should become unnecessary
    in Python 3.5 because of ``async for``.
    """
    # this requires scrapy >= 1.1rc1
    crawler = crawler_runner.create_crawler(crawler_or_spidercls)
    # for scrapy < 1.1rc1 the following code is needed:
    # crawler = crawler_or_spidercls
    # if not isinstance(crawler_or_spidercls, Crawler):
    #    crawler = crawler_runner._create_crawler(crawler_or_spidercls)

    d = crawler_runner.crawl(crawler, *args, **kwargs)
    return ItemCursor(d, crawler)


class ItemCursor(object):
    def __init__(self, crawl_d, crawler):
        self.crawl_d = crawl_d
        self.crawler = crawler

        crawler.signals.connect(self._on_item_scraped, signals.item_scraped)

        crawl_d.addCallback(self._on_finished)
        crawl_d.addErrback(self._on_error)

        self.closed = False
        self._items_available = Deferred()
        self._items = collections.deque()

    def _on_item_scraped(self, item):
        print('Item')
        self._items.append(item)
        self._items_available.callback(True)
        self._items_available = Deferred()

    def _on_finished(self, result):
        self.closed = True
        self._items_available.callback(False)

    def _on_error(self, failure):
        self.closed = True
        self._items_available.errback(failure)

    @property
    def fetch_next(self):
        """
        A Deferred used with ``inlineCallbacks`` or ``gen.coroutine`` to
        asynchronously retrieve the next item, waiting for an item to be
        crawled if necessary. Resolves to ``False`` if the crawl is finished,
        otherwise :meth:`next_item` is guaranteed to return an item
        (a dict or a scrapy.Item instance).
        """
        print('fetch_next', self.closed, self._items, self._items_available)
        if self.closed:
            # crawl is finished
            d = Deferred()
            d.callback(False)
            return d

        if self._items:
            # result is ready
            d = Deferred()
            d.callback(True)
            return d

        # We're active, but item is not ready yet. Return a Deferred which
        # resolves to True if item is scraped or to False if crawl is stopped.
        return self._items_available

    def next_item(self):
        """Get a document from the most recently fetched batch, or ``None``.
        See :attr:`fetch_next`.
        """
        if not self._items:
            return None
        return self._items.popleft()
