from itertools import combinations


class AssociationRuleMiner(object):
    """Uses market basket analysis to generate association rules"""
    
    def __init__(self, basket_data, support_threshold, confidence_threshold):
        """ Constructor for the Association Rule Miner
        @param basket_data: A DataBasket object containing the pertinent data
        """
        self.__basket_data = basket_data
        self.support_threshold = support_threshold
        self.confidence_threshold = confidence_threshold
        self.confidence_counts = {}
        self.association_rules = []

    @property
    def basket_data(self):
        return self.__basket_data

    @basket_data.setter
    def basket_data(self, value):
        """ Basket data setter
        Makes sure to clear all previous confidence counts and rules
        """
        self.__basket_data = value
        self.confidence_counts = 0
        self.association_rules = 0

    def build_frequent_item_sets(self):
        """ Uses an Apriori approach to generate all frequent item sets
        Terminates when at a given k level there is no more than 1 frequent item set.
        """
        # First construct the size k = 1 item sets
        self.frequent_item_sets = []
        level_1_frequent_item_sets = []
        possible_item_sets = []
        for product in self.basket_data.products_list:
            possible_item_sets.append(frozenset([product]))
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

    def get_association_rules(self):
        # We note that item sets of size 1 cannot give us a rule
        self.association_rules = []
        for i in range(1, len(self.frequent_item_sets)):
            for item_set in self.frequent_item_sets[i]:
                possible_rules = self.get_possible_rules(item_set)
                for rule in possible_rules:
                    if (rule.support >= self.support_threshold and
                        rule.confidence >= self.confidence_threshold and
                        rule.lift >= 1):
                        self.association_rules.append(rule)

    def sort_association_rules(self):
        """ Sorts the association rules in order of confidence and lift descending"""
        if len(self.association_rules) > 0:
            self.association_rules.sort(key=lambda x: x.lift, reverse=True)
            self.association_rules.sort(key=lambda x: x.confidence, reverse=True)

    def get_possible_rules(self, frequent_item_set):
        """ Generates all of the possible rules from the frequent item set
        This process is slightly inefficient and could be improved
        It doubles up some of its work since all possible 2->3 rules are just 3->2 rules
        @param frequent_item_set: The item set to generate rules from
        """
        possible_rules = []
        # We generate the item set support since it is also
        # going to be the support of all of the rules that we generate
        item_set_support_count = 0
        for item_set in self.basket_data.item_sets:
            if frequent_item_set.issubset(item_set):
                item_set_support_count += 1
        # Now calculate all of the possible rules
        for antecedent_size in range(1, len(frequent_item_set)):
            consequent_size = len(frequent_item_set) - antecedent_size
            antecedent_combinations = combinations(frequent_item_set, antecedent_size)
            consequent_combinations = combinations(frequent_item_set, consequent_size)
            # We now convert the generators to list so Python doesn't freak out
            antecedents = []
            for antecedent in antecedent_combinations:
                antecedents.append(frozenset(antecedent))
            consequents = []
            for consequent in consequent_combinations:
                consequents.append(frozenset(consequent))
            for antecedent in antecedents:
                for consequent in consequents:
                    if len(antecedent.intersection(consequent)) == 0:
                        # We already have the support so we just need the confidence and lift
                        basket_size = len(self.basket_data.item_sets)
                        support = item_set_support_count / basket_size
                        if antecedent not in self.confidence_counts:
                            confidence_count = 0
                            for item_set in self.basket_data.item_sets:
                                if antecedent.issubset(item_set):
                                    confidence_count += 1
                            self.confidence_counts[antecedent] = confidence_count
                        else:
                            confidence_count = self.confidence_counts[frozenset(antecedent)]
                        confidence = item_set_support_count / confidence_count
                        expected_confidence = confidence_count / basket_size
                        lift = confidence / expected_confidence
                        possible_rules.append(
                            AssociationRule(antecedent, consequent, support, confidence, lift)
                            )
        return possible_rules

    def full_run_with_report(self):
        print("Generating rules with")
        print("\tmin-support    : " + str(self.support_threshold))
        print("\tmin-confidence : " + str(self.confidence_threshold))
        print()
        print("Generating frequent item sets.....", end="")
        self.build_frequent_item_sets()
        print("Done")
        for k, item_sets in enumerate(self.frequent_item_sets):
            print("\tNumber of k=" + str(k+1) + " item sets: " + str(len(item_sets)))
        print()
        print("Building association rules.....", end="")
        self.get_association_rules()
        print("Done")
        print("Sorting association rules.....", end="")
        self.sort_association_rules()
        print("Done")
        print("Rule generation complete....." + str(len(self.association_rules)) + " rules found")
        print()
        if len(self.association_rules) > 0:
            print("Rules:")
            for rule in self.association_rules:
                print("\t* " + str(rule) + " ; Sup=" + str(format(rule.support, ".3f")) + 
                      " ; Conf=" + str(format(rule.confidence, ".3f")) +
                      " ; Lift=" + str(format(rule.lift, ".3f")))
        print()


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

    def __repr__(self):
        return "AssociationRule()"

    def __str__(self):
        ant_str = ""
        for ant in self.antecedent:
            ant_str += str(ant) + " + "
        ant_str = ant_str[:-3]
        cons_str = ""
        for cons in self.consequent:
            cons_str += str(cons) + " + "
        cons_str = cons_str[:-3]
        return ant_str + " -> " + cons_str

    def __eq__(self, other):
        if isinstance(other, AssociationRule):
            if (len(self.antecedent.difference(other.antecedent)) == 0 and
                len(self.consequent.difference(other.consequent)) == 0 and
                self.lift == other.lift and
                self.confidence == other.confidence and
                self.support == other.support):
                return True
        else:
            return False

    @staticmethod
    def __fnv1a_64(string):
        """ Hashes a string using the 64 bit FNV1a algorithm
        Used here simply as a utility
        For more information see:
            https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function
        @param string The key to hash
        @returns Hashed key
        """
        fnv_offset = 0xcbf29ce484222325 # The standard FNV 64 bit offset base
        fnv_prime = 0x100000001b3 # The standard FNV 64 digit prime
        hash = fnv_offset
        uint64_max = 2 ** 64
        # Iterate through the bytes of the string, ie the characters
        for char in string:
            # ord() converts the character to its unicode value
            hash = hash ^ ord(char)
            hash = (hash * fnv_prime) % uint64_max
        return hash

    def __hash__(self):
        hash_str = ""
        for item in self.antecedent:
            hash_str += item.name
        hash_str += "->"
        for item in self.consequent:
            hash_str += item.name
        return self.__fnv1a_64(hash_str)