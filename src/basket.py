class Basket:
    items: dict = {}

    def add(self, product_id, name):
        if product_id not in self.items.keys():
            self.items[product_id] = name


    def remove(self, product_id):
       if product_id in self.items.keys():
           self.items.pop(product_id)


    def check_product(self, product_id):
        if product_id in list(self.items.keys()):
            return True
        else:
            return False
