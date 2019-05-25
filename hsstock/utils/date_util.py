import time
from datetime import datetime, date, timedelta

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

