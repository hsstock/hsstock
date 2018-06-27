import requests
import bs4
import os

# https://finviz.com/help/screener.ashx

class Crawler(object):
    def __init__(self,seperator):
        self.seperator  = seperator
        self.propertiesList = ['No',
                          'Ticker',
                          'Company',
                          'Sector',
                          'Industry',
                          'Country',
                          'Market Cap',
                          'P/E',
                          'Fwd P/E',
                          'PEG',
                          'P/S',
                          'P/B',
                          'P/C',
                          'P/FCF',
                          'Dividend',
                          'Payout Ratio',
                          'EPS',
                          'EPS this Y',
                          'EPS next Y',
                          'EPS past 5Y',
                          'EPS next 5Y',
                          'Sales past 5Y',
                          'EPS Q/Q',
                          'Sales Q/Q',
                          'Outstanding',
                          'Float',
                          'Insider Own',
                          'Insider Trans',
                          'Inst Own',
                          'Inst Trans',
                          'Float Short',
                          'Short Ratio',
                          'ROA',
                          'ROE',
                          'ROI',
                          'CurrR',
                          'Quick R',
                          'LTDebt/Eq',
                          'Debt/Eq',
                          'Gross M',
                          'Oper M',
                          'Profit M',
                          'Perf Week',
                          'Perf Month',
                          'Perf Quart',
                          'Perf Half',
                          'Perf Year',
                          'Perf YTD',
                          'Beta',
                          'ATR',
                          'Volatility W',
                          'Volatility M',
                          'SMA20',
                          'SMA50',
                          'SMA200',
                          '50D High',
                          '50D Low',
                          '52W High',
                          '52W Low',
                          'RSI',
                          'from Open',
                          'Gap',
                          'Recom',
                          'Avg Volume',
                          'Rel Volume',
                          'Price',
                          'Change',
                          'Volume',
                          'Earnings',
                          'Target Price',
                          'IPO Date']

    def get_page(self,url):
        self.itemArray = []
        res = requests.get(url)
        res.raise_for_status()
        if res.status_code == 200 :
            contentSoup = bs4.BeautifulSoup(res.text,'html5lib')
            elems = contentSoup.select('.table-dark-row-cp,.table-light-row-cp')
            for elem in elems:
                items = elem.select('.screener-body-table-nw')
                itemValueStr = ''
                for item in items:
                    internal = item.select('a,span')
                    itemValueStr = itemValueStr + internal[0].getText() + self.seperator

                self.itemArray.append(itemValueStr)


    def writeToFile(self,path):
        if os._exists(path):
            os.remove(path)
        file = open(path,'a')
        for item in self.itemArray:
            file.write(item+'\n')
        file.close()

    def readFile(self,path):
        file = open(path)
        self.itemArray = file.readlines()
        for item in self.itemArray:
            print(item)
            arr = item.split( self.seperator )
            print(str(len(arr)))
        file.close()

    def toJsons(self):
        jsonArray = []
        for item in self.itemArray:
            arr = item.split( self.seperator )
            pos = 0
            json = {}
            for prop in self.propertiesList:
                json[prop] = arr[pos]
                pos = pos + 1
            jsonArray.append(json)
        return jsonArray

    def toJsons(self):
        jsonArray = []
        for item in self.itemArray:
            arr = item.split( self.seperator )
            pos = 0
            json = {}
            for prop in self.propertiesList:
                json[prop] = arr[pos]
                pos = pos + 1
            jsonArray.append(json)
        return jsonArray