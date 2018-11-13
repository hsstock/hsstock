
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

class FT5M35(Base,FT5MBase):
	__tablename__ = 'ft_5M_35'


class FT5M36(Base,FT5MBase):
	__tablename__ = 'ft_5M_36'


class FT5M37(Base,FT5MBase):
	__tablename__ = 'ft_5M_37'


class FT5M38(Base,FT5MBase):
	__tablename__ = 'ft_5M_38'


class FT5M39(Base,FT5MBase):
	__tablename__ = 'ft_5M_39'


class FT5M40(Base,FT5MBase):
	__tablename__ = 'ft_5M_40'


class FT5M41(Base,FT5MBase):
	__tablename__ = 'ft_5M_41'


class FT5M42(Base,FT5MBase):
	__tablename__ = 'ft_5M_42'


class FT5M43(Base,FT5MBase):
	__tablename__ = 'ft_5M_43'


class FT5M44(Base,FT5MBase):
	__tablename__ = 'ft_5M_44'


class FT5M45(Base,FT5MBase):
	__tablename__ = 'ft_5M_45'


class FT5M46(Base,FT5MBase):
	__tablename__ = 'ft_5M_46'


class FT5M47(Base,FT5MBase):
	__tablename__ = 'ft_5M_47'


class FT5M48(Base,FT5MBase):
	__tablename__ = 'ft_5M_48'


class FT5M49(Base,FT5MBase):
	__tablename__ = 'ft_5M_49'


class FT5M50(Base,FT5MBase):
	__tablename__ = 'ft_5M_50'


class FT5M51(Base,FT5MBase):
	__tablename__ = 'ft_5M_51'


class FT5M52(Base,FT5MBase):
	__tablename__ = 'ft_5M_52'


class FT5M53(Base,FT5MBase):
	__tablename__ = 'ft_5M_53'


class FT5M54(Base,FT5MBase):
	__tablename__ = 'ft_5M_54'


class FT5M55(Base,FT5MBase):
	__tablename__ = 'ft_5M_55'


class FT5M56(Base,FT5MBase):
	__tablename__ = 'ft_5M_56'


class FT5M57(Base,FT5MBase):
	__tablename__ = 'ft_5M_57'


class FT5M58(Base,FT5MBase):
	__tablename__ = 'ft_5M_58'


class FT5M59(Base,FT5MBase):
	__tablename__ = 'ft_5M_59'


class FT5M60(Base,FT5MBase):
	__tablename__ = 'ft_5M_60'


class FT5M61(Base,FT5MBase):
	__tablename__ = 'ft_5M_61'


class FT5M62(Base,FT5MBase):
	__tablename__ = 'ft_5M_62'


class FT5M63(Base,FT5MBase):
	__tablename__ = 'ft_5M_63'


class FT5M64(Base,FT5MBase):
	__tablename__ = 'ft_5M_64'


class FT5M65(Base,FT5MBase):
	__tablename__ = 'ft_5M_65'


class FT5M66(Base,FT5MBase):
	__tablename__ = 'ft_5M_66'


class FT5M67(Base,FT5MBase):
	__tablename__ = 'ft_5M_67'


class FT5M68(Base,FT5MBase):
	__tablename__ = 'ft_5M_68'


class FT5M69(Base,FT5MBase):
	__tablename__ = 'ft_5M_69'


class FT5M70(Base,FT5MBase):
	__tablename__ = 'ft_5M_70'


class FT5M71(Base,FT5MBase):
	__tablename__ = 'ft_5M_71'


class FT5M72(Base,FT5MBase):
	__tablename__ = 'ft_5M_72'


class FT5M73(Base,FT5MBase):
	__tablename__ = 'ft_5M_73'


class FT5M74(Base,FT5MBase):
	__tablename__ = 'ft_5M_74'


class FT5M75(Base,FT5MBase):
	__tablename__ = 'ft_5M_75'


class FT5M76(Base,FT5MBase):
	__tablename__ = 'ft_5M_76'


class FT5M77(Base,FT5MBase):
	__tablename__ = 'ft_5M_77'


class FT5M78(Base,FT5MBase):
	__tablename__ = 'ft_5M_78'


class FT5M79(Base,FT5MBase):
	__tablename__ = 'ft_5M_79'


class FT5M80(Base,FT5MBase):
	__tablename__ = 'ft_5M_80'

def get5MClassByIndex(tindex):
    return globals()['FT5M{}'.format(tindex)]

if __name__ == '__main__':
    print(locals()['FT5M1'])
    cls = locals()['FT5M1']
    print(cls.__table__)
    print(FT5M1.__table__)

    tables = 81
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