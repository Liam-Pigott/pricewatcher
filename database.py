import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Watcher(Base):
    '''
    Watcher table holds the required details to scrape prices.
    Columns: id, name, url, xpath
    PK: id
    '''
    __tablename__ = 'Watcher'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(300), nullable=False)
    xpath = Column(String(300), nullable=False)
    def __repr__(self):
        return 'Watcher(id={}, name={}, url={}, xpath={}'.format(self.id, self.name, self.url, self.xpath)

class Price(Base):
    '''
    Price entries for a given watcher at a time
    Columns: id, watcher_id, price, date
    PK: id
    '''
    __tablename__ = 'Price'
    id = Column(Integer, primary_key=True)
    watcher_id = Column(Integer, ForeignKey('Watcher.id', name='FK__Price__Watcher'))
    price = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)
    watcher = relationship('Watcher', back_populates = 'price')
    def __repr__(self):
        return 'Price(id={}, watcher_id={}, date_time={}'.format(self.id, self.watcher_id, self.date_time)

Watcher.price = relationship('Price', order_by = Price.id, back_populates = 'watcher')

def setup_db_session():
    db_url = generate_db_url()
    engine = create_engine(db_url, echo = True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()

def generate_db_url():
    env = os.environ
    return "mysql://{user}:{pwd}@{host}/{database}".format(
        user=env.get('PRICEWATCH_MYSQL_USER'),
        pwd=env.get('PRICEWATCH_MYSQL_PASS'),
        host=env.get('PRICEWATCH_MYSQL_HOST'),
        database=env.get('PRICEWATCH_MYSQL_DATABASE'))

def commit_price(watcher_id, price, session):
    price_object = Price(watcher_id=watcher_id, price=price, date_time=datetime.now())
    session.add(price_object)
    session.commit()

def commit_prices(prices, session):
    session.add_all(prices)
    session.commit()