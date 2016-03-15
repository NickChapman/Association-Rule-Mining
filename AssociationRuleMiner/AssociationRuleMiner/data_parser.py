from data_parser.DataBasket import Product

class DataFileParser(object):
    """Loads the data file and returns a data object"""
    def __init__(self, products_file, basket_file):
        self.products_file = products_file
        self.basket_file = basket_file

    def process_files(self):
        products_list = self.build_products_list()
        basket_matrix = self.build_basket_matrix()
        return {'products_list' : products_list, 'basket_matrix' : basket_matrix }

    def build_products_list(self):
        """Reads the products file and creates a products list
        @returns The completed product list
        """
        products_list = []
        with open(self.products_file) as f:
            for line in f.readlines:
                parts = [x.strip() for x in line.split(',')]
                product_name = parts[0]
                # We now determine the best numeric type for the product price
                try:
                    product_price = int(parts[1])
                except ValueError:
                    # The price is either a decimal like 2.99 or not a valid price
                    try:
                        product_price = float(parts[1])
                    except ValueError:
                        # The price is not the correct format
                        raise ValueError("The products file contains an invalid price for the item: " + product_name)
                products_list.append(Product(product_name, product_price))
        return products_list

    def build_basket_matrix(self):
        """Reads the basket file and builds the basket matrix
        """
        basket_matrix = []
        with open(self.basket_file) as f:
            for line in f.readlines:
                try:
                    parts = [int(x.strip) for x in line.split(',')]
                    # If the int cast in the previous line fails then the market basket data is corrupted
                except ValueError:
                    raise ValueError("The basket file contains non numeric data.")
                # We don't care about the transaction number so we ignore it
                basket_matrix.append(parts[1:])
        return basket_matrix

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

