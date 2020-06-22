from flask import Flask, url_for, render_template
from flask.blueprints import Blueprint
from flask_security import Security
from flask_admin import helpers as admin_helpers
from flasgger import Swagger
from adminlte.admin import AdminLte, admins_store
from api.admin.base import FaLink
from api.admin.views import AdminView, SubscriberView, TransactionView, CategoryView
from api.utils.extensions import ma
from pages.views import blueprint as page_blueprint
import api.routes

from api.models import db, AdminUser, Transaction, User, Category, BillingLog, UnsubscriptionLog, Subscription
from config import ConfigObject

app = Flask(__name__)
app.config.from_object(ConfigObject)
db.init_app(app)
db.app = app
ma.init_app(app)
# migrate = Migrate(app, db)


# AdminLTE Panel
# todo fix admin portal
security = Security(app, admins_store)
admin = AdminLte(app, skin='green', name='StickerAdmin', short_name="<b>S</b>A", long_name="<b>Sticker</b>Admin")
admin.add_link(FaLink(name="Documentation", icon_value='fa-book', icon_type="fa", url='/docs/'))
admin.add_view(CategoryView(Category, db.session, name="Categories", menu_icon_value='fa-list-alt'))
admin.add_view(SubscriberView(Subscription, db.session, name="Subscribers", menu_icon_value='fa-users'))
# admin.add_view(AdminView(User, db.session, name="Subscribers", menu_icon_value='fa-users'))
admin.add_view(TransactionView(BillingLog, db.session, name="Transactions", menu_icon_value='fa-credit-card'))
admin.add_view(TransactionView(UnsubscriptionLog, db.session, name="Transactions", menu_icon_value='fa-credit-card'))
admin.add_view(TransactionView(Transaction, db.session, name="Transactions", menu_icon_value='fa-credit-card'))
admin.add_view(AdminView(AdminUser, db.session, name="Administrators", menu_icon_value='fa-user-secret'))
admin.add_link(FaLink(name="Logout", icon_value='fa-sign-out', icon_type="fa", url='/admin/logout'))


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


# Blueprints
app.url_map.strict_slashes = False
for blueprint in vars(api.routes).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint)
app.register_blueprint(page_blueprint)

# Swagger
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Sticker",
    "specs": [
        {
            "version": None,
            "title": "API Docs",
            "description": None,
            "termsOfService": None,
            "endpoint": 'spec',
            "route": '/spec/',
            "rule_filter": lambda rule: True  # all in
        }
    ],
    "static_url_path": "/docs/",
    "specs_route": "/docs/"
}
Swagger(app)


# Custom error pages
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(host=ConfigObject.APP_HOST, port=ConfigObject.APP_PORT)
