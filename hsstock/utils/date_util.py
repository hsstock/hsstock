import time
from datetime import datetime, date, timedelta

class DateUtil():
    def __init__(self):
        pass

    @staticmethod
    def getDatetimeToday():
        return date.today()

    @staticmethod
    def getDatetimeToday2(self):
        t = date.today()  # date类型
        dt = datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime
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

    # 把datetime转成字符串
    @staticmethod
    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 把字符串转成datetime
    @staticmethod
    def string_toDatetime(string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

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

if __name__ == "__main__":
    print( DateUtil.getTodayStr() )
    print(DateUtil.getDatetimeToday())
    print(DateUtil.getDatetimeYesterdayStr( DateUtil.getDatetimeToday()))
    print(DateUtil.format_date('07-02 06:00'))
    print(DateUtil.datetime_toString(datetime.now()))
    print(DateUtil.string_toDatetime(DateUtil.format_date('07-02 06:00')))
    print(DateUtil.string_toTimestamp(DateUtil.format_date('07-02 06:00')))
    print(DateUtil.timestamp_toString(DateUtil.string_toTimestamp(DateUtil.format_date('07-02 06:00'))))