"""
Configurações da aplicação DataBoard Reports.
"""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Configuração base compartilhada entre os ambientes.
    """

    APP_NAME = "DataBoard Reports"

    SECRET_KEY = os.getenv("SECRET_KEY")

    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    UPLOAD_FOLDER = BASE_DIR / "app" / "uploads"
    REPORTS_FOLDER = BASE_DIR / "app" / "reports"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

    SQLALCHEMY_DATABASE_URI = "sqlite:///databoard.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
