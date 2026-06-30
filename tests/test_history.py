from io import BytesIO

from app.models import UploadRecord
from app.services.history import create_upload_record, list_upload_records


def test_create_upload_record_persists_data(app):
    with app.app_context():
        record = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=10,
            column_count=4,
        )

        saved_record = UploadRecord.query.get(record.id)

        assert saved_record is not None
        assert saved_record.file_name == "vendas.csv"
        assert saved_record.file_extension == ".csv"
        assert saved_record.row_count == 10
        assert saved_record.column_count == 4


def test_list_upload_records_returns_newest_first(app):
    with app.app_context():
        first_record = create_upload_record(
            file_name="primeiro.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        second_record = create_upload_record(
            file_name="segundo.csv",
            file_extension=".csv",
            row_count=8,
            column_count=3,
        )

        records = list_upload_records()

        assert records[0].id == second_record.id
        assert records[1].id == first_record.id


def test_history_page_loads_successfully(client):
    response = client.get("/history")

    assert response.status_code == 200
    assert "Histórico de uploads".encode("utf-8") in response.data


def test_upload_creates_history_record(client, app):
    data = {
        "file": (
            BytesIO(b"Categoria,Valor\nA,10\nB,20\nA,30\n"),
            "dados.csv",
        )
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        record = UploadRecord.query.one()

        assert record.file_name == "dados.csv"
        assert record.file_extension == ".csv"
        assert record.row_count == 3
        assert record.column_count == 2