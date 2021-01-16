import scrapy


class MyItem(scrapy.Item):
    names = scrapy.Field()
    reviewerLink = scrapy.Field()
    reviewTitles = scrapy.Field()
    reviewBody = scrapy.Field()
    verifiedPurchase = scrapy.Field()
    postDate = scrapy.Field()
    starRating = scrapy.Field()
    helpful = scrapy.Field()
    nextPage = scrapy.Field(default='null')


class ReviewspiderSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ["amazon.in"]
    start_urls = [
        "https://www.amazon.in/SanDisk-Cruzer-Blade-Flash-Drive/dp/B005FYNT3G?pf_rd_r=1W70BFZPN5EG28PWZE5R&pf_rd_p=406d1302-20ad-5b8d-a279-43ce0bfbba6f&pd_rd_r=c64162e5-4da0-4b63-acd2-83963ed57401&pd_rd_w=z1E5E&pd_rd_wg=HvMvr&ref_=pd_gw_ri"]

    # This will tell scrapy to store the scraped data to outputfile.json and for how long the spider should run.
    custom_settings = {
        'FEED_URI': 'spiders/outputfile.json',
        'CLOSESPIDER_TIMEOUT': 15
    }

    def parse(self, response):
        # This will get the link for the all reviews tag on amazon page.
        all_reviews = response.xpath(
            '//div[@data-hook="reviews-medley-footer"]//a[@data-hook="see-all-reviews-link-foot"]/@href').extract_first()
        # This will tell scrapy to move to all reviews page for further scraping.
        yield response.follow("https://www.amazon.in" + all_reviews, callback=self.parse_page)

    def parse_page(self, response):
        # Scraping all the items for all the reviewers mentioned on that Page
        names = response.xpath('//div[@data-hook="review"]//span[@class="a-profile-name"]/text()').extract()
        reviewerLink = response.xpath('//div[@data-hook="review"]//a[@class="a-profile"]/@href').extract()
        reviewTitles = response.xpath('//a[@data-hook="review-title"]/span/text()').extract()
        reviewBody = response.xpath('//span[@data-hook="review-body"]/span').xpath('normalize-space()').getall()
        verifiedPurchase = response.xpath('//span[@data-hook="avp-badge"]/text()').extract()
        postDate = response.xpath('//span[@data-hook="review-date"]/text()').extract()
        starRating = response.xpath('//i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()').extract()
        helpful = response.xpath('//span[@class="cr-vote"]//span[@data-hook="helpful-vote-statement"]/text()').extract()

        # Extracting details of each reviewer and storing it in in the MyItem object items and then appending it to the JSON file.

        for (name, reviewLink, title, Review, Verified, date, rating, helpful_count) in zip(names, reviewerLink,
                                                                                            reviewTitles, reviewBody,
                                                                                            verifiedPurchase, postDate,
                                                                                            starRating, helpful):
            # Getting the Next Page URL for futher scraping.
            next_urls = response.css('.a-last > a::attr(href)').extract_first()

            item = MyItem(names=name, reviewerLink=reviewLink, reviewTitles=title, reviewBody=Review,
                          verifiedPurchase=Verified, postDate=date, starRating=rating, helpful=helpful_count,
                          nextPage=next_urls)
            yield item

        # This will get the next psge URL
        next_page = response.css('.a-last > a::attr(href)').extract_first()
        # Checking if next page is not none then loop back in the same function with the next page URL.
        if next_page is not None:
            yield response.follow("https://www.amazon.in" + next_page, callback=self.parse_page)
