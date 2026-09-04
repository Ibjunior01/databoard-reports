"""
Configurações da aplicação DataBoard Reports.
"""

import os
from pathlib import Path
from typing import ClassVar

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Configuração base compartilhada entre os ambientes.
    """

    APP_NAME = "DataBoard Reports"
    APP_TIMEZONE = os.getenv(
        "APP_TIMEZONE",
        "America/Fortaleza",
    )

    SECRET_KEY = os.getenv("SECRET_KEY")

    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    UPLOAD_FOLDER = Path(
        os.getenv(
            "UPLOAD_FOLDER",
            BASE_DIR / "app" / "uploads",
        )
    )

    REPORTS_FOLDER = Path(
        os.getenv(
            "REPORTS_FOLDER",
            BASE_DIR / "app" / "reports",
        )
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///databoard.sqlite3",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS: ClassVar[set[str]] = {
        "csv",
        "xlsx",
        "xls",
    }


class DevelopmentConfig(Config):
    """
    Configuração utilizada no desenvolvimento local.
    """

    DEBUG = True


class TestingConfig(Config):
    """
    Configuração utilizada nos testes automatizados.
    """

    TESTING = True
    WTF_CSRF_ENABLED = False

    SECRET_KEY = "test-secret-key"


class ProductionConfig(Config):
    """
    Configuração utilizada no ambiente de produção.
    """

    DEBUG = False

    @classmethod
    def validate(cls) -> None:
        """
        Garante que configurações obrigatórias de produção existam.
        """

        if not cls.SECRET_KEY:
            raise RuntimeError(
                "A variável de ambiente SECRET_KEY é obrigatória em produção."
            )
