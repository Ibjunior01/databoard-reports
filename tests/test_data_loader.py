from app.services import data_loader


def test_data_loader_module_exists():
    assert data_loader is not None