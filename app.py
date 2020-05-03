from flask import Flask, url_for, render_template
from flask.blueprints import Blueprint
from flask_security import Security
from flask_admin import helpers as admin_helpers
from flasgger import Swagger
from adminlte.admin import AdminLte, admins_store
from api.admin.base import FaLink
from api.admin.views import AdminView
from config import config, host, port
import api.routes

from api.models import db, AdminUser

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
db.app = app
# migrate = Migrate(app, db)


# AdminLTE Panel
security = Security(app, admins_store)
admin = AdminLte(app, skin='green', name='StickerAdmin', short_name="<b>S</b>A", long_name="<b>Sticker</b>Admin")
admin.add_link(FaLink(name="Documentation", icon_value='fa-book', icon_type="fa", url='/docs/'))
# admin.add_view(UserView(User, db.session, name="Users", menu_icon_value='fa-users'))
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


# Swagger
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "FlaskCMS",
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
    app.run(host=host, port=port)
