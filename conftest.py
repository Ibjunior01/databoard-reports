import sys
from pathlib import Path

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app()
    app.config.update(
        TESTING=True,
        UPLOAD_FOLDER=tmp_path,
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()