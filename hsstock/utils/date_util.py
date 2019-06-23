import time
from datetime import datetime, date, timedelta
import six as six


class DateUtil():
    def __init__(self):
        pass

    @staticmethod
    def getDatetimeToday():
        return date.today()

    @staticmethod
    def getDatetimeToday3():
        today = datetime.today()
        return today.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def getDatetimeToday4():
        today = datetime.today()
        return today.strftime('%Y-%m-%d %H:%M:%S')


    @staticmethod
    def getDatetimeToday2():
        t = date.today()
        dt = datetime.strptime(str(t), '%Y-%m-%d %H:%M:%S')  # date转str再转datetime
        return dt

    @staticmethod
    def getDatetimeYesterdayStr(today):
        yesterday = today + timedelta(days=-1)  # 减去一天
        return yesterday.isoformat()

    @staticmethod
    def getDatetimePastStr(today, ndays):
        past = today + timedelta(days=-ndays)  # 减去ndays天
        return DateUtil.date_toString(past)

    @staticmethod
    def getDatetimeFutureStr(today, ndays):
        past = today + timedelta(days=ndays)  # 加上ndays天
        return DateUtil.date_toString(past)

    @staticmethod
    def getNextHalfYear(start, end,ndays=180):
        future = start
        while future < end:
            if future + timedelta(days=ndays) < end:
                future += timedelta(days=ndays)
                yield DateUtil.date_toString(future)
            else:
                yield DateUtil.date_toString(end)
                break

    @staticmethod
    def getTodayStr():
        return time.strftime('%Y-%m-%d', time.localtime())

    @staticmethod
    def format_date(strDate):
        if DateUtil.isVaildDate(strDate):
            return strDate
        md = str();
        hms = str();
        ymdhms = str();
        if " " in strDate:
            tupDate = strDate.partition(" ")
            md = tupDate[0]
            hms = tupDate[2] + ":00"
        else:
            md = strDate
            hms = "00:00:00"
        ymdhms = str(datetime.now().year) + "-" + md + " " + hms
        return ymdhms

    @staticmethod
    def isVaildDate(date):
        try:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

    @staticmethod
    def format_date_us_history(strDate):
        if DateUtil.isVaildDate(strDate):
            return strDate
        tupDate = strDate.partition("|")
        chineseDate = tupDate[2] + ":00"
        date = str(chineseDate)
        date = date.replace("年", "-")
        date = date.replace("月", "-")
        date = date.replace("日", "")
        date = date.strip()
        return date

    # 把datetime转成字符串
    @staticmethod
    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 把字符串转成datetime
    @staticmethod
    def string_toDatetime(string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    # 把字符串转成datetime
    @staticmethod
    def string_toDatetime2(string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M")

    @staticmethod
    def date_toString(dt):
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def string_toDate(string):
        return datetime.strptime(string, "%Y-%m-%d")

    # 把字符串转成时间戳形式
    @staticmethod
    def string_toTimestamp(strTime):
        return time.mktime(DateUtil.string_toDatetime(strTime).timetuple())

    # 把时间戳转成字符串形式
    @staticmethod
    def timestamp_toString(stamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))

    # 把datetime类型转外时间戳形式
    def datetime_toTimestamp(dateTim):
        return time.mktime(dateTim.timetuple())

    @staticmethod
    def millisecond_to_date(millisecond, format):
        return time.strftime(format, time.localtime(millisecond / 1000))

    @staticmethod
    def date_to_millisecond(date="20100101", format='%Y%m%d'):
        return int(time.mktime(time.strptime(date, format)) * 1000)

    @staticmethod
    def date_str_to_int(date="2010-01-01"):
        return int(date.replace("-", ""))

    @staticmethod
    def week_today():
        d = datetime.now()
        return d.weekday()

    K_DEFAULT_DT_FMT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def week_of_date(date_str, fmt=K_DEFAULT_DT_FMT):
        """
        输入'2016-01-01' 转换为星期几，返回int 0-6分别代表周一到周日
        :param date_str: 式时间日期str对象
        :param fmt: 如date_str不是%Y-%m-%d形式，对应的格式str对象
        :param fix: 是否修复日期不规范的写法，eg. 2016-1-1 fix 2016-01-01
        :return: 返回int 0-6分别代表周一到周日
        """
        return datetime.strptime(date_str, fmt).weekday()

    @staticmethod
    def year_of_date(date_str, fmt=K_DEFAULT_DT_FMT):
        """
        输入'2016-01-01' 转换为星期几，返回int 0-6分别代表周一到周日
        :param date_str: 式时间日期str对象
        :param fmt: 如date_str不是%Y-%m-%d形式，对应的格式str对象
        :param fix: 是否修复日期不规范的写法，eg. 2016-1-1 fix 2016-01-01
        :return: 返回int 0-6分别代表周一到周日
        """
        return datetime.strptime(date_str, fmt).year

    @staticmethod
    def diff(start_date, end_date, check_order=True):
        """
        对两个输入日期计算间隔的天数，如果check_order=False, str日期对象效率最高
        :param start_date: str对象或者int对象，如果check_order=True int对象效率最高
        :param end_date: str对象或者int对象，如果check_order=True int对象效率最高
        :param check_order: 是否纠正参数顺序是否放置正常，默认check
        :return:
        """

        # 首先进来的date都格式化，主要进行的是fix操作，不管是int还是str，这样20160101转换为2016-01-01日期格式
        start_date = fix_date(start_date)
        end_date = fix_date(end_date)

        if check_order and isinstance(start_date, six.string_types):
            # start_date字符串的日期格式转换为int
            start_date = date_str_to_int(start_date)

        if check_order and isinstance(end_date, six.string_types):
            # end_date字符串的日期格式转换为int
            end_date = date_str_to_int(end_date)

        # 是否纠正参数顺序是否放置正常，默认check
        if check_order and start_date > end_date:
            # start_date > end_date说明要换一下
            tmp = end_date
            end_date = start_date
            start_date = tmp

        # fmt_date，但在不需要纠正check_order的情况，这些就都不会执行
        if isinstance(start_date, int):
            # noinspection PyTypeChecker
            start_date = fmt_date(start_date)
        if isinstance(end_date, int):
            # noinspection PyTypeChecker
            end_date = fmt_date(end_date)

        # 在不需要纠正check_order的情况, 直接执行的是这里
        sd = str_to_datetime(start_date)
        ed = str_to_datetime(end_date)

        return (ed - sd).days

"""默认的时间日期格式，项目中金融时间序列等时间相关默认格式"""
K_DEFAULT_DT_FMT2 = "%Y-%m-%d"


def str_to_datetime(date_str, fmt=K_DEFAULT_DT_FMT2, fix=True):
    """
    将字符串日期格式转换成datetime.datetime对象 eg. '2016-01-01' －> datetime.datetime(2016, 1, 1, 0, 0)
    :param date_str: %Y-%m-%d 形式str对象，eg. '2016-01-01'
    :param fmt: 如date_str不是%Y-%m-%d形式，对应的格式str对象
    :param fix: 是否修复日期不规范的写法，eg. 2016-1-1 fix 2016-01-01
    :return: datetime.datetime对象，eg. datetime.datetime(2016, 1, 1, 0, 0)
    """
    if fix and fmt == K_DEFAULT_DT_FMT2:
        # 只针对%Y-%m-%d形式格式标准化日期格式
        date_str = fix_date(date_str)

    return datetime.strptime(date_str, fmt)

def date_str_to_int(date_str, split='-', fix=True):
    """
    eg. 2016-01-01 -> 20160101
    不使用时间api，直接进行字符串解析，执行效率高
    :param date_str: %Y-%m-%d形式时间str对象
    :param split: 年月日的分割符，默认'-'
    :param fix: 是否修复日期不规范的写法，eg. 2016-1-1 fix 2016-01-01
    :return: int类型时间
    """
    if fix and split == '-':
        # 只针对%Y-%m-%d形式格式标准化日期格式
        date_str = fix_date(date_str)
    string_date = date_str.replace(split, '')
    return int(string_date)


def fix_date(date_str):
    """
    修复日期不规范的写法:
                eg. 2016-1-1 fix 2016-01-01
                eg. 2016:01-01 fix 2016-01-01
                eg. 2016,01 01 fix 2016-01-01
                eg. 2016/01-01 fix 2016-01-01
                eg. 2016/01/01 fix 2016-01-01
                eg. 2016/1/1 fix 2016-01-01
                eg. 2016:1:1 fix 2016-01-01
                eg. 2016 1 1 fix 2016-01-01
                eg. 2016 01 01 fix 2016-01-01
                .............................
    不使用时间api，直接进行字符串解析，执行效率高，注意fix_date内部会使用fmt_date
    :param date_str: 检测需要修复的日期str对象或者int对象
    :return: 修复了的日期str对象
    """
    if date_str is not None:
        # 如果是字符串先统一把除了数字之外的都干掉，变成干净的数字串
        if isinstance(date_str, six.string_types):
            # eg, 2016:01-01, 201601-01, 2016,01 01, 2016/01-01 -> 20160101
            date_str = ''.join(list(filter(lambda c: c.isdigit(), date_str)))
        # 再统一确定%Y-%m-%d形式
        date_str = fmt_date(date_str)
        y, m, d = date_str.split('-')
        if len(m) == 1:
            # 月上补0
            m = '0{}'.format(m)
        if len(d) == 1:
            # 日上补0
            d = '0{}'.format(d)
        date_str = "%s-%s-%s" % (y, m, d)
    return date_str

def fmt_date(convert_date):
    """
    将时间格式如20160101转换为2016-01-01日期格式, 注意没有对如 201611
    这样的做fix适配，外部需要明确知道参数的格式，针对特定格式，不使用时间api，
    直接进行字符串解析，执行效率高
    :param convert_date: 时间格式如20160101所示，int类型或者str类型对象
    :return: %Y-%m-%d日期格式str类型对象
    """
    if isinstance(convert_date, float):
        # float先转换int
        convert_date = int(convert_date)
    convert_date = str(convert_date)

    if len(convert_date) > 8 and convert_date.startswith('20'):
        # eg '20160310000000000'
        convert_date = convert_date[:8]

    if '-' not in convert_date:
        if len(convert_date) == 8:
            # 20160101 to 2016-01-01
            convert_date = "%s-%s-%s" % (convert_date[0:4],
                                         convert_date[4:6], convert_date[6:8])
        elif len(convert_date) == 6:
            # 201611 to 2016-01-01
            convert_date = "%s-0%s-0%s" % (convert_date[0:4],
                                           convert_date[4:5], convert_date[5:6])
        else:
            raise ValueError('fmt_date: convert_date fmt error {}'.format(convert_date))
    return convert_date


if __name__ == "__main__":
    print( DateUtil.getTodayStr() )
    print(DateUtil.getDatetimeToday())
    print(DateUtil.getDatetimeYesterdayStr( DateUtil.getDatetimeToday()))
    print(DateUtil.format_date('07-02 06:00'))
    print(DateUtil.datetime_toString(datetime.now()))
    print(DateUtil.string_toDatetime(DateUtil.format_date('07-02 06:00')))
    print(DateUtil.string_toTimestamp(DateUtil.format_date('07-02 06:00')))
    print(DateUtil.timestamp_toString(DateUtil.string_toTimestamp(DateUtil.format_date('07-02 06:00'))))
    print(DateUtil.date_str_to_int('2007-07-07'))
    print(DateUtil.date_to_millisecond(str(DateUtil.date_str_to_int('2007-07-07'))))

    gen = DateUtil.getNextHalfYear( DateUtil.string_toDate('2016-01-01'),DateUtil.string_toDate('2018-01-01') )
    while True:
        try:
            end = next(gen)
            print( end )
            print( DateUtil.getDatetimeFutureStr(DateUtil.string_toDate(end),1) )

        except StopIteration as e:
            print(e)
            break

