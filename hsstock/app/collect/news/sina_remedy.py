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

    # PreResUrl = ''.join(
    #     (os.path.abspath(''.join((__file__, '../../../'))), AppConfig.get_config().get('tf_idf', 'pre.res.filename')))
    # config = AppConfig.get_config()
    # interval = config.getfloat('portal', 'timer.interval')
    # timer = threading.Timer(interval, make_keyword, args=[interval, PreResUrl])
    # timer.start()
    # make_tag()
    connection = mongodbutil.collection

    logger.info('Starting time: {}'.format(datetime.datetime.now()))

    # for s in connection.find({}):
    #     content = str(s['content'])
    #     if content.startswith('\n\n\n\n\n\n\n\n'):
    #         content = content.partition('\n\n\n\n\n\n\n\n')
    #         if content.__len__() == 3:
    #             content = content[2].partition('\n\n\n\n\n\n\n\n')
    #             if content.__len__() ==3 and content[0].startswith('.ct_hqimg'):
    #                 content = content[2]
    #                 connection.update({"_id": s['_id']}, {"$set": {"content": content}})

    isDateCount = 0
    for s in connection.find({}):
        url = str(s['href'])
        if isinstance(s['date'], str):
            date = None
            strDate = s['date']
            try:
                strDate = strDate.replace('  </a>','')
                date = DateUtil.string_toDatetime(strDate)
            except:
                print('2')


            if date is not None:
                connection.update_one({"_id": s['_id']}, {"$set": {"date": date}})
            else:
                try:
                    date = DateUtil.string_toDatetime2(strDate)

                    if date is not None:
                        connection.update_one({"_id": s['_id']}, {"$set": {"date": date}})
                    else:
                        connection.delete_one({"_id": s['_id']})
                except:
                    print('3')


        else:
            isDateCount = isDateCount+1
            if isDateCount > 10000:
                print(isDateCount)
                isDateCount = 0

    logger.info('Ending time: {}'.format(datetime.datetime.now()))