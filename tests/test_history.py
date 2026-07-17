from io import BytesIO

from app.extensions import db
from app.models import ReportRecord, UploadRecord
from app.services.history import (
    create_upload_record,
    delete_upload_record,
    list_upload_records,
)
from app.services.report_history import (
    create_report_record,
)

def test_create_upload_record_persists_data(app):
    with app.app_context():
        record = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=100,
            column_count=5,
            file_path="app/uploads/vendas.csv",
        )

        saved_record = db.session.get(UploadRecord, record.id)

        assert saved_record is not None
        assert saved_record.file_name == "vendas.csv"
        assert saved_record.file_extension == ".csv"
        assert saved_record.row_count == 100
        assert saved_record.column_count == 5
        assert saved_record.file_path == "app/uploads/vendas.csv"


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
        assert record.file_path
        assert record.file_path.endswith("dados.csv")


def test_upload_detail_page_returns_record_data(client, app):
    with app.app_context():
        record = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=100,
            column_count=5,
            file_path="app/uploads/vendas.csv",
        )
        record_id = record.id

    response = client.get(f"/history/{record_id}")

    assert response.status_code == 200
    assert b"vendas.csv" in response.data
    assert b".csv" in response.data
    assert b"100" in response.data
    assert b"5" in response.data
    assert b"app/uploads/vendas.csv" in response.data


def test_upload_detail_page_returns_404_for_missing_record(client):
    response = client.get("/history/999999")

    assert response.status_code == 404


def test_history_page_contains_upload_detail_link(client, app):
    with app.app_context():
        record = create_upload_record(
            file_name="relatorio.xlsx",
            file_extension=".xlsx",
            row_count=50,
            column_count=8,
        )
        record_id = record.id

    response = client.get("/history")

    assert response.status_code == 200
    assert f"/history/{record_id}".encode() in response.data


def test_create_upload_record_saves_file_path(app):
    with app.app_context():
        record = create_upload_record(
            file_name="dados.xlsx",
            file_extension=".xlsx",
            row_count=20,
            column_count=4,
            file_path="app/uploads/dados.xlsx",
        )

        assert record.file_path == "app/uploads/dados.xlsx"


def test_upload_detail_page_contains_reprocess_button(client, app):
    with app.app_context():
        record = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=100,
            column_count=5,
            file_path="app/uploads/vendas.csv",
        )
        record_id = record.id

    response = client.get(f"/history/{record_id}")

    assert response.status_code == 200
    assert "Reprocessar upload".encode("utf-8") in response.data
    assert f"/history/{record_id}/reprocess".encode() in response.data


