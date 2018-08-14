import unittest
import itertools

class ItertoolsTestCase(unittest.TestCase):

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


    def test_permutations(self):
        items = [1,2,3,4]
        for item in itertools.permutations(items):
            print(item)

    def test_combinations(self):
        items = [1, 2, 3, 4]
        for item in itertools.combinations(items,2):
            print(item)

    def test_combinations_with_replacement(self):
        items = [1, 2, 3, 4]
        for item in itertools.combinations_with_replacement(items,2):
            print(item)

    def test_combinations_with_replacement(self):
        abc = ['a','b','c']
        dfe = ['d','e','f']
        for item in itertools.product(abc, dfe):
            print(item)




unittest.main