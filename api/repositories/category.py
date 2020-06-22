from api.models import Category


class CategoryRepository:

    @staticmethod
    def get(cat):
        try:
            cat = int(cat)
        except ValueError:
            return Category.query.filter_by(slug=cat).first()
        return Category.query.get(cat)

    @staticmethod
    def get_all():
        return Category.query