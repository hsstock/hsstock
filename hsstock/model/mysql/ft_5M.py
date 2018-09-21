
from sqlalchemy import Column, Integer, String, BigInteger,Date,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FT5MBase(object):

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
        return "<ft_5M(code={},time_key={},open={},close={})>".format(self.code, self.time_key,
                                                                                      self.open, self.close)


class FT5MAll(Base,FT5MBase):
    __tablename__ = 'ft_5M'

class FT5M1(Base,FT5MBase):
    __tablename__ = 'ft_5M_1'


class FT5M2(Base,FT5MBase):
    __tablename__ = 'ft_5M_2'


class FT5M3(Base,FT5MBase):
    __tablename__ = 'ft_5M_3'


class FT5M4(Base,FT5MBase):
    __tablename__ = 'ft_5M_4'


class FT5M5(Base,FT5MBase):
    __tablename__ = 'ft_5M_5'


class FT5M6(Base,FT5MBase):
    __tablename__ = 'ft_5M_6'


class FT5M7(Base,FT5MBase):
    __tablename__ = 'ft_5M_7'


class FT5M8(Base,FT5MBase):
    __tablename__ = 'ft_5M_8'


class FT5M9(Base,FT5MBase):
    __tablename__ = 'ft_5M_9'


class FT5M10(Base,FT5MBase):
    __tablename__ = 'ft_5M_10'


class FT5M11(Base,FT5MBase):
    __tablename__ = 'ft_5M_11'


class FT5M12(Base,FT5MBase):
    __tablename__ = 'ft_5M_12'


class FT5M13(Base,FT5MBase):
    __tablename__ = 'ft_5M_13'


class FT5M14(Base,FT5MBase):
    __tablename__ = 'ft_5M_14'


class FT5M15(Base,FT5MBase):
    __tablename__ = 'ft_5M_15'


class FT5M16(Base,FT5MBase):
    __tablename__ = 'ft_5M_16'


class FT5M17(Base,FT5MBase):
    __tablename__ = 'ft_5M_17'


def getClass5mByIndex(tindex):
    return globals()['FT5M{}'.format(tindex)]

class FT5M18(Base,FT5MBase):
	__tablename__ = 'ft_5M_18'


class FT5M19(Base,FT5MBase):
	__tablename__ = 'ft_5M_19'


class FT5M20(Base,FT5MBase):
	__tablename__ = 'ft_5M_20'


class FT5M21(Base,FT5MBase):
	__tablename__ = 'ft_5M_21'


class FT5M22(Base,FT5MBase):
	__tablename__ = 'ft_5M_22'


class FT5M23(Base,FT5MBase):
	__tablename__ = 'ft_5M_23'


class FT5M24(Base,FT5MBase):
	__tablename__ = 'ft_5M_24'


class FT5M25(Base,FT5MBase):
	__tablename__ = 'ft_5M_25'


class FT5M26(Base,FT5MBase):
	__tablename__ = 'ft_5M_26'


class FT5M27(Base,FT5MBase):
	__tablename__ = 'ft_5M_27'


class FT5M28(Base,FT5MBase):
	__tablename__ = 'ft_5M_28'


class FT5M29(Base,FT5MBase):
	__tablename__ = 'ft_5M_29'


class FT5M30(Base,FT5MBase):
	__tablename__ = 'ft_5M_30'


class FT5M31(Base,FT5MBase):
	__tablename__ = 'ft_5M_31'


class FT5M32(Base,FT5MBase):
	__tablename__ = 'ft_5M_32'


class FT5M33(Base,FT5MBase):
	__tablename__ = 'ft_5M_33'


class FT5M34(Base,FT5MBase):
	__tablename__ = 'ft_5M_34'
    
if __name__ == '__main__':
    print(locals()['FT5M1'])
    cls = locals()['FT5M1']
    print(cls.__table__)
    print(FT5M1.__table__)

    tables = 35
    for index in range(1,tables,1):
        print('class FT5M{0}(Base,FT5MBase):'.format(index))
        print('\t__tablename__ = \'ft_5M_{0}\'\n\n'.format(index))

# pip3 install flask-sqlalchemy
# class FT(object):
#
#     _mapper = {}
#
#     @staticmethod
#     def model(code, dtype, storeservice):
#         table_index = storeservice.find_tindex(code,dtype)
#
#         class_name = 'FT_%d' % table_index
#
#         ModelClass = FT._mapper.get(class_name,None)
#         if ModelClass is None:
#             ModelClass = type(class_name, (db.Model,),{
#                 '__module__': __name__,
#                 '__name__': class_name,
#                 '__tablename__': ('ft_history_kline_%d' % table_index)
#             })
#
#             FT._mapper[class_name] = ModelClass
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