class ProductService:

    @staticmethod
    def description(product):
        text = f"{product.name}\n\n{product.description}"
        return text
