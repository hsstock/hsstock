import logging
import os
import shutil
import os

from hsstock.utils.date_util import DateUtil

logname = ''.join((os.path.abspath(''.join((__file__, '..{}..{}'.format(os.sep,os.sep,os.sep)))), '{}log.txt'.format(os.sep)))
filehandler = logging.FileHandler(filename=logname, encoding="utf-8")
fmter = logging.Formatter(fmt="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
filehandler.setFormatter(fmter)
loger = logging.getLogger(logname)
loger.addHandler(filehandler)
loger.setLevel(logging.INFO)


def info(msg):
    file_size_control()
    loger.info(msg)


def warning(msg):
    file_size_control()
    loger.info(msg)


def file_size_control():
    if os.path.getsize(logname) > 100000000:
        filehandler.close()
        os.rename(logname, logname.replace('log.txt',"log-{}.txt".format(DateUtil.getDatetimeToday4())))
        file = open(logname, "w", encoding='utf-8', errors='ignore')
        file.seek(0)
        file.truncate()
