from abc import ABC

from sqlalchemy import Column, Integer, String, BigInteger,Date,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FTHistoryBase(object):

    code = Column(String, primary_key=True)
    time_key = Column(DateTime)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    pe_ratio = Column(Float)
    turnover_rate = Column(Float)
    volume = Column(BigInteger)
    turnover = Column(Float)
    change_rate = Column(Float)
    last_close = Column(Float)

    def __repr__(self):
        return "<ft_history_kline(code={},time_key={},open={},close={})>".format(self.code, self.time_key, self.open,
                                                                                 self.close)


class FTHistoryKlineAll(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline'


class FTHistoryKline1(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_1'


class FTHistoryKline2(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_2'

class FTHistoryKline3(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_3'

class FTHistoryKline4(Base, FTHistoryBase):
    __tablename__ = 'ft_history_kline_4'

class FTHistoryKline5(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_5'

class FTHistoryKline6(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_6'

class FTHistoryKline7(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_7'

class FTHistoryKline8(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_8'

class FTHistoryKline9(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_9'

class FTHistoryKline10(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_10'

class FTHistoryKline11(Base,FTHistoryBase):
    __tablename__ = 'ft_history_kline_11'

def getClassByIndex(tindex):
    return globals()['FTHistoryKline{}'.format(tindex)]

if __name__ == '__main__':
    print(locals()['FTHistoryKline1'])
    cls = locals()['FTHistoryKline1']
    print(cls.__table__)
    print(FTHistoryKline1.__table__)

# pip3 install flask-sqlalchemy
# class FTHistoryKline(object):
#
#     _mapper = {}
#
#     @staticmethod
#     def model(code, dtype, storeservice):
#         table_index = storeservice.find_tindex(code,dtype)
#
#         class_name = 'FTHistoryKline_%d' % table_index
#
#         ModelClass = FTHistoryKline._mapper.get(class_name,None)
#         if ModelClass is None:
#             ModelClass = type(class_name, (db.Model,),{
#                 '__module__': __name__,
#                 '__name__': class_name,
#                 '__tablename__': ('ft_history_kline_%d' % table_index)
#             })
#
#             FTHistoryKline._mapper[class_name] = ModelClass
#
#             cls = ModelClass()
#             cls.code = code
#             return cls
#

# ,
#                 'code' = Column(String, primary_key=True),
#                 'time_key' = Column(DateTime),
#                 'open' = Column(Float),
#                 'close' = Column(Float),
#                 'high' = Column(Float),
#                 'low' = Column(Float),
#                 'pe_ratio' = Column(Float),
#                 'turnover_rate' = Column(Float),
#                 'volume' = Column(BigInteger),
#                 'turnover' = Column(Float),
#                 'change_rate' = Column(Float),
#                 'last_close' = Column(Float)