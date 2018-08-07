
from sqlalchemy import Column, Integer, String, BigInteger,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FTPlateList(Base):
    __tablename__ = 'ft_plate_list'

    code = Column(String,primary_key=True)
    plate_name = Column(String)
    plate_id = Column(BigInteger)

    def __repr__(self):
        return "{},{},{}".format(self.code, self.plate_name,self.plate_id)


if __name__ == '__main__':
    print(FTPlateList.__table__)