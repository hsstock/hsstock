
from sqlalchemy import Column, Integer, String, BigInteger,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FTPlateStock(Base):
    __tablename__ = 'ft_plate_stock'

    code = Column(String,primary_key=True)
    lot_size = Column(BigInteger)
    stock_name = Column(String)
    stock_owner = Column(String)
    stock_child_type = Column(String)
    stock_type = Column(String)
    list_time = Column(Date)
    stock_id = Column(BigInteger)

    def __repr__(self):
        return "{},{},{}".format(self.code, self.plate_name,self.plate_id)


if __name__ == '__main__':
    print(FTPlateStock.__table__)