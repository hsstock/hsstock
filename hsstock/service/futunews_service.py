# -*- coding: UTF-8 -*-
import requests
import bs4
import time
import random
import hsstock.utils.logger as logger
from hsstock.utils.date_util import DateUtil
from hsstock.utils.decorator import retry


class FutunnService(object):
    def __init__(self, mongodbutil):
        self.itemArray = []
        self.mongodbutil = mongodbutil
        self.url = 'https://news.futunn.com/main'


    @retry(wait=30)
    def get_info(self):

        ret_code = -1
        ret_data = ''
        self.itemArray = []

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

        for i in range(69000,100000,1):
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

    def get_item_array(self):
        return self.itemArray

    def clear_item_array(self):
        return self.itemArray.clear()