def test_reprocess_upload_success(client, app, tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text(
        "nome,valor\nProduto A,10\nProduto B,20\n",
        encoding="utf-8",
    )

    with app.app_context():
        record = UploadRecord(
            file_name="sample.csv",
            file_extension=".csv",
            row_count=2,
            column_count=2,
            file_path=str(file_path),
        )

        db.session.add(record)
        db.session.commit()

        record_id = record.id

    response = client.get(f"/history/{record_id}/reprocess")

    assert response.status_code == 200
    assert b"sample.csv" in response.data
    assert b"Produto A" in response.data
    assert b"Produto B" in response.data


def test_reprocess_upload_not_found(client):
    response = client.get("/history/999999/reprocess")

    assert response.status_code == 404


def test_reprocess_upload_missing_physical_file(client, app, tmp_path):
    missing_file_path = tmp_path / "missing-file.csv"

    with app.app_context():
        record = UploadRecord(
            file_name="missing.csv",
            file_extension=".csv",
            row_count=2,
            column_count=2,
            file_path=str(missing_file_path),
        )

        db.session.add(record)
        db.session.commit()

        record_id = record.id

    response = client.get(
        f"/history/{record_id}/reprocess",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert (
        "O arquivo físico deste upload não foi encontrado no servidor.".encode("utf-8")
        in response.data
    )

def test_upload_detail_displays_generate_pdf_button(app, client):
    with app.app_context():
        record = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=100,
            column_count=5,
            file_path="app/uploads/vendas.csv",
        )

        record_id = record.id

    response = client.get(f"/history/{record_id}")

    assert response.status_code == 200
    assert b"Gerar PDF" in response.data
    assert f"/history/{record_id}/report".encode() in response.data


def test_download_upload_report_returns_pdf(
    app,
    client,
    tmp_path,
):
    reports_folder = tmp_path / "reports"
    spreadsheet_path = tmp_path / "vendas.csv"

    app.config["REPORTS_FOLDER"] = reports_folder

    spreadsheet_path.write_text(
        "categoria,valor\n"
        "A,10\n"
        "B,20\n"
        "A,\n",
        encoding="utf-8",
    )

    with app.app_context():
        record = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=3,
            column_count=2,
            file_path=str(spreadsheet_path),
        )

        record_id = record.id

    response = client.get(f"/history/{record_id}/report")

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")

    content_disposition = response.headers.get(
        "Content-Disposition",
        "",
    )

    assert "attachment" in content_disposition
    assert ".pdf" in content_disposition

    generated_reports = list(reports_folder.glob("*.pdf"))

    assert len(generated_reports) == 1
    assert generated_reports[0].is_file()
    assert generated_reports[0].stat().st_size > 0

    with app.app_context():
        report_record = ReportRecord.query.one()

        assert report_record.upload_id == record_id
        assert report_record.file_name == generated_reports[0].name
        assert report_record.file_path == str(
            generated_reports[0]
        )


def test_download_upload_report_missing_physical_file(
    app,
    client,
    tmp_path,
):
    reports_folder = tmp_path / "reports"
    missing_file_path = tmp_path / "arquivo-inexistente.csv"

    app.config["REPORTS_FOLDER"] = reports_folder

    with app.app_context():
        record = create_upload_record(
            file_name="arquivo-inexistente.csv",
            file_extension=".csv",
            row_count=10,
            column_count=3,
            file_path=str(missing_file_path),
        )

        record_id = record.id

    response = client.get(
        f"/history/{record_id}/report",
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert (
        "O arquivo físico deste upload não foi encontrado no servidor.".encode(
            "utf-8"
        )
        in response.data
    )

    generated_reports = list(reports_folder.glob("*.pdf"))

    assert generated_reports == []

def test_upload_detail_displays_persisted_reports(
    app,
    client,
    tmp_path,
):
    report_path = tmp_path / "relatorio_vendas.pdf"
    report_path.write_bytes(b"%PDF-1.4\n")

    with app.app_context():
        upload = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=10,
            column_count=3,
            file_path="app/uploads/vendas.csv",
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=report_path.name,
            file_path=report_path,
        )

        upload_id = upload.id
        report_id = report.id

    response = client.get(
        f"/history/{upload_id}"
    )

    assert response.status_code == 200
    assert b"Relat" in response.data
    assert b"relatorio_vendas.pdf" in response.data
    assert (
        f"/reports/{report_id}/download".encode()
        in response.data
    )


def test_upload_detail_displays_empty_report_state(
    app,
    client,
):
    with app.app_context():
        upload = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=10,
            column_count=3,
        )

        upload_id = upload.id

    response = client.get(
        f"/history/{upload_id}"
    )

    assert response.status_code == 200

    assert (
        "Nenhum relatório PDF foi gerado para este upload.".encode(
            "utf-8"
        )
        in response.data
    )


def test_download_existing_report_returns_pdf(
    app,
    client,
    tmp_path,
):
    report_path = tmp_path / "relatorio_existente.pdf"
    report_path.write_bytes(
        b"%PDF-1.4\narquivo de teste"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=report_path.name,
            file_path=report_path,
        )

        report_id = report.id

    response = client.get(
        f"/reports/{report_id}/download"
    )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")

    content_disposition = response.headers.get(
        "Content-Disposition",
        "",
    )

    assert "attachment" in content_disposition
    assert "relatorio_existente.pdf" in content_disposition


