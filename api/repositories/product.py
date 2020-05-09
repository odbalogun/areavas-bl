from api.models import Product


class ProductRepository:

    @staticmethod
    def get(prod):
        try:
            prod = int(prod)
        except ValueError:
            return Product.query.filter_by(slug=prod).first()
        return Product.query.get(prod)

    @staticmethod
    def get_all():
        return Product.query
