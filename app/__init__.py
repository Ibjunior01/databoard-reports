"""
Application Factory do DataBoard Reports.
"""

import os
from pathlib import Path

from flask import Flask, flash, redirect, url_for
from werkzeug.exceptions import RequestEntityTooLarge

from app.config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
)
from app.datetime_utils import (
    format_local_datetime,
    get_timezone,
)
from app.extensions import csrf, db

CONFIG_BY_ENV = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def create_app(test_config=None):
    """
    Cria e configura a aplicação Flask.

    Os testes utilizam sempre TestingConfig.

    Fora dos testes, o ambiente é definido por APP_ENV.
    Quando APP_ENV não é informado, production é utilizado
    como padrão seguro.
    """

    app = Flask(__name__)

    if test_config and test_config.get("TESTING"):
        config_class = TestingConfig
    else:
        environment = (
            os.getenv(
                "APP_ENV",
                "production",
            )
            .strip()
            .lower()
        )

        try:
            config_class = CONFIG_BY_ENV[environment]
        except KeyError as exc:
            raise RuntimeError(
                "APP_ENV inválido. Use 'development' ou 'production'."
            ) from exc

    app.config.from_object(config_class)

    if config_class is ProductionConfig:
        ProductionConfig.validate()

    if test_config:
        app.config.update(test_config)

    get_timezone(app.config["APP_TIMEZONE"])

    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True,
    )

    def local_datetime_filter(
        value,
        format_string="%d/%m/%Y %H:%M",
    ):
        return format_local_datetime(
            value,
            format_string=format_string,
            timezone_name=app.config["APP_TIMEZONE"],
        )

    app.jinja_env.filters["local_datetime"] = local_datetime_filter

    db.init_app(app)
    csrf.init_app(app)

    from app import models  # noqa: F401
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        """
        Trata uploads que excedem MAX_CONTENT_LENGTH.
        """

        current_limit = app.config["MAX_CONTENT_LENGTH"]
        limit_mb = current_limit // (1024 * 1024)

        flash(
            f"O arquivo excede o limite máximo de {limit_mb} MB.",
            "error",
        )

        return redirect(url_for("main.upload_file"))

    with app.app_context():
        db.create_all()

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        return response

    return app
