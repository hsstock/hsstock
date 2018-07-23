
from sqlalchemy import Column, Integer, String, BigInteger,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FTStockBasicInfo(Base):
    __tablename__ = 'ft_stock_basicinfo'

    code = Column(String,primary_key=True)
    name = Column(String)
    lot_size = Column(BigInteger)
    stock_type = Column(String)
    stock_child_type = Column(String)
    stock_owner = Column(String)
    listing_date = Column(Date)
    stock_id = Column(BigInteger)

    def __repr__(self):
        return "<ft_stock_basicinfo(code={},name={})>".format(self.code, self.name)


if __name__ == '__main__':
    print(FTStockBasicInfo.__table__)