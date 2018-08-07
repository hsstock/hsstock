
from sqlalchemy import Column, Enum, SMALLINT,String, BigInteger,Date,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SysSharding(Base):
    __tablename__ = 'sys_sharding'

    code = Column(String,primary_key=True)
    dtype = Column(Enum('hk','hk_5m'))
    tindex = Column(SMALLINT)
    lastdate = Column(Date)

    def __repr__(self):
        return "<sys_sharding(code={},dtype={},tindex={})>".format(self.code, self.dtype,self.tindex)


if __name__ == '__main__':
    print(SysSharding.__table__)