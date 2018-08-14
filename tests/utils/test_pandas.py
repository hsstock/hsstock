import unittest
import itertools
import numpy as np
import pandas as pd


class PandasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('tearUpClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')


    def test_qcut(self):
        bins = [-np.inf,-7.0,-5,-3,0,3,5,7,np.inf]
        cats = pd.cut([0.2,2.0,3.0,20.00,90],bins)
        print(cats.value_counts())



unittest.main