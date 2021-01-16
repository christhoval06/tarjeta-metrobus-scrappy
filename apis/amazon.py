import time

from crochet import run_in_reactor, wait_for_reactor
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerRunner

from flask_restx import Namespace, fields, Resource
from twisted.internet.defer import inlineCallbacks

from apis.utils import scrape_items
from tarjetametrobus.tarjetametrobus.spiders.tarjeta_metrobus__scraping import ReviewspiderSpider
from models.review import ReviewDAO

api = Namespace('amazon', description='Amazon operations')

ReviewModel = api.model('Todo', {
    "helpful": fields.String(required=True, description='The task details'),
    "names": fields.String(required=True, description='The task details'),
    "nextPage": fields.String(required=True, description='The task details'),
    "postDate": fields.String(required=True, description='The task details'),
    "reviewBody": fields.String(required=True, description='The task details'),
    "reviewTitles": fields.String(required=True, description='The task details'),
    "reviewerLink": fields.String(required=True, description='The task details'),
    "starRating": fields.String(required=True, description='The task details'),
    "verifiedPurchase": fields.String(required=True, description='The task details'),
})


@api.route('/reviews')
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    DAO = ReviewDAO()
    scrape_in_progress = False
    scrape_complete = False
    crawl_runner = CrawlerRunner()

    @api.doc('list_reviews')
    @api.marshal_list_with(ReviewModel)
    def get(self):
        """List all tasks"""
        self.scrape_complete = False
        self.scrape_in_progress = False

        if not self.scrape_in_progress:
            self.scrape_in_progress = True

        self.scrape_with_crochet()

        while not self.scrape_complete:
            print('scrape_complete', self.scrape_complete)
            # time.sleep(0.1)
        return self.DAO.reviews

    @run_in_reactor
    def scrape_with_crochet(self):
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)
        d = self.crawl_runner.crawl(ReviewspiderSpider)
        d.addCallback(self._on_finished)

    def _crawler_result(self, item, response, spider):
        self.DAO.create(item)

    def _on_finished(self, result):
        print('result', result)
        self._items_available.callback(False)
        self.scrape_complete = True
