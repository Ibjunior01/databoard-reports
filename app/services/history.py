from app.extensions import db
from app.models import UploadRecord


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


def list_upload_records(limit: int = 50) -> list[UploadRecord]:
    return (
        UploadRecord.query.order_by(
            UploadRecord.created_at.desc(),
            UploadRecord.id.desc(),
        )
        .limit(limit)
        .all()
    )


def get_upload_record(record_id: int):
    return db.session.get(UploadRecord, record_id)
