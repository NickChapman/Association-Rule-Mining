class AssociationRuleMiner(object):
    """Uses market basket analysis to generate association rules"""
    
    def __init__(self, basket_data):
        self.basket_data = basket_data