from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .db import db

csrf = CSRFProtect()

migrate = Migrate()
cors = CORS()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_pyfile('default_config.py')
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app=app, db=db)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    login_manager = LoginManager()
    login_manager.login_view = 'auth_blp.login'
    login_manager.init_app(app)
    from .models import UserModel
    from .routes import auth_blp,home_blp
    app.register_blueprint(auth_blp, url_prefix="/")
    app.register_blueprint(home_blp, url_prefix="/dash")

    @login_manager.user_loader
    def load_user(id):
        return UserModel.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', user=current_user), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html', user=current_user), 500

    return app
