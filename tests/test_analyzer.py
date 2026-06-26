from app.services import analyzer


def test_analyzer_module_exists():
    assert analyzer is not None