class AssociationRuleMiner(object):
    """Uses market basket analysis to generate association rules"""
    
    def __init__(self, basket_data, support_threshold, confidence_threshold):
        """ Constructor for the Association Rule Miner
        @param basket_data: A DataBasket object containing the pertinent data
        """
        self.basket_data = basket_data
        self.support_threshold = support_threshold
        self.confidence_threshold = confidence_threshold

    def build_frequent_item_sets(self):
        """ Uses an Apriori approach to generate all frequent item sets
        Terminates when at a given k level there is no more than 1 frequent item set.
        """
        # First construct the size k = 1 item sets
        self.frequent_item_sets = []
        level_1_frequent_item_sets = []
        possible_item_sets = []
        for product in self.basket_data.products_list:
            possible_item_sets.append(set([product]))
        for item_set in possible_item_sets:
            support_count = 0
            for basket_set in self.basket_data.item_sets:
                if item_set.issubset(basket_set):
                    support_count += 1
            if (support_count / len(self.basket_data.item_sets)) >= self.support_threshold:
                level_1_frequent_item_sets.append(item_set)
        self.frequent_item_sets.append(level_1_frequent_item_sets)
        k = 1 # They're indexed from 0 so 1 is item sets of length 2
        while len(self.frequent_item_sets[-1]) > 1:
            """ We make sure that the previous level had more than one
            frequent item set in it. If it only had one frequent item set then
            that item set is the largest frequent item set we will ever generate. 
            We know this via a priori. """
            possible_item_sets = []
            level_k_frequent_item_sets = []
            sets_joined = 0 # Counts the sets for which all possible supersets have been created
            total_sets = len(self.frequent_item_sets[k - 1])
            # We generate the possible item sets
            for item_set in self.frequent_item_sets[k - 1]:
                for i in range(sets_joined + 1, total_sets):
                    set_to_join = self.frequent_item_sets[k - 1][i]
                    # We do a little bit of idiot checking here (better safe than sorry)
                    if set_to_join == item_set:
                        # Skip this one
                        continue
                    joined_set = item_set.union(set_to_join)
                    possible_item_sets.append(joined_set)
                sets_joined += 1
            # We determine which possible item sets to keep
            level_k_valid_sets = []
            for item_set in possible_item_sets:
                support_count = 0
                for basket_set in self.basket_data.item_sets:
                    if item_set.issubset(basket_set):
                        support_count += 1
                if ((support_count / len(self.basket_data.item_sets)) >= self.support_threshold 
                    and item_set not in level_k_valid_sets):
                    level_k_valid_sets.append(item_set)
            self.frequent_item_sets.append(level_k_valid_sets)
            k += 1

def build_association_rules(self):
    pass # TODO

class AssociationRule(object):
    """ A single association rule
    Details which antecedents lead to which consequents
    Additionally provides three metrics regarding the rule """

    def __init__(self, antecedent, consequent, support, connfidence, lift):
        self.antecedent = antecedent
        self.consequent = consequent
        self.support = support
        self.confidence = connfidence
        self.lift = lift