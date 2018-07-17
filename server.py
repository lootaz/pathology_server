from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object("common.config.DevelopmentConfig")

    CORS(app)
    # CORS(app, resource={r"/*": {"origins": "*"}})

    from common.models import db
    db.init_app(app)

    from blueprints.api.views import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(app.config.get("HOST"), app.config.get("PORT"))