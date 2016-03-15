class DataBasket(object):
    """Stores information about products and their sales"""
    def __init__(self, **kwargs):
        if len(basket_matrix[0]) != len(product_map):
            raise AssertionError("A basket matrix entry must be the same length as the product map")
        if 'products_list' in kwargs:
            self.products_list = kwargs['products_list']
        else:
            self.products_list = None
        if 'basket_matrix' in kwargs:
            if self.products_list == None:
                raise AssertionError('A basket matrix can not exist before a products list')
            self.basket_matrix = kwargs['basket_matrix']
        else:
            self.basket_matrix = None

    @property
    def products_list(self):
        return self.products_list

    @products_list.setter
    def products_list(self, value):
        """Sets the product list and clears any existing basket matrix"""
        self.basket_matrix = None
        self.products_list = value

    @property
    def basket_matrix(self):
        return self.basket_matrix

    @basket_matrix.setter
    def basket_matrix(self, value):
        """Sets the basket matrix
        Ensures that a products list exists first
        Ensures that the basket matrix matches up with the products list
        """
        if self.products_list == None:
            raise AssertionError('A product list must exist before a basket matrix')
        if len(self.products_list) != len(value[0]):
            raise AssertionError('A basket matrix entry must be the same length as the products list')
        self.basket_matrix = value

class Product(object):
    """Stores the name of a product and its price"""
    def __init__(self, name, price):
        if not (isinstance(price, int) or isinstance(price, float)):
            raise ValueError("The price of a product must be numeric")
        self.name = name
        self.price = price

