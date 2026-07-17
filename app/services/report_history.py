"""
Serviço responsável pela persistência e consulta
dos relatórios PDF gerados.
"""

from pathlib import Path

from app.extensions import db
from app.models import ReportRecord


def create_report_record(
    upload_id: int,
    file_name: str,
    file_path: str | Path,
) -> ReportRecord:
    """
    Registra no banco um relatório PDF gerado.
    """

    record = ReportRecord(
        upload_id=upload_id,
        file_name=file_name,
        file_path=str(file_path),
    )

    try:
        db.session.add(record)
        db.session.commit()

        return record

    except Exception:
        db.session.rollback()
        raise


def list_report_records_by_upload(
    upload_id: int,
    limit: int = 50,
) -> list[ReportRecord]:
    """
    Lista os relatórios relacionados a um upload,
    do mais recente para o mais antigo.
    """

    return (
        ReportRecord.query
        .filter_by(upload_id=upload_id)
        .order_by(
            ReportRecord.created_at.desc(),
            ReportRecord.id.desc(),
        )
        .limit(limit)
        .all()
    )


def get_report_record(
    report_id: int,
) -> ReportRecord | None:
    """
    Busca um relatório persistido pelo seu ID.
    """

    return db.session.get(
        ReportRecord,
        report_id,
    )