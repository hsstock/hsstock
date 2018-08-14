import os
import json
import logging.config

def setup_logging(
    default_path='./../../data/logging_config.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


#
# import logging
# from datetime import datetime
# import os
#
# logger = logging.getLogger('FT')
# log_level = logging.DEBUG
# is_file_log = True
#
# # 设置logger的level为DEBUG
# logger.setLevel(log_level)
#
# # 创建一个输出日志到控制台的StreamHandler
# hdr = logging.StreamHandler()
# formatter = logging.Formatter(
#     '%(asctime)s [%(filename)s] %(funcName)s:%(lineno)d: %(message)s')
# hdr.setFormatter(formatter)
#
# # 给logger添加上handler
# logger.addHandler(hdr)
#
# # 添加文件handle
# if is_file_log:
#     filename = 'hs_' + datetime.now().strftime('%Y%m%d') + '.log'
#     tempPath = os.path.join(os.getcwd(), 'log')
#     if not os.path.exists(tempPath):
#         os.makedirs(tempPath)
#     filepath = os.path.join(tempPath, filename)
#     fileHandler = logging.FileHandler(filepath)
#     fileHandler.setLevel(log_level)
#     fileHandler.setFormatter(formatter)
#     logger.addHandler(fileHandler)
#
#
