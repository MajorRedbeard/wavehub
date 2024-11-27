
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .routes.main import main
    from .routes.services import services
    from .routes.ports import ports

    app.register_blueprint(main)
    app.register_blueprint(services, url_prefix='/services')
    app.register_blueprint(ports, url_prefix='/ports')

    return app
