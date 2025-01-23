from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ads = Column(Integer, index=True)
    url = Column(String)
    posted_at = Column(DateTime)
    title = Column(String)
    raw_price = Column(String)
    price = Column(Float)
    currency = Column(String)
    phone = Column(String)
    img_url = Column(String)
    type = Column(String)
    options = Column(String)
    delivery = Column(String)
    description = Column(String)
    views = Column(Integer)

    def __repr__(self):
        return f"<Ads(id_ads={self.id_ads} | title={self.title}, price={self.raw_price}, posted_at={self.posted_at})>"

