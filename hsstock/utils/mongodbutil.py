from pymongo import MongoClient
from hsstock.utils.app_config import AppConfig

class MongodbUtil(object):
    def __init__(self,ip,port,collection):
        self.ip = ip
        self.port = port
        self.client = MongoClient(ip,port)
        self.db = self.client.admin
        self.db.authenticate(AppConfig.mongodb_user,AppConfig.mongodb_password)
        #self.db.authenticate(' ', ' ')
        self.collection = self.db[collection]


    # item and items, all both ok
    def insertItems(self,items):
        self.collection.insert(items)

    def urlIsExist(self,url):
        items = self.collection.find({"href":url})
        for item in items:
            return True
        return False

    def getLastLivetime(self):
        items = self.collection.find().sort("time", -1)
        for item in items:
            return item["time"]
        return '2018-05-01 09:00'
