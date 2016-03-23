from data_parser import DataBasket, DataFileParser
from AssociationRuleMiner import AssociationRuleMiner

normal_parser = DataFileParser("ar_test_data/products", "ar_test_data/small_basket.dat")
tiny_parser = DataFileParser("ar_test_data/tiny_test_products.prod", "ar_test_data/tiny_test_basket.bsk")
data = DataBasket()
processed_files = tiny_parser.process_files()
data.products_list = processed_files['products_list'] # Note the order in which we set these. The reverse will raise an error
data.basket_matrix = processed_files['basket_matrix']

miner = AssociationRuleMiner(data, .125, .1)
miner.build_frequent_item_sets()
for level_k in miner.frequent_item_sets:
    for item_set in level_k:
        for elem in item_set:
            print(str(elem) + ", ", end="")
        print()

from itertools import combinations
subs = combinations(miner.frequent_item_sets[-1][0],1)
for s in subs:
    item_set = s
    for elem in item_set:
        print(str(elem) + ", ", end="")
    print()


