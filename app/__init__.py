"""
Initilizes module od the app
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_login import LoginManager
from flask_mail import Mail

bootstrap = Bootstrap()
app = Flask(__name__)
db = SQLAlchemy(session_options={"expire_on_commit": False})
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
def create_app(class_config=DevelopmentConfig):
    """
    Create Fthe Flask app
    """
    app.config.from_object(class_config)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # Import parts of our application
    from app.views import order
    from app.views import login
    from app.views import public
    from app.views import user
    # Register Blueprints
    app.register_blueprint(order.order_bp)
    app.register_blueprint(login.auth_bp)
    app.register_blueprint(public.public_bp)
    app.register_blueprint(user.user_bp)
    return app