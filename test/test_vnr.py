import unittest
from webrake.vnr_scraper import Vnr

__author__ = 'toor'


class TestVnr(unittest.TestCase):

    def setUp(self):
        self.vnr_test = Vnr("fuck")

    def test_vnr_get_price_method_returns_correct_result(self):
        vnr_test = Vnr("http://www.hagkaup.is/vorur/vnr/74")
        result = vnr_test.get_price()
        self.assertEqual(179, result)

if __name__ == '__main__':
    unittest.main()