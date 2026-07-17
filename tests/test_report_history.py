from app.extensions import db
from app.models import ReportRecord
from app.services.history import create_upload_record
from app.services.report_history import (
    create_report_record,
    get_report_record,
    list_report_records,
    list_report_records_by_upload,
)


def test_create_report_record_persists_data(
    app,
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

        saved_report = db.session.get(
            ReportRecord,
            report.id,
        )

        assert saved_report is not None
        assert saved_report.upload_id == upload.id
        assert saved_report.file_name == "relatorio_vendas.pdf"
        assert saved_report.file_path == str(report_path)
        assert saved_report.created_at is not None


def test_report_record_has_upload_relationship(
    app,
    tmp_path,
):
    report_path = tmp_path / "relatorio.pdf"
    report_path.write_bytes(b"%PDF-1.4\n")

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

        assert report.upload.id == upload.id
        assert report.upload.file_name == "dados.csv"

        assert len(upload.reports) == 1
        assert upload.reports[0].id == report.id


def test_list_report_records_by_upload_returns_newest_first(
    app,
):
    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        other_upload = create_upload_record(
            file_name="outro.csv",
            file_extension=".csv",
            row_count=3,
            column_count=2,
        )

        first_report = create_report_record(
            upload_id=upload.id,
            file_name="primeiro.pdf",
            file_path="reports/primeiro.pdf",
        )

        second_report = create_report_record(
            upload_id=upload.id,
            file_name="segundo.pdf",
            file_path="reports/segundo.pdf",
        )

        create_report_record(
            upload_id=other_upload.id,
            file_name="outro.pdf",
            file_path="reports/outro.pdf",
        )

        reports = list_report_records_by_upload(
            upload_id=upload.id,
        )

        assert len(reports) == 2
        assert reports[0].id == second_report.id
        assert reports[1].id == first_report.id

        assert all(
            report.upload_id == upload.id
            for report in reports
        )


def test_get_report_record_returns_record_and_none(
    app,
):
    with app.app_context():
        upload = create_upload_record(
            file_name="dados.csv",
            file_extension=".csv",
            row_count=5,
            column_count=2,
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name="relatorio.pdf",
            file_path="reports/relatorio.pdf",
        )

        saved_report = get_report_record(
            report.id
        )

        missing_report = get_report_record(
            999999
        )

        assert saved_report is not None
        assert saved_report.id == report.id
        assert missing_report is None


def test_list_report_records_returns_all_reports_newest_first(
    app,
):
    with app.app_context():
        first_upload = create_upload_record(
            file_name="vendas.csv",
            file_extension=".csv",
            row_count=10,
            column_count=3,
        )

        second_upload = create_upload_record(
            file_name="clientes.xlsx",
            file_extension=".xlsx",
            row_count=20,
            column_count=5,
        )

        first_report = create_report_record(
            upload_id=first_upload.id,
            file_name="primeiro.pdf",
            file_path="reports/primeiro.pdf",
        )

        second_report = create_report_record(
            upload_id=second_upload.id,
            file_name="segundo.pdf",
            file_path="reports/segundo.pdf",
        )

        reports = list_report_records()

        assert len(reports) == 2
        assert reports[0].id == second_report.id
        assert reports[1].id == first_report.id

        assert (
            reports[0].upload.file_name
            == "clientes.xlsx"
        )

        assert (
            reports[1].upload.file_name
            == "vendas.csv"
        )


def test_reports_history_page_loads_successfully(
    client,
):
    response = client.get("/reports")

    assert response.status_code == 200

    assert (
        "Histórico de relatórios".encode(
            "utf-8"
        )
        in response.data
    )


def test_reports_history_page_displays_reports_and_links(
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
        )

        report = create_report_record(
            upload_id=upload.id,
            file_name=report_path.name,
            file_path=report_path,
        )

        upload_id = upload.id
        report_id = report.id

    response = client.get("/reports")

    assert response.status_code == 200
    assert b"relatorio_vendas.pdf" in response.data
    assert b"vendas.csv" in response.data

    assert (
        f"/history/{upload_id}".encode()
        in response.data
    )

    assert (
        f"/reports/{report_id}/download".encode()
        in response.data
    )


def test_reports_history_page_displays_empty_state(
    client,
):
    response = client.get("/reports")

    assert response.status_code == 200

    assert (
        "Nenhum relatório gerado".encode(
            "utf-8"
        )
        in response.data
    )


def test_navigation_contains_reports_link(
    client,
):
    response = client.get("/")

    assert response.status_code == 200
    assert b'href="/reports"' in response.data

    assert (
        "Relatórios".encode("utf-8")
        in response.data
    )