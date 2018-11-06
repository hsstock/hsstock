from abc import ABC

from sqlalchemy import Column, Integer, String, BigInteger,Date,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FTBase(object):

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
        print(self.time_key)
        return "({},{},{},{},{},{},{},{},{},{},{},{})".format(self.code,*self.time_key,self.open,self.close,self.high,self.low,self.pe_ratio,self.turnover_rate,self.volume,self.turnover,self.change_rate,self.last_close)


class FTKlineAll(Base,FTBase):
    __tablename__ = 'ft_kline'


class FTKline1(Base,FTBase):
    __tablename__ = 'ft_kline_1'


class FTKline2(Base,FTBase):
    __tablename__ = 'ft_kline_2'

class FTKline3(Base,FTBase):
    __tablename__ = 'ft_kline_3'

class FTKline4(Base, FTBase):
    __tablename__ = 'ft_kline_4'

class FTKline5(Base,FTBase):
    __tablename__ = 'ft_kline_5'

class FTKline6(Base,FTBase):
    __tablename__ = 'ft_kline_6'

class FTKline7(Base,FTBase):
    __tablename__ = 'ft_kline_7'

class FTKline8(Base,FTBase):
    __tablename__ = 'ft_kline_8'

class FTKline9(Base,FTBase):
    __tablename__ = 'ft_kline_9'

class FTKline10(Base,FTBase):
    __tablename__ = 'ft_kline_10'

class FTKline11(Base,FTBase):
    __tablename__ = 'ft_kline_11'

class FTKline12(Base,FTBase):
    __tablename__ = 'ft_kline_12'

class FTKline13(Base,FTBase):
    __tablename__ = 'ft_kline_13'

class FTKline14(Base,FTBase):
    __tablename__ = 'ft_kline_14'

class FTKline15(Base, FTBase):
    __tablename__ = 'ft_kline_15'

class FTKline16(Base,FTBase):
    __tablename__ = 'ft_kline_16'



def getHKClassByIndex(tindex):
    return globals()['FTKline{}'.format(tindex)]

if __name__ == '__main__':
    print(locals()['FTKline1'])
    cls = locals()['FTKline1']
    print(cls.__table__)
    print(FTKline1.__table__)

# pip3 install flask-sqlalchemy
# class FTKline(object):
#
#     _mapper = {}
#
#     @staticmethod
#     def model(code, dtype, storeservice):
#         table_index = storeservice.find_tindex(code,dtype)
#
#         class_name = 'FTKline_%d' % table_index
#
#         ModelClass = FTKline._mapper.get(class_name,None)
#         if ModelClass is None:
#             ModelClass = type(class_name, (db.Model,),{
#                 '__module__': __name__,
#                 '__name__': class_name,
#                 '__tablename__': ('ft_kline_%d' % table_index)
#             })
#
#             FTKline._mapper[class_name] = ModelClass
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