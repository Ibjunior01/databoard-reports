from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from app.services.reports import generate_upload_report


def test_generate_upload_report_creates_pdf(tmp_path):
    upload_record = SimpleNamespace(
        id=1,
        file_name="vendas.csv",
        file_extension=".csv",
        row_count=100,
        column_count=5,
        created_at=datetime(2026, 7, 13, 10, 30, 0),
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        reports_folder=tmp_path,
    )

    assert isinstance(report_path, Path)
    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.suffix == ".pdf"
    assert report_path.stat().st_size > 0


def test_generate_upload_report_creates_valid_pdf_header(tmp_path):
    upload_record = SimpleNamespace(
        id=2,
        file_name="relatorio financeiro.xlsx",
        file_extension=".xlsx",
        row_count=250,
        column_count=12,
        created_at=datetime(2026, 7, 13, 11, 0, 0),
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        reports_folder=tmp_path,
    )

    with report_path.open("rb") as pdf_file:
        pdf_header = pdf_file.read(4)

    assert pdf_header == b"%PDF"


def test_generate_upload_report_creates_reports_directory(tmp_path):
    reports_folder = tmp_path / "generated_reports"

    upload_record = SimpleNamespace(
        id=3,
        file_name="clientes.xls",
        file_extension=".xls",
        row_count=50,
        column_count=8,
        created_at=None,
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        reports_folder=reports_folder,
    )

    assert reports_folder.exists()
    assert report_path.exists()