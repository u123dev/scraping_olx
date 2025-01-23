import time
import requests
import scrapy
from scrapy.utils import spider
from sqlalchemy.orm import sessionmaker

from olx import db
from olx.models import Ads

from olx.spiders.utils import convert_to_date, convert_to_num


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["www.olx.ua", ]
    start_urls = ["https://www.olx.ua/list/", ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # init
        self.page_limit = 5
        self.current_page = 0

        engine = db.db_connect()
        db.create_table(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def parse(self, response: scrapy.http.Response) -> scrapy.http.Response:
        ids = response.css("div.css-l9drzq::attr(id)").getall()
        olx_page_links = response.css("div.css-1ut25fa a.css-qo0cxu::attr(href)")[:2]

        for n, link in enumerate(olx_page_links):
            # check if id exist in db
            if self.session.query(Ads).filter(Ads.id_ads == ids[n]).first():
                spider.logger.info(f"Ads ID: {ids[n]}  already exists in db")
                continue
            yield response.follow(link, callback=self.parse_ads, meta={"id_ads": ids[n]})

        next_page_url = response.css('a[data-testid="pagination-forward"]::attr(href)').get()
        if next_page_url and self.current_page < self.page_limit:
            self.current_page += 1
            yield response.follow(next_page_url, self.parse)

    def parse_ads(self, response: scrapy.http.Response) -> dict:
        url = response.url
        id_ads = str(response.meta["id_ads"])
        raw_price = response.css("div[data-testid='ad-price-container'] h3::text").get()
        price, currency = convert_to_num(raw_price)

        # API for getting phones
        # !!! Uncomment & Use next code with Proxy only, cause ip ban will be used
        api_phone = f"https://www.olx.ua/api/v1/offers/{id_ads}/limited-phones/"
        response_phone = None
        # response_phone = requests.get(api_phone)
        # time.sleep(0.5)

        if response_phone and response_phone.status_code == 200 and response_phone.headers["Content-Type"].startswith("application/json"):
            data_phone = response_phone.json()
            phones = ",".join(data_phone.get("data", {}).get("phones")).replace(" ","")
        else:
            phones = ""

        yield {
            "id_ads": id_ads,
            "url": url,
            "posted_at": convert_to_date(response.css("span[data-cy='ad-posted-at']::text").get()),  # Сегодня в 16:59
            "title": response.css("div[data-cy='ad_title'] h4::text").get(),
            "raw_price": raw_price,
            "price": price,
            "currency": currency,
            "phone": phones,
            "img_url": response.css("img.css-1bmvjcs::attr(src)").getall(),  # list of images
            "type": response.css("ul.css-rn93um li p span::text").get(),
            "options": response.css("ul.css-rn93um li p::text").getall(),
            "delivery": response.css("div[data-testid='courier-btn']::text").get(),
            "description": response.css("div.css-1o924a9::text").getall(),
        }

    def close_spider(self, response: scrapy.http.Response) -> None:
        self.session.close()
