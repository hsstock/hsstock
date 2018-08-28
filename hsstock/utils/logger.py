import logging
import os

logname = ''.join((os.path.abspath(''.join((__file__, '../../'))), '/log.txt'))
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
    if os.path.getsize(logname) > 104857600:
        file = open(logname, "w", encoding='utf-8', errors='ignore')
        file.seek(0)
        file.truncate()
