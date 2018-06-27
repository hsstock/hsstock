import time
from datetime import datetime, date, timedelta

class DateUtil():
    def __init__(self):
        pass

    @staticmethod
    def getDatetimeToday():
        return date.today()

    def getDatetimeToday2(self):
        t = date.today()  # date类型
        dt = datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime
        return dt

    @staticmethod
    def getDatetimeYesterdayStr(today):
        yesterday = today + timedelta(days=-1)  # 减去一天
        return yesterday.isoformat()

    @staticmethod
    def getTodayStr():
        return time.strftime('%Y-%m-%d', time.localtime())



if __name__ == "__main__":
    print( DateUtil.getTodayStr() )
    print(DateUtil.getDatetimeToday())
    print(DateUtil.getDatetimeYesterdayStr( DateUtil.getDatetimeToday()))