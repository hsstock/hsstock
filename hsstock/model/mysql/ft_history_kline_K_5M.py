
from sqlalchemy import Column, Integer, String, BigInteger,Date,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FTHistoryKline5MBase(object):

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
        return "<ft_history_kline_K_5M(code={},time_key={},open={},close={})>".format(self.code, self.time_key,
                                                                                      self.open, self.close)


class FTHistoryKline5MAll(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M'

class FTHistoryKline5M1(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_1'


class FTHistoryKline5M2(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_2'


class FTHistoryKline5M3(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_3'


class FTHistoryKline5M4(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_4'


class FTHistoryKline5M5(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_5'


class FTHistoryKline5M6(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_6'


class FTHistoryKline5M7(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_7'


class FTHistoryKline5M8(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_8'


class FTHistoryKline5M9(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_9'


class FTHistoryKline5M10(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_10'


class FTHistoryKline5M11(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_11'


class FTHistoryKline5M12(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_12'


class FTHistoryKline5M13(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_13'


class FTHistoryKline5M14(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_14'


class FTHistoryKline5M15(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_15'


class FTHistoryKline5M16(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_16'


class FTHistoryKline5M17(Base,FTHistoryKline5MBase):
    __tablename__ = 'ft_history_kline_K_5M_17'


def getClass5mByIndex(tindex):
    return globals()['FTHistoryKline5M{}'.format(tindex)]

if __name__ == '__main__':
    print(locals()['FTHistoryKline5M1'])
    cls = locals()['FTHistoryKline5M1']
    print(cls.__table__)
    print(FTHistoryKline5M1.__table__)



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