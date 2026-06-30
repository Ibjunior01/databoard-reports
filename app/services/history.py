from app.extensions import db
from app.models import UploadRecord


def create_upload_record(
    *,
    file_name: str,
    file_extension: str,
    row_count: int,
    column_count: int,
) -> UploadRecord:
    record = UploadRecord(
        file_name=file_name,
        file_extension=file_extension,
        row_count=row_count,
        column_count=column_count,
    )

    try:
        db.session.add(record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return record


def list_upload_records(limit: int = 50) -> list[UploadRecord]:
    return (
        UploadRecord.query.order_by(
            UploadRecord.created_at.desc(),
            UploadRecord.id.desc(),
        )
        .limit(limit)
        .all()
    )