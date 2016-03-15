from data_parser import DataBasket, DataFileParser

parser = DataFileParser("ar_test_data/products", "ar_test_data/small_basket.dat")
data = DataBasket()
processed_files = parser.process_files()
data.products_list = processed_files['products_list'] # Note the order in which we set these. The reverse will raise an error
data.basket_matrix = processed_files['basket_matrix']
