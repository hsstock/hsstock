import pymongo
import re
import datetime

from hsstock.utils.app_config import AppConfig
from hsstock.utils.mongodbutil import MongodbUtil
import hsstock.utils.logger as logger
from hsstock.utils.date_util import DateUtil

if __name__ == '__main__':
    AppConfig.get_config()
    mongodbutil = MongodbUtil(AppConfig.mongodb_ip, AppConfig.mongodb_port, AppConfig.mongodb_collection)
    mongodbutil2 = MongodbUtil('47.111.187.230', 27017, AppConfig.mongodb_collection)

    # PreResUrl = ''.join(
    #     (os.path.abspath(''.join((__file__, '../../../'))), AppConfig.get_config().get('tf_idf', 'pre.res.filename')))
    # config = AppConfig.get_config()
    # interval = config.getfloat('portal', 'timer.interval')
    # timer = threading.Timer(interval, make_keyword, args=[interval, PreResUrl])
    # timer.start()
    # make_tag()
    connection2 = mongodbutil2.collection
    connection = mongodbutil.collection

    logger.info('Starting time: {}'.format(datetime.datetime.now()))

    for s in connection.find({}):
        url = str(s['href'])
        if isinstance(s['date'],str):
            s['date'] = DateUtil.string_toDatetime(s['date'])
        if not mongodbutil2.urlIsExist(url):
            mongodbutil2.insertItems(s)

    logger.info('Ending time: {}'.format(datetime.datetime.now()))