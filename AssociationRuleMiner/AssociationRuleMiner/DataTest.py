import unittest
from data_parser import DataBasket, DataFileParser, Product

class Test_DataTest(unittest.TestCase):
    def test_file_loader(self):
        parser = DataFileParser("ar_test_data/products", "ar_test_data/small_basket.dat")
        processed_files = parser.process_files()
        self.assertIsInstance(processed_files, dict)
        self.assertIsInstance(processed_files['products_list'][0], Product)
        self.assertIsInstance(processed_files['basket_matrix'][0], list)
        self.assertEqual(len(processed_files['basket_matrix'][0]), len(processed_files['products_list'])) 

    def test_data_basket(self):
        parser = DataFileParser("ar_test_data/products", "ar_test_data/small_basket.dat")
        data = DataBasket()
        processed_files = parser.process_files()
        self.assertRaises(AssertionError, data.basket_matrix, processed_files["basket_matrix"])

if __name__ == '__main__':
    unittest.main()
