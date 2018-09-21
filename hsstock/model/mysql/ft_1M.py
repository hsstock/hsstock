
from sqlalchemy import Column, Integer, String, BigInteger,Date,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FT1MBase(object):

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
        return "<ft_1M(code={},time_key={},open={},close={})>".format(self.code, self.time_key,
                                                                                      self.open, self.close)

class FT1M1(Base,FT1MBase):
	__tablename__ = 'ft_1M_1'


class FT1M2(Base,FT1MBase):
	__tablename__ = 'ft_1M_2'


class FT1M3(Base,FT1MBase):
	__tablename__ = 'ft_1M_3'


class FT1M4(Base,FT1MBase):
	__tablename__ = 'ft_1M_4'


class FT1M5(Base,FT1MBase):
	__tablename__ = 'ft_1M_5'


class FT1M6(Base,FT1MBase):
	__tablename__ = 'ft_1M_6'


class FT1M7(Base,FT1MBase):
	__tablename__ = 'ft_1M_7'


class FT1M8(Base,FT1MBase):
	__tablename__ = 'ft_1M_8'


class FT1M9(Base,FT1MBase):
	__tablename__ = 'ft_1M_9'


class FT1M10(Base,FT1MBase):
	__tablename__ = 'ft_1M_10'


class FT1M11(Base,FT1MBase):
	__tablename__ = 'ft_1M_11'


class FT1M12(Base,FT1MBase):
	__tablename__ = 'ft_1M_12'


class FT1M13(Base,FT1MBase):
	__tablename__ = 'ft_1M_13'


class FT1M14(Base,FT1MBase):
	__tablename__ = 'ft_1M_14'


class FT1M15(Base,FT1MBase):
	__tablename__ = 'ft_1M_15'


class FT1M16(Base,FT1MBase):
	__tablename__ = 'ft_1M_16'


class FT1M17(Base,FT1MBase):
	__tablename__ = 'ft_1M_17'


class FT1M18(Base,FT1MBase):
	__tablename__ = 'ft_1M_18'


class FT1M19(Base,FT1MBase):
	__tablename__ = 'ft_1M_19'


class FT1M20(Base,FT1MBase):
	__tablename__ = 'ft_1M_20'


class FT1M21(Base,FT1MBase):
	__tablename__ = 'ft_1M_21'


class FT1M22(Base,FT1MBase):
	__tablename__ = 'ft_1M_22'


class FT1M23(Base,FT1MBase):
	__tablename__ = 'ft_1M_23'


class FT1M24(Base,FT1MBase):
	__tablename__ = 'ft_1M_24'


class FT1M25(Base,FT1MBase):
	__tablename__ = 'ft_1M_25'


class FT1M26(Base,FT1MBase):
	__tablename__ = 'ft_1M_26'


class FT1M27(Base,FT1MBase):
	__tablename__ = 'ft_1M_27'


class FT1M28(Base,FT1MBase):
	__tablename__ = 'ft_1M_28'


class FT1M29(Base,FT1MBase):
	__tablename__ = 'ft_1M_29'


class FT1M30(Base,FT1MBase):
	__tablename__ = 'ft_1M_30'


class FT1M31(Base,FT1MBase):
	__tablename__ = 'ft_1M_31'


class FT1M32(Base,FT1MBase):
	__tablename__ = 'ft_1M_32'


class FT1M33(Base,FT1MBase):
	__tablename__ = 'ft_1M_33'


class FT1M34(Base,FT1MBase):
	__tablename__ = 'ft_1M_34'


class FT1M35(Base,FT1MBase):
	__tablename__ = 'ft_1M_35'


class FT1M36(Base,FT1MBase):
	__tablename__ = 'ft_1M_36'


class FT1M37(Base,FT1MBase):
	__tablename__ = 'ft_1M_37'


class FT1M38(Base,FT1MBase):
	__tablename__ = 'ft_1M_38'


class FT1M39(Base,FT1MBase):
	__tablename__ = 'ft_1M_39'


class FT1M40(Base,FT1MBase):
	__tablename__ = 'ft_1M_40'


class FT1M41(Base,FT1MBase):
	__tablename__ = 'ft_1M_41'