def test_download_existing_report_returns_404(
    client,
):
    response = client.get(
        "/reports/999999/download"
    )

    assert response.status_code == 404


def test_download_existing_report_handles_missing_file(
    app,
    client,
    tmp_path,
):
    missing_report_path = (
        tmp_path
        / "relatorio-inexistente.pdf"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name="relatorio-inexistente.pdf",
            file_path=missing_report_path,
        )

        upload_id = upload.id
        report_id = report.id

    response = client.get(
        f"/reports/{report_id}/download",
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert (
        "O arquivo físico deste relatório não foi encontrado no servidor.".encode(
            "utf-8"
        )
        in response.data
    )

    assert (
        f"Upload #{upload_id}".encode()
        in response.data
    )


def test_upload_detail_contains_report_delete_form(
    app,
    client,
    tmp_path,
):
    report_path = tmp_path / "relatorio.pdf"
    report_path.write_bytes(
        b"%PDF-1.4\n"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=report_path.name,
            file_path=report_path,
        )

        upload_id = upload.id
        report_id = report.id

    response = client.get(
        f"/history/{upload_id}"
    )

    assert response.status_code == 200

    assert (
        f"/reports/{report_id}/delete".encode()
        in response.data
    )

    assert b'name="redirect_to"' in response.data
    assert b'value="upload"' in response.data


def test_delete_report_redirects_to_upload_detail(
    app,
    client,
    tmp_path,
):
    report_path = tmp_path / "relatorio.pdf"
    report_path.write_bytes(
        b"%PDF-1.4\n"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=report_path.name,
            file_path=report_path,
        )

        upload_id = upload.id
        report_id = report.id

    response = client.post(
        f"/reports/{report_id}/delete",
        data={
            "redirect_to": "upload",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert f"Upload #{upload_id}".encode() in response.data

    assert (
        "Nenhum relatório PDF foi gerado para este upload.".encode(
            "utf-8"
        )
        in response.data
    )

    assert not report_path.exists()

    with app.app_context():
        assert (
            db.session.get(
                ReportRecord,
                report_id,
            )
            is None
        )


def test_delete_upload_record_removes_files_and_database_records(
    app,
    tmp_path,
):
    upload_path = tmp_path / "dados.csv"
    first_report_path = tmp_path / "primeiro.pdf"
    second_report_path = tmp_path / "segundo.pdf"

    upload_path.write_text(
        "produto,valor\nA,10\n",
        encoding="utf-8",
    )

    first_report_path.write_bytes(
        b"%PDF-1.4\n"
    )

    second_report_path.write_bytes(
        b"%PDF-1.4\n"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=1,
            column_count=2,
            file_path=str(upload_path),
        )

        first_report = create_report_record(
            upload_id=upload.id,
            file_name=first_report_path.name,
            file_path=first_report_path,
        )

        second_report = create_report_record(
            upload_id=upload.id,
            file_name=second_report_path.name,
            file_path=second_report_path,
        )

        upload_id = upload.id
        first_report_id = first_report.id
        second_report_id = second_report.id

        result = delete_upload_record(
            upload
        )

        assert result.upload_file_deleted is True
        assert result.report_files_deleted == 2
        assert result.report_records_deleted == 2
        assert result.missing_files == 0

        assert (
            db.session.get(
                UploadRecord,
                upload_id,
            )
            is None
        )

        assert (
            db.session.get(
                ReportRecord,
                first_report_id,
            )
            is None
        )

        assert (
            db.session.get(
                ReportRecord,
                second_report_id,
            )
            is None
        )

    assert not upload_path.exists()
    assert not first_report_path.exists()
    assert not second_report_path.exists()


def test_delete_upload_record_handles_missing_physical_files(
    app,
    tmp_path,
):
    missing_upload_path = (
        tmp_path / "upload-inexistente.csv"
    )

    missing_report_path = (
        tmp_path / "relatorio-inexistente.pdf"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="upload-inexistente.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
            file_path=str(missing_upload_path),
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=missing_report_path.name,
            file_path=missing_report_path,
        )

        upload_id = upload.id
        report_id = report.id

        result = delete_upload_record(
            upload
        )

        assert result.upload_file_deleted is False
        assert result.report_files_deleted == 0
        assert result.report_records_deleted == 1
        assert result.missing_files == 2

        assert (
            db.session.get(
                UploadRecord,
                upload_id,
            )
            is None
        )

        assert (
            db.session.get(
                ReportRecord,
                report_id,
            )
            is None
        )


def test_delete_upload_does_not_remove_other_uploads(
    app,
    tmp_path,
):
    first_path = tmp_path / "primeiro.csv"
    second_path = tmp_path / "segundo.csv"

    first_path.write_text(
        "valor\n10\n",
        encoding="utf-8",
    )

    second_path.write_text(
        "valor\n20\n",
        encoding="utf-8",
    )

    with app.app_context():
        first_upload = create_upload_record(
            file_name="primeiro.csv",
            file_extension=".csv",
            row_count=1,
            column_count=1,
            file_path=str(first_path),
        )

        second_upload = create_upload_record(
            file_name="segundo.csv",
            file_extension=".csv",
            row_count=1,
            column_count=1,
            file_path=str(second_path),
        )

        first_id = first_upload.id
        second_id = second_upload.id

        delete_upload_record(
            first_upload
        )

        assert (
            db.session.get(
                UploadRecord,
                first_id,
            )
            is None
        )

        remaining_upload = db.session.get(
            UploadRecord,
            second_id,
        )

        assert remaining_upload is not None
        assert remaining_upload.file_name == "segundo.csv"

    assert not first_path.exists()
    assert second_path.exists()


def test_upload_detail_contains_delete_upload_form(
    app,
    client,
):
    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        upload_id = upload.id

    response = client.get(
        f"/history/{upload_id}"
    )

    assert response.status_code == 200

    assert (
        f"/history/{upload_id}/delete".encode()
        in response.data
    )

    assert b'method="post"' in response.data
    assert b"Excluir upload" in response.data


def test_history_page_contains_delete_upload_form(
    app,
    client,
):
    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        upload_id = upload.id

    response = client.get(
        "/history"
    )

    assert response.status_code == 200

    assert (
        f"/history/{upload_id}/delete".encode()
        in response.data
    )

    assert b'method="post"' in response.data
    assert b"Excluir" in response.data


def test_delete_upload_route_removes_upload_and_related_files(
    app,
    client,
    tmp_path,
):
    upload_path = tmp_path / "dados.csv"
    report_path = tmp_path / "relatorio.pdf"

    upload_path.write_text(
        "produto,valor\nA,10\n",
        encoding="utf-8",
    )

    report_path.write_bytes(
        b"%PDF-1.4\n"
    )

    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=1,
            column_count=2,
            file_path=str(upload_path),
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=report_path.name,
            file_path=report_path,
        )

        upload_id = upload.id
        report_id = report.id

    response = client.post(
        f"/history/{upload_id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert (
        "Upload e arquivos associados excluídos com sucesso.".encode(
            "utf-8"
        )
        in response.data
    )

    assert not upload_path.exists()
    assert not report_path.exists()

    with app.app_context():
        assert (
            db.session.get(
                UploadRecord,
                upload_id,
            )
            is None
        )

        assert (
            db.session.get(
                ReportRecord,
                report_id,
            )
            is None
        )


def test_delete_upload_route_returns_404_for_missing_record(
    client,
):
    response = client.post(
        "/history/999999/delete"
    )

    assert response.status_code == 404