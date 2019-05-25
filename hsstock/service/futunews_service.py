# -*- coding: UTF-8 -*-
import requests
import bs4
import time
import random
import json
import copy

import hsstock.utils.logger as logger
from hsstock.utils.date_util import DateUtil
from hsstock.utils.decorator import retry


class FutunnService(object):
    def __init__(self, mongodbutil,mongodbutil_live,mongodbutil_calendar,mongodbutil_cash,
                 mongodbutil_balancesheet,mongodbutil_income,mongodbutil_companyinfo,mongodbutil_dividend):
        self.itemArray = []
        self.mongodbutil = mongodbutil
        self.mongodbutil_live = mongodbutil_live
        self.mongodbutil_calendar = mongodbutil_calendar
        self.mongodbutil_cash = mongodbutil_cash
        self.mongodbutil_balancesheet = mongodbutil_balancesheet
        self.mongodbutil_income = mongodbutil_income
        self.mongodbutil_companyinfo = mongodbutil_companyinfo
        self.mongodbutil_dividend = mongodbutil_dividend
        self.url = 'https://news.futunn.com/main'

    def get_individual_news(self,market, code):
        ret_code = -1
        ret_data = ''
        self.itemArray = []

        url = "https://www.futunn.com/quote/stock-news?m={0}&code={1}".format(market.lower(),code.upper())

        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Accept': 'application/json,text/javascript,*.*;q=0.01',
                'Origin': 'https://www.futunn.com',
                'Referer': 'https://www.futunn.com/quote/stock-info?m={0}&code={1}&type=finance_analyse'.format(market.lower(),code.upper)
            }
            res = requests.get(url, headers=header)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            html = res.text  # .encode(res.encoding)
            res.raise_for_status()
            if res.status_code == 200:
                contentSoup = bs4.BeautifulSoup(html, 'lxml')

                elems = contentSoup.select('.ulList02 >  ul > li')

                for elem in elems:
                    json = {}
                    json['code'] = code
                    json['market']  = market
                    json['title'] = elem.select('.txt01')[0].getText()
                    json['href'] = elem.select('.txt01 > a')[0]['href']
                    json['date'] = DateUtil.string_toDatetime2(elem.select('.bar01')[0].getText().strip()[3:])
                    json['year'] = json['date'].year
                    json['sourcefrom'] = 'futunn'

                    ret, content = self.get_content(json['href'],'utf-8')

                    # if ret != -1:
                    #     time.sleep(4 * random.random())

                    if ret == 0:
                        json['content'] = content
                        self.itemArray.append(json)


                ret_code = 0
                ret_data = ''
        except Exception as err:
            # time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code, ret_data


    def get_individual_cashflow(self,market, code):
        ret_code = -1
        ret_data = ''
        self.itemArray = []

        url = "https://finance.futunn.com/api/finance/cash-flow?code={0}&label={1}&quarter=0&page=0".format(code.upper(),market.lower())

        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Accept': 'application/json,text/javascript,*.*;q=0.01',
                'Origin': 'https://www.futunn.com',
                'Referer': 'https://www.futunn.com/quote/stock-info?m={0}&code={1}&type=finance_analyse'.format(market.lower(),code.upper)
            }
            res = requests.get(url, headers=header)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            res.raise_for_status()

            if res.status_code == 200:
                data = res.text
                js = json.loads(data)

                obj = js['data']['list']

                for v in obj['values']:
                    o = {}
                    idx = 0

                    for item in v:
                        o[obj['keys'][idx]] = item['value']
                        idx += 1

                    o['title'] = obj['title']
                    o['enterpriseType'] = obj['enterpriseType']
                    o['market'] = market
                    o['code'] = code

                    self.itemArray.append(o)

                ret_code = 0
                ret_data = ''
        except Exception as err:
            # time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code, ret_data


    def get_individual_balancesheet(self,market, code):
        ret_code = -1
        ret_data = ''
        self.itemArray = []

        url = "https://finance.futunn.com/api/finance/balance-sheet?code={0}&label={1}&quarter=0&page=0".format(code.upper(),market.lower())

        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Accept': 'application/json,text/javascript,*.*;q=0.01',
                'Origin': 'https://www.futunn.com',
                'Referer': 'https://www.futunn.com/quote/stock-info?m={0}&code={1}&type=finance_analyse'.format(market.lower(),code.upper)
            }
            res = requests.get(url, headers=header)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            res.raise_for_status()

            if res.status_code == 200:
                data = res.text
                js = json.loads(data)

                obj = js['data']['list']

                for v in obj['values']:
                    o = {}
                    idx = 0

                    for item in v:
                        o[obj['keys'][idx]] = item['value']
                        idx += 1

                    o['title'] = obj['title']
                    o['enterpriseType'] = obj['enterpriseType']
                    o['market'] = market
                    o['code'] = code

                    self.itemArray.append(o)

                ret_code = 0
                ret_data = ''
        except Exception as err:
            # time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code, ret_data

    def get_individual_income(self, market, code):
        ret_code = -1
        ret_data = ''
        self.itemArray = []

        url = "https://finance.futunn.com/api/finance/balance-sheet?code={0}&label={1}&quarter=0&page=0".format(code.upper(), market.lower())

        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Accept': 'application/json,text/javascript,*.*;q=0.01',
                'Origin': 'https://www.futunn.com',
                'Referer': 'https://www.futunn.com/quote/stock-info?m={0}&code={1}&type=finance_analyse'.format(
                    market.lower(), code.upper)
            }
            res = requests.get(url, headers=header)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            res.raise_for_status()

            if res.status_code == 200:
                data = res.text
                js = json.loads(data)

                obj = js['data']['list']

                for v in obj['values']:
                    o = {}
                    idx = 0

                    for item in v:
                        o[obj['keys'][idx]] = item['value']
                        idx += 1

                    o['title'] = obj['title']
                    o['enterpriseType'] = obj['enterpriseType']
                    o['market'] = market
                    o['code'] = code

                    self.itemArray.append(o)

                ret_code = 0
                ret_data = ''
        except Exception as err:
            # time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code, ret_data

    def get_individual_companyinfo(self, market, code):
        ret_code = -1
        ret_data = ''
        self.itemArray = []

        url = "https://finance.futunn.com/api/finance/company-info?code={0}&label={1}".format(code.upper(), market.lower())

        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Accept': 'application/json,text/javascript,*.*;q=0.01',
                'Origin': 'https://www.futunn.com',
                'Referer': 'https://www.futunn.com/quote/stock-info?m={0}&code={1}&type=finance_analyse'.format(
                    market.lower(), code.upper)
            }
            res = requests.get(url, headers=header)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            res.raise_for_status()

            if res.status_code == 200:
                data = res.text
                js = json.loads(data)


                obj = js['data']
                if len(obj) != 0:
                    obj['market'] = market
                    obj['code'] = code

                    self.itemArray.append(obj)

                ret_code = 0
                ret_data = ''
        except Exception as err:
            # time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code, ret_data


    def get_individual_dividend(self, market, code):
        ret_code = -1
        ret_data = ''
        self.itemArray = []

        url = "https://finance.futunn.com/api/finance/dividend?code={0}&label={1}".format(code.upper(), market.lower())

        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Accept': 'application/json,text/javascript,*.*;q=0.01',
                'Origin': 'https://www.futunn.com',
                'Referer': 'https://www.futunn.com/quote/stock-info?m={0}&code={1}&type=finance_analyse'.format(
                    market.lower(), code.upper)
            }
            res = requests.get(url, headers=header)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            res.raise_for_status()

            if res.status_code == 200:
                data = res.text
                js = json.loads(data)

                obj = js['data']
                if len(obj) != 0:
                    obj['market'] = market
                    obj['code'] = code

                    self.itemArray.append(obj)

                ret_code = 0
                ret_data = ''
        except Exception as err:
            # time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code, ret_data



    @retry(wait=30)
    def get_live_info(self):

        ret_code = -1
        ret_data = ''
        self.itemArray = []

        lasttime = DateUtil.string_toDatetime2('2019-05-01 09:00')

        try:
            res = requests.get(self.url)
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'gbk'
            html = res.text  # .encode(res.encoding)
            res.raise_for_status()
            if res.status_code == 200 :
                    contentSoup = bs4.BeautifulSoup(html, 'lxml')
                    elems = contentSoup.find_all('a', class_='news-link')

                    for elem in elems:
                        json = {}
                        json['code'] = ' '


                        newstime = elem.select('span')
                        time = newstime[len(newstime) - 1].getText()
                        json['date'] = DateUtil.string_toDatetime2(time)
                        s = json['date']

                        if s < lasttime :
                            continue
                        else:
                            lasttime = s

                        h3 = elem.select('h3')
                        json['title'] = h3[len(h3) - 1].getText()

                        logger.info("date:{},title:{}".format(s, json['title']))
                        json['href'] = elem.attrs['href']
                        json['year'] = json['date'].year
                        json['sourcefrom'] = 'futunn'
                        ret,content = self.get_content(json['href'],'utf-8')
                        # if ret != -1 :
                        #     time.sleep(4 * random.random())

                        if ret == 0 :
                            json['content'] = content
                            self.itemArray.append(json)
                        ret_code = 0
                        ret_data = ''
        except Exception as err:
            #time.sleep(4 * random.random())
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret_code,ret_data


    #@retry()
    def get_content(self, url, enco):
        content = ''
        ret = -1

        urlExist = self.mongodbutil.urlIsExist(url)
        if urlExist:
            logger.info('This url:{} has existed'.format(url))
            return -2, content

        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        try:
            res = requests.get(url, headers=header, timeout=60)
            res.encoding = enco
            res.raise_for_status()
            if res.status_code == 200:
                soup = bs4.BeautifulSoup(res.text, 'lxml')
                elems = soup.select('.inner')
                if len(elems) > 0:
                    content = elems[0].getText()
                    ret = 0

        except Exception as err:
            #time.sleep(4 * random.random())
            logger.warning(err)
        except requests.exceptions.ConnectTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.ReadTimeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except requests.exceptions.Timeout as err:
            logger.warning(err)
            ret_code = -1
            ret_data = err
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return ret, content

    def get_futunn_news(self):

        for i in range(94471,94480,1):
            url = 'https://news.futunn.com/market/{0}?src=3'.format(i)

            urlExist = self.mongodbutil.urlIsExist(url)
            if urlExist:
                logger.info('This url:{} has existed'.format(url))
                continue

            json = {}
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            try:
                res = requests.get(url, headers=header, timeout=60)
                res.raise_for_status()
                if res.status_code == 200:
                    soup = bs4.BeautifulSoup(res.text, 'lxml')
                    elems = soup.select('.inner')
                    json['content']  = elems[0].getText()
                    elems = soup.select('.news-title > h1')
                    json['title'] = elems[0].getText()
                    elems = soup.select('.news-title > .timeBar')

                    pos = elems[0].getText().strip().find('2')
                    json['date'] = elems[0].getText().strip()[pos:pos+16]
                    json['href'] = url
                    json['code'] = ' '
                    json['year'] = DateUtil.string_toDatetime2(json['date']).year
                    json['sourcefrom'] = 'futunn'
                    self.itemArray.append(json)

                    if len(self.get_item_array()) > 50:
                        self.mongodbutil.insertItems(self.get_item_array())
                        logger.info("store items to mongodb ...")
                        self.clear_item_array()


            except Exception as err:
                #time.sleep(4 * random.random())
                logger.warning(err)
            except requests.exceptions.ConnectTimeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except requests.exceptions.ReadTimeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except requests.exceptions.Timeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except:
                logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(random.random())
                ret_code = -1
                ret_data = ''
            finally:
                res.close()

        return 1, 'ok'

    def get_futunn_live(self):

        lasttime = DateUtil.string_toDatetime(self.mongodbutil_live.getLastLivetime())

        for i in range(0,-1,-1):
            p = int(1000*time.mktime(time.localtime())) + i
            url = 'https://news.futunn.com/main/live-list?page={0}page_size=50&_=1556778263374'.format(i,p)

            logger.info("address current url {0}...".format(url))

            arr = []
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            try:
                res = requests.get(url, headers=header, timeout=60)
                res.raise_for_status()
                if res.status_code == 200:
                    data = res.text
                    js = json.loads(data)

                    list = js['data']['list']
                    for elem in list:
                        itemTime = DateUtil.string_toDatetime(elem['time'])

                        if itemTime > lasttime:
                            arr.append( elem )
                            logger.info(elem)
                        else:
                            continue

                    if len(arr) > 0 :
                        self.mongodbutil_live.insertItems(arr)
                        logger.info("store items to mongodb ...")
                    else:
                        logger.info("still have no new live message")

            except Exception as err:
                #time.sleep(4 * random.random())
                logger.warning(err)
            except requests.exceptions.ConnectTimeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except requests.exceptions.ReadTimeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except requests.exceptions.Timeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except:
                logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(random.random())
                ret_code = -1
                ret_data = ''
            finally:
                res.close()

        return 1, 'ok'

    def get_calendars(self):

        urls = [
            'https://news.futunn.com/new-calendar/events-list?begin_time={0}&end_time=2037-12-31&event_type=%5B%22%E6%B8%AF%E8%82%A1%E6%96%B0%E8%82%A1%22%2C%22%E7%BE%8E%E8%82%A1%E6%96%B0%E8%82%A1%22%2C%22A%E8%82%A1%E6%96%B0%E8%82%A1%22%5D&stock_type=&_={1}',
            'https://news.futunn.com/new-calendar/events-list?begin_time={0}&end_time=2037-12-31&event_type=["港股财报"%2C"美股财报"%2C"A股财报"]&stock_type=&_={1}',
            'https://news.futunn.com/new-calendar/events-list?begin_time={0}&end_time=2037-12-31&event_type=["港股除权除息"%2C"美股除权除息"%2C"A股除权除息"]&stock_type=&_={1}',
            'https://news.futunn.com/new-calendar/events-list?begin_time={0}&end_time=2037-12-31&event_type=["财经事件"]&stock_type=&_={1}',
            'https://news.futunn.com/new-calendar/events-list?begin_time={0}&end_time=2037-12-31&event_type=["经济数据"]&stock_type=&_={1}',
            'https://news.futunn.com/new-calendar/events-list?begin_time={0}&end_time=2037-12-31&event_type=["休市提醒"]&stock_type=&_={1}'
        ]

        for idx in range(0,len(urls),1):

            print(idx)
            url = urls[idx].format(DateUtil.getTodayStr(),int(1000*time.mktime(time.localtime())) + idx)
            print(url)
            logger.info("address current url {0}...".format(url))

            arr = []
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            try:
                res = requests.get(url, headers=header, timeout=60)
                res.raise_for_status()
                if res.status_code == 200:
                    data = res.text
                    js = json.loads(data)

                    list = js['data']['list']
                    for elem in list:
                        # { unique key, drop duplicate
                        #     "market_type": 1,
                        #     "event_type": 1,
                        #     "event_time": 1
                        # }
                        # elem['event_type']
                        # elem['market_type']
                        # elem['event_time']
                        #itemTime = DateUtil.string_toDatetime(elem['time'])

                        # 'event_type': '港股新股',
                        # 'market_type': 'HK',
                        # 'event_text': '认购中<br/><a href="http://www.futunn.com/quote/stock?m=hk&code=01832" target="_blank" data-market="hk" data-code="01832" class="js-nn-stock">海天地悦旅(01832)</a><br/><a href="http://www.futunn.com/quote/stock?m=hk&code=02230" target="_blank" data-market="hk" data-code="02230" class="js-nn-stock">羚邦集团(02230)</a><br/>',
                        # 'event_time': '2019-05-05 00:00:00',
                        # 'total': 2}

                        # if itemTime > lasttime:
                        #     arr.append( elem )
                        #     logger.info(elem)
                        # else:
                        #     continue

                        arr.append(elem)

                    if len(arr) > 0 :
                        self.mongodbutil_calendar.insertItems(arr)
                        logger.info("store items to mongodb ...")
                    else:
                        logger.info("still have no calendar live message")

            except Exception as err:
                #time.sleep(4 * random.random())
                logger.warning(err)
            except requests.exceptions.ConnectTimeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except requests.exceptions.ReadTimeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except requests.exceptions.Timeout as err:
                logger.warning(err)
                ret_code = -1
                ret_data = err
            except:
                logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(random.random())
                ret_code = -1
                ret_data = ''
            finally:
                res.close()

        return 1, 'ok'


    def get_item_array(self):
        return self.itemArray

    def clear_item_array(self):
        return self.itemArray.clear()