class FT1M42(Base,FT1MBase):
	__tablename__ = 'ft_1M_42'


class FT1M43(Base,FT1MBase):
	__tablename__ = 'ft_1M_43'


class FT1M44(Base,FT1MBase):
	__tablename__ = 'ft_1M_44'


class FT1M45(Base,FT1MBase):
	__tablename__ = 'ft_1M_45'


class FT1M46(Base,FT1MBase):
	__tablename__ = 'ft_1M_46'


class FT1M47(Base,FT1MBase):
	__tablename__ = 'ft_1M_47'


class FT1M48(Base,FT1MBase):
	__tablename__ = 'ft_1M_48'


class FT1M49(Base,FT1MBase):
	__tablename__ = 'ft_1M_49'


class FT1M50(Base,FT1MBase):
	__tablename__ = 'ft_1M_50'


class FT1M51(Base,FT1MBase):
	__tablename__ = 'ft_1M_51'


class FT1M52(Base,FT1MBase):
	__tablename__ = 'ft_1M_52'


class FT1M53(Base,FT1MBase):
	__tablename__ = 'ft_1M_53'


class FT1M54(Base,FT1MBase):
	__tablename__ = 'ft_1M_54'


class FT1M55(Base,FT1MBase):
	__tablename__ = 'ft_1M_55'


class FT1M56(Base,FT1MBase):
	__tablename__ = 'ft_1M_56'


class FT1M57(Base,FT1MBase):
	__tablename__ = 'ft_1M_57'


class FT1M58(Base,FT1MBase):
	__tablename__ = 'ft_1M_58'


class FT1M59(Base,FT1MBase):
	__tablename__ = 'ft_1M_59'


class FT1M60(Base,FT1MBase):
	__tablename__ = 'ft_1M_60'


class FT1M61(Base,FT1MBase):
	__tablename__ = 'ft_1M_61'


class FT1M62(Base,FT1MBase):
	__tablename__ = 'ft_1M_62'


class FT1M63(Base,FT1MBase):
	__tablename__ = 'ft_1M_63'


class FT1M64(Base,FT1MBase):
	__tablename__ = 'ft_1M_64'


class FT1M65(Base,FT1MBase):
	__tablename__ = 'ft_1M_65'


class FT1M66(Base,FT1MBase):
	__tablename__ = 'ft_1M_66'


class FT1M67(Base,FT1MBase):
	__tablename__ = 'ft_1M_67'


class FT1M68(Base,FT1MBase):
	__tablename__ = 'ft_1M_68'


class FT1M69(Base,FT1MBase):
	__tablename__ = 'ft_1M_69'


class FT1M70(Base,FT1MBase):
	__tablename__ = 'ft_1M_70'


class FT1M71(Base,FT1MBase):
	__tablename__ = 'ft_1M_71'


class FT1M72(Base,FT1MBase):
	__tablename__ = 'ft_1M_72'


class FT1M73(Base,FT1MBase):
	__tablename__ = 'ft_1M_73'


class FT1M74(Base,FT1MBase):
	__tablename__ = 'ft_1M_74'


class FT1M75(Base,FT1MBase):
	__tablename__ = 'ft_1M_75'


class FT1M76(Base,FT1MBase):
	__tablename__ = 'ft_1M_76'


class FT1M77(Base,FT1MBase):
	__tablename__ = 'ft_1M_77'


class FT1M78(Base,FT1MBase):
	__tablename__ = 'ft_1M_78'


class FT1M79(Base,FT1MBase):
	__tablename__ = 'ft_1M_79'


class FT1M80(Base,FT1MBase):
	__tablename__ = 'ft_1M_80'


class FT1M81(Base,FT1MBase):
	__tablename__ = 'ft_1M_81'


class FT1M82(Base,FT1MBase):
	__tablename__ = 'ft_1M_82'


class FT1M83(Base,FT1MBase):
	__tablename__ = 'ft_1M_83'


class FT1M84(Base,FT1MBase):
	__tablename__ = 'ft_1M_84'


class FT1M85(Base,FT1MBase):
	__tablename__ = 'ft_1M_85'


class FT1M86(Base,FT1MBase):
	__tablename__ = 'ft_1M_86'


class FT1M87(Base,FT1MBase):
	__tablename__ = 'ft_1M_87'


class FT1M88(Base,FT1MBase):
	__tablename__ = 'ft_1M_88'


class FT1M89(Base,FT1MBase):
	__tablename__ = 'ft_1M_89'


class FT1M90(Base,FT1MBase):
	__tablename__ = 'ft_1M_90'


class FT1M91(Base,FT1MBase):
	__tablename__ = 'ft_1M_91'


class FT1M92(Base,FT1MBase):
	__tablename__ = 'ft_1M_92'


class FT1M93(Base,FT1MBase):
	__tablename__ = 'ft_1M_93'


class FT1M94(Base,FT1MBase):
	__tablename__ = 'ft_1M_94'


class FT1M95(Base,FT1MBase):
	__tablename__ = 'ft_1M_95'


class FT1M96(Base,FT1MBase):
	__tablename__ = 'ft_1M_96'


class FT1M97(Base,FT1MBase):
	__tablename__ = 'ft_1M_97'


class FT1M98(Base,FT1MBase):
	__tablename__ = 'ft_1M_98'


class FT1M99(Base,FT1MBase):
	__tablename__ = 'ft_1M_99'


class FT1M100(Base,FT1MBase):
	__tablename__ = 'ft_1M_100'


class FT1M101(Base,FT1MBase):
	__tablename__ = 'ft_1M_101'


class FT1M102(Base,FT1MBase):
	__tablename__ = 'ft_1M_102'


class FT1M103(Base,FT1MBase):
	__tablename__ = 'ft_1M_103'


class FT1M104(Base,FT1MBase):
	__tablename__ = 'ft_1M_104'


class FT1M105(Base,FT1MBase):
	__tablename__ = 'ft_1M_105'


class FT1M106(Base,FT1MBase):
	__tablename__ = 'ft_1M_106'


class FT1M107(Base,FT1MBase):
	__tablename__ = 'ft_1M_107'


class FT1M108(Base,FT1MBase):
	__tablename__ = 'ft_1M_108'


class FT1M109(Base,FT1MBase):
	__tablename__ = 'ft_1M_109'


class FT1M110(Base,FT1MBase):
	__tablename__ = 'ft_1M_110'


class FT1M111(Base,FT1MBase):
	__tablename__ = 'ft_1M_111'


class FT1M112(Base,FT1MBase):
	__tablename__ = 'ft_1M_112'


class FT1M113(Base,FT1MBase):
	__tablename__ = 'ft_1M_113'


class FT1M114(Base,FT1MBase):
	__tablename__ = 'ft_1M_114'


class FT1M115(Base,FT1MBase):
	__tablename__ = 'ft_1M_115'


class FT1M116(Base,FT1MBase):
	__tablename__ = 'ft_1M_116'


class FT1M117(Base,FT1MBase):
	__tablename__ = 'ft_1M_117'


class FT1M118(Base,FT1MBase):
	__tablename__ = 'ft_1M_118'


class FT1M119(Base,FT1MBase):
	__tablename__ = 'ft_1M_119'


class FT1M120(Base,FT1MBase):
	__tablename__ = 'ft_1M_120'


class FT1M121(Base,FT1MBase):
	__tablename__ = 'ft_1M_121'


class FT1M122(Base,FT1MBase):
	__tablename__ = 'ft_1M_122'


class FT1M123(Base,FT1MBase):
	__tablename__ = 'ft_1M_123'


class FT1M124(Base,FT1MBase):
	__tablename__ = 'ft_1M_124'


class FT1M125(Base,FT1MBase):
	__tablename__ = 'ft_1M_125'


class FT1M126(Base,FT1MBase):
	__tablename__ = 'ft_1M_126'


class FT1M127(Base,FT1MBase):
	__tablename__ = 'ft_1M_127'


class FT1M128(Base,FT1MBase):
	__tablename__ = 'ft_1M_128'


class FT1M129(Base,FT1MBase):
	__tablename__ = 'ft_1M_129'


class FT1M130(Base,FT1MBase):
	__tablename__ = 'ft_1M_130'


class FT1M131(Base,FT1MBase):
	__tablename__ = 'ft_1M_131'


class FT1M132(Base,FT1MBase):
	__tablename__ = 'ft_1M_132'


class FT1M133(Base,FT1MBase):
	__tablename__ = 'ft_1M_133'


class FT1M134(Base,FT1MBase):
	__tablename__ = 'ft_1M_134'


class FT1M135(Base,FT1MBase):
	__tablename__ = 'ft_1M_135'


class FT1M136(Base,FT1MBase):
	__tablename__ = 'ft_1M_136'


class FT1M137(Base,FT1MBase):
	__tablename__ = 'ft_1M_137'


class FT1M138(Base,FT1MBase):
	__tablename__ = 'ft_1M_138'


class FT1M139(Base,FT1MBase):
	__tablename__ = 'ft_1M_139'


class FT1M140(Base,FT1MBase):
	__tablename__ = 'ft_1M_140'


class FT1M141(Base,FT1MBase):
	__tablename__ = 'ft_1M_141'


class FT1M142(Base,FT1MBase):
	__tablename__ = 'ft_1M_142'


class FT1M143(Base,FT1MBase):
	__tablename__ = 'ft_1M_143'


class FT1M144(Base,FT1MBase):
	__tablename__ = 'ft_1M_144'


class FT1M145(Base,FT1MBase):
	__tablename__ = 'ft_1M_145'


class FT1M146(Base,FT1MBase):
	__tablename__ = 'ft_1M_146'


class FT1M147(Base,FT1MBase):
	__tablename__ = 'ft_1M_147'


class FT1M148(Base,FT1MBase):
	__tablename__ = 'ft_1M_148'


class FT1M149(Base,FT1MBase):
	__tablename__ = 'ft_1M_149'


class FT1M150(Base,FT1MBase):
	__tablename__ = 'ft_1M_150'


class FT1M151(Base,FT1MBase):
	__tablename__ = 'ft_1M_151'


class FT1M152(Base,FT1MBase):
	__tablename__ = 'ft_1M_152'


class FT1M153(Base,FT1MBase):
	__tablename__ = 'ft_1M_153'


class FT1M154(Base,FT1MBase):
	__tablename__ = 'ft_1M_154'


class FT1M155(Base,FT1MBase):
	__tablename__ = 'ft_1M_155'


class FT1M156(Base,FT1MBase):
	__tablename__ = 'ft_1M_156'


class FT1M157(Base,FT1MBase):
	__tablename__ = 'ft_1M_157'


class FT1M158(Base,FT1MBase):
	__tablename__ = 'ft_1M_158'


class FT1M159(Base,FT1MBase):
	__tablename__ = 'ft_1M_159'


class FT1M160(Base,FT1MBase):
	__tablename__ = 'ft_1M_160'


class FT1M161(Base,FT1MBase):
	__tablename__ = 'ft_1M_161'


class FT1M162(Base,FT1MBase):
	__tablename__ = 'ft_1M_162'


class FT1M163(Base,FT1MBase):
	__tablename__ = 'ft_1M_163'


class FT1M164(Base,FT1MBase):
	__tablename__ = 'ft_1M_164'


class FT1M165(Base,FT1MBase):
	__tablename__ = 'ft_1M_165'


class FT1M166(Base,FT1MBase):
	__tablename__ = 'ft_1M_166'


class FT1M167(Base,FT1MBase):
	__tablename__ = 'ft_1M_167'


class FT1M168(Base,FT1MBase):
	__tablename__ = 'ft_1M_168'


class FT1M169(Base,FT1MBase):
	__tablename__ = 'ft_1M_169'


class FT1M170(Base,FT1MBase):
	__tablename__ = 'ft_1M_170'

    
if __name__ == '__main__':
    print(locals()['FT1M1'])
    cls = locals()['FT1M1']
    print(cls.__table__)
    print(FT1M1.__table__)

    tables = 171
    for index in range(1,tables,1):
        print('class FT1M{0}(Base,FT1MBase):'.format(index))
        print('\t__tablename__ = \'ft_1M_{0}\'\n\n'.format(index))

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