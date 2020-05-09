from api.models import ProductCategory


class CategoryRepository:

    @staticmethod
    def get(cat):
        try:
            cat = int(cat)
        except ValueError:
            return ProductCategory.query.filter_by(slug=cat).first()
        return ProductCategory.query.get(cat)

    @staticmethod
    def get_all():
        return ProductCategory.query

    @staticmethod
    def get_all_by_product(prod):
        return ProductCategory.query.filter_by(product_id=prod).all()