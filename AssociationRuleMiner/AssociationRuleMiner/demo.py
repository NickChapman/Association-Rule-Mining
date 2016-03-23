from data_parser import DataBasket, DataFileParser
from AssociationRuleMiner import AssociationRuleMiner

normal_parser = DataFileParser("ar_test_data/products", "ar_test_data/small_basket.dat")
tiny_parser = DataFileParser("ar_test_data/tiny_test_products.prod", "ar_test_data/tiny_test_basket.bsk")
data = DataBasket()
processed_files = normal_parser.process_files()
data.products_list = processed_files['products_list'] # Note the order in which we set these. The reverse will raise an error
data.basket_matrix = processed_files['basket_matrix']

# Pairs of (support, confidence) values we want to test
# The pair (.2, .75) is omitted because we first run it manually
test_threshold_pairs = [(.4, .75),
                        (.5, .75),
                        (.2, .6),
                        (.4, .6),
                        (.5, .6)]

generated_rules = []

miner = AssociationRuleMiner(data, .2, .75)
miner.full_run_with_report()
generated_rules.append(miner.association_rules)

for test_pair in test_threshold_pairs:
    miner.support_threshold = test_pair[0]
    miner.confidence_threshold = test_pair[1]
    miner.full_run_with_reporr()
    generated_rules.append(miner.association_rules)

