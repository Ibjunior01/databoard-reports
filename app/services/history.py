"""
Serviço responsável pela persistência e consulta
dos uploads registrados.
"""

from dataclasses import dataclass
from pathlib import Path

from app.extensions import db
from app.models import UploadRecord


@dataclass(frozen=True)
class UploadDeletionResult:
    """
    Resultado da exclusão completa de um upload.
    """

    upload_file_deleted: bool
    report_files_deleted: int
    report_records_deleted: int
    missing_files: int


def create_upload_record(
    file_name: str,
    file_extension: str,
    row_count: int,
    column_count: int,
    file_path: str = "",
):
    record = UploadRecord(
        file_name=file_name,
        file_extension=file_extension,
        row_count=row_count,
        column_count=column_count,
        file_path=file_path,
    )

    try:
        db.session.add(record)
        db.session.commit()

        return record

    except Exception:
        db.session.rollback()
        raise


def list_upload_records(
    limit: int = 50,
) -> list[UploadRecord]:
    return (
        UploadRecord.query.order_by(
            UploadRecord.created_at.desc(),
            UploadRecord.id.desc(),
        )
        .limit(limit)
        .all()
    )


def get_upload_record(
    record_id: int,
) -> UploadRecord | None:
    return db.session.get(
        UploadRecord,
        record_id,
    )


def _delete_physical_file(
    file_path: str,
) -> bool:
    """
    Remove um arquivo físico quando ele existe.

    Returns:
        True: arquivo encontrado e removido.
        False: caminho vazio ou arquivo inexistente.
    """

    if not file_path:
        return False

    path = Path(file_path)

    if not path.is_file():
        return False

    path.unlink()

    return True


def delete_upload_record(
    upload_record: UploadRecord,
) -> UploadDeletionResult:
    """
    Exclui um upload, seu arquivo original, os PDFs
    relacionados e os respectivos registros do banco.

    Os registros de relatório são removidos pelo
    relacionamento em cascata configurado no modelo.
    """

    related_reports = list(
        upload_record.reports
    )

    upload_file_deleted = False
    report_files_deleted = 0
    missing_files = 0

    try:
        if _delete_physical_file(
            upload_record.file_path
        ):
            upload_file_deleted = True

        elif upload_record.file_path:
            missing_files += 1

        for report in related_reports:
            if _delete_physical_file(
                report.file_path
            ):
                report_files_deleted += 1

            elif report.file_path:
                missing_files += 1

        report_records_deleted = len(
            related_reports
        )

        db.session.delete(
            upload_record
        )
        db.session.commit()

        return UploadDeletionResult(
            upload_file_deleted=(
                upload_file_deleted
            ),
            report_files_deleted=(
                report_files_deleted
            ),
            report_records_deleted=(
                report_records_deleted
            ),
            missing_files=missing_files,
        )

    except Exception:
        db.session.rollback()
        raise