from data_parser import DataBasket, DataFileParser
from AssociationRuleMiner import AssociationRuleMiner
from time import time

demo_start_time = time()

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
                        (.5, .6),
                        (.5, .5),
                        (.3, .5)]

generated_rules = []

miner = AssociationRuleMiner(data, .2, .75)
start_time = time()
miner.full_run_with_report()
end_time = time()
print("Run completed in: %.3g seconds" % (end_time - start_time))
print()
print("--------------------------------------------------------------")
generated_rules.extend(miner.association_rules)

for test_pair in test_threshold_pairs:
    miner.support_threshold = test_pair[0]
    miner.confidence_threshold = test_pair[1]
    start_time = time()
    miner.full_run_with_report()
    end_time = time()
    print("Run completed in: %.3g seconds" % (end_time - start_time))
    print()
    print("--------------------------------------------------------------")
    generated_rules.extend(miner.association_rules)

# Gather the top 15 rules based on confidence and lift
# We first make a set to get rid of duplicates
generated_rules = set(generated_rules)
# Then cast back to array to preserve sorting
generated_rules = list(generated_rules)
# We sort on lift then confidence so that confidence is the primary factor
generated_rules.sort(key=lambda x: x.lift, reverse=True)
generated_rules.sort(key=lambda x: x.confidence, reverse=True)
print()
print("Top 15 generated rules based on confidence and lift are:")
for rule in generated_rules[:15]:
    print("\t* " + str(rule) + " ; Sup=" + str(format(rule.support, ".3f")) + 
            " ; Conf=" + str(format(rule.confidence, ".3f")) +
            " ; Lift=" + str(format(rule.lift, ".3f")))

demo_end_time = time()
print("Demo ran in: %.3g seconds" % (demo_end_time - demo_start_time))
