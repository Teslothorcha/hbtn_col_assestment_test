from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

bootstrap = Bootstrap()
app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dreamful'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def create_app():
    """Create Flask application."""
    app.config.from_object(os.environ['APP_SETTINGS'])
    migrate = Migrate()
    migrate.init_app(app, db)

    with app.app_context():
        # Import parts of our application
        from app.views import order
        # Register Blueprints
        app.register_blueprint(order.order_bp)
        bootstrap.init_app(app)
        return app