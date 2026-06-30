import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Configurações centrais da aplicação.

    Nesta primeira entrega, ainda não usaremos banco de dados,
    upload de arquivos ou geração de relatórios. As pastas já ficam
    configuradas para facilitar a evolução do projeto nas próximas etapas.
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    APP_NAME = "DataBoard Reports"

    UPLOAD_FOLDER = BASE_DIR / "app" / "uploads"
    REPORTS_FOLDER = BASE_DIR / "app" / "reports"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

    SQLALCHEMY_DATABASE_URI = "sqlite:///databoard.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False