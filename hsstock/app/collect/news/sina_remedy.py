import pymongo
import re
import datetime

from hsstock.utils.app_config import AppConfig
from hsstock.utils.mongodbutil import MongodbUtil
import hsstock.utils.logger as logger

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

    for s in connection.find({}):
        content = str(s['content'])
        if content.startswith('\n\n\n\n\n\n\n\n'):
            content = content.partition('\n\n\n\n\n\n\n\n')
            if content.__len__() == 3:
                content = content[2].partition('\n\n\n\n\n\n\n\n')
                if content.__len__() ==3 and content[0].startswith('.ct_hqimg'):
                    content = content[2]
                    connection.update({"_id": s['_id']}, {"$set": {"content": content}})

    logger.info('Ending time: {}'.format(datetime.datetime.now()))