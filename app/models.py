"""
Modelos persistentes da aplicação DataBoard Reports.
"""

from datetime import datetime, timezone

from app.extensions import db


class UploadRecord(db.Model):
    __tablename__ = "upload_records"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    file_name = db.Column(
        db.String(255),
        nullable=False,
    )

    file_extension = db.Column(
        db.String(20),
        nullable=False,
    )

    file_path = db.Column(
        db.String(500),
        nullable=False,
        default="",
    )

    row_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    column_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    reports = db.relationship(
        "ReportRecord",
        back_populates="upload",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<UploadRecord {self.file_name}>"


class ReportRecord(db.Model):
    __tablename__ = "report_records"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    upload_id = db.Column(
        db.Integer,
        db.ForeignKey("upload_records.id"),
        nullable=False,
        index=True,
    )

    file_name = db.Column(
        db.String(255),
        nullable=False,
    )

    file_path = db.Column(
        db.String(500),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    upload = db.relationship(
        "UploadRecord",
        back_populates="reports",
    )

    def __repr__(self):
        return (
            f"<ReportRecord "
            f"id={self.id} "
            f"upload_id={self.upload_id} "
            f"file_name={self.file_name}>"
        )