import requests
import bs4
import time
import random
import hsstock.utils.logger as logger
from hsstock.utils.date_util import DateUtil
from hsstock.utils.decorator import retry


class SinanewsService(object):
    def __init__(self, mongodbutil):
        self.itemArray = []
        self.mongodbutil = mongodbutil


    @retry()
    def get_page(self,market, code,url):

        ret_code = -1
        ret_data = ''
        self.itemArray = []

        try:
            res = requests.get(url,timeout=60)
            res.encoding = "gbk"

            res.raise_for_status()
            if res.status_code == 200 :
                    contentSoup = bs4.BeautifulSoup(res.text,'lxml')
                    elems = contentSoup.select('#js_ggzx > li,.li_point > ul > li,.col02_22 > ul > li')
                    for elem in elems:
                        json = {}
                        json['code'] = code
                        temp = elem.__str__()[4:5]
                        if (temp == '\n') and market == 'US':
                            continue
                        ele = elem.select('span')
                        json['date'] = DateUtil.format_date(ele[0].getText()[1:-1])
                        s = json['date']
                        ele = elem.select('a')
                        json['title'] = ele[len(ele)-1].getText()
                        logger.info("date:{},title:{}".format(s, json['title']))
                        json['href'] = ele[len(ele)-1].attrs['href']
                        json['year'] = 'guess'
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

    def generate_page_url(self, market, code, page):
        """
        HK: http://stock.finance.sina.com.cn/hkstock/go/CompanyNews/page/1/code/00771.html
        US: http://biz.finance.sina.com.cn/usstock/usstock_news.php?pageIndex=1&symbol=ntes&type=1
        SH: http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh603722&Page=1
        SZ: http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000063&Page=1
        """
        if market == 'HK':
            return 'http://stock.finance.sina.com.cn/hkstock/go/CompanyNews/page/' + str(
                page) + '/code/' + code + '.html'
        if market == 'US':
            return 'http://biz.finance.sina.com.cn/usstock/usstock_news.php?pageIndex=' + str(
                page) + '&symbol=' + code + '&type='
        if market == 'SH':
            return 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=' + str.lower(
                market) + code + '&Page=' + str(
                page)
        if market == 'SZ':
            return 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=' + str.lower(
                market) + code + '&Page=' + str(
                page)
        else:
            return "url not found"

    @retry()
    def get_hk_page(self, market, code, page):
        """
        :param market:
        :param code:
        :param page:
        :return:  page number, -1: failed
        """
        self.itemArray = []

        url = self.generate_page_url(market, code, page)
        logger.info('fetch url: {}'.format(url))

        try:
            res = requests.get(url, timeout=60)
            res.encoding = "gbk"
            res.raise_for_status()
            if res.status_code == 200:
                contentSoup = bs4.BeautifulSoup(res.text, 'lxml')
                elems = contentSoup.select('#js_ggzx > li,.li_point > ul > li,.col02_22 > ul > li')
                if len(elems) < 2:
                    return -1,''
                for elem in elems:
                    json = {}
                    json['code'] = code
                    ele = elem.select('span')
                    if len(ele) == 0:
                        continue
                    json['date'] = ele[0].getText()
                    s = json['date']
                    ele = elem.select('a')
                    json['title'] = ele[len(ele) - 1].getText()
                    logger.info("date:{},title:{}".format(s, json['title']))
                    json['href'] = ele[len(ele) - 1].attrs['href']
                    json['year'] = 'real'
                    ret, content = self.get_content(json['href'], "utf-8")
                    # if ret != -1:
                    #     time.sleep(4 * random.random())

                    if ret == 0:
                        json['content'] = content

                        self.itemArray.append(json)
        except Exception as err:
            #
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
        return page + 1,''

    @retry()
    def get_us_page(self, market, code, page, type):
        """
        :param market:
        :param code:
        :param page:
        :param type:
        :return: (page_number, type), page_number:-1
        """
        self.itemArray = []
        url = self.generate_page_url(market, code, page)
        url = url + type
        logger.info('fetch url: {}'.format(url))
        try:
            res = requests.get(url, timeout=60)
            res.encoding = "gbk"
            res.raise_for_status()
            if res.status_code == 200:
                contentSoup = bs4.BeautifulSoup(res.text, 'lxml')
                elems = contentSoup.select('.xb_news > ul > li')
                if page >= 100:
                    if type.__eq__("1"):
                        return 1, '2'
                    else:
                        return -1, '2'
                for elem in elems:
                    json = {}
                    json['code'] = code
                    ele = elem.select('span')
                    if len(ele) == 0:
                        continue
                    json['date'] = DateUtil.format_date_us_history(ele[0].getText())
                    s = json['date']
                    ele = elem.select('a')
                    json['title'] = ele[len(ele) - 1].getText()
                    logger.info("date:{},title:{}".format(s, json['title']))
                    json['href'] = ele[len(ele) - 1].attrs['href']
                    json['year'] = 'real'
                    ret, content = self.get_content(json['href'], "utf-8")
                    # if ret != -1:
                    #     time.sleep(4 * random.random())

                    if ret == 0:
                        json['content'] = content
                        self.itemArray.append(json)
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
        return page + 1, type

    @retry()
    def get_chn_page(self, market, code, page):
        self.itemArray = []
        url = self.generate_page_url(market, code, page)
        logger.info('fetch url: {}'.format(url))
        try:
            res = requests.get(url, timeout=60)
            res.encoding = "gbk"
            res.raise_for_status()
            if res.status_code == 200:
                contentSoup = bs4.BeautifulSoup(res.text, 'lxml')
                strList = str(contentSoup.select('.datelist > ul'))[10:-12]
                elems = strList.split("<br/>")
                if len(elems) < 2:
                    return -1,''
                for elem in elems:
                    if elem == '':
                        continue
                    json = {}
                    elem = elem.lstrip()
                    parts = elem.split('<a href="')
                    json['code'] = code
                    json['date'] = parts[0].rstrip() + ":00"
                    s = json['date']
                    parts1 = parts[1].split('" target="_blank">')
                    json['href'] = parts1[0]
                    json['year'] = 'real'
                    parts2 = parts1[1].split('</a>')
                    json['title'] = parts2[0]
                    logger.info("date:{},title:{}".format(s, json['title']))
                    ret, content = self.get_content(json['href'], "utf-8")
                    # if ret != -1:
                    #     time.sleep(4 * random.random())

                    if ret == 0:
                        json['content'] = content
                        self.itemArray.append(json)
        except Exception as err:
            #time.sleep(4 * random.random())
            logger.warning(err)
        except:
            logger.warning('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(random.random())
            ret_code = -1
            ret_data = ''
        finally:
            res.close()
        return page + 1,''

    @retry()
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
                elems = soup.select('#artibody,.entry-content')
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

    def get_item_array(self):
        return self.itemArray

    def clear_item_array(self):
        return self.itemArray.clear()
