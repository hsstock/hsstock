import unittest

from hsstock.utils.emailplugin import EmailNotification
from hsstock.utils.app_config import AppConfig

class EmailPluginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = AppConfig.get_config()
        cls.sender = config.get('sender', 'sender')
        cls.password = config.get('sender', 'password')
        cls.smtpserver = config.get('sender', 'smtpserver')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')


    def test_send_mail(self):
        en = EmailNotification()
        en.set_enable(True)
        en.set_sender(EmailPluginTestCase.sender,EmailPluginTestCase.password,EmailPluginTestCase.smtpserver)
        en.send_email('jiabao_hu@corp.netease.com', 'subject', 'words')


unittest.main