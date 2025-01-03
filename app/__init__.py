
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .routes.main import main
    from .routes.services import services
    from .routes.ports import ports
    from .routes.nginx import nginx
	from .routes.settings import settings_bp


    app.register_blueprint(main)
    app.register_blueprint(services, url_prefix='/services')
    app.register_blueprint(ports, url_prefix='/ports')
    app.register_blueprint(nginx, url_prefix='/nginx')
	app.register_blueprint(settings_bp, url_prefix='/settings')


    return app
