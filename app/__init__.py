"""
Application Factory do DataBoard Reports.
"""

from pathlib import Path

from flask import Flask

from app.config import Config, TestingConfig
from app.extensions import db


def create_app(test_config=None):
    """
    Cria e configura a aplicação Flask.

    Quando TESTING=True é informado, utiliza explicitamente
    a configuração dedicada ao ambiente de testes.
    """

    app = Flask(__name__)

    if test_config and test_config.get("TESTING"):
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True,
    )

    db.init_app(app)

    from app import models  # noqa: F401
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app