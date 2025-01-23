# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from sqlalchemy.exc import DatabaseError

from models import Ads


class OlxPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        # session = self.Session()
        session = spider.session

        ad = Ads()
        ad.id_ads = item.get("id_ads")
        ad.posted_at = item.get("posted_at")
        ad.url = item.get("url"),
        ad.title=item.get("title"),
        ad.raw_price = item.get("raw_price")
        ad.price=item.get("price")
        ad.currency = item.get("currency")
        ad.phone = item.get("phone")
        ad.img_url = item.get("img_url")
        ad.type = item.get("type")
        ad.options = item.get("options")
        ad.delivery = item.get("delivery")
        ad.description=item.get("description")

        spider.logger.info(f"Processed: {ad}")
        try:
            session.add(ad)
            session.commit()
        except DatabaseError as e:
            session.rollback()
            spider.logger.error(f"Database Error: {e}")

        return item

    def close_spider(self, spider):
        pass
