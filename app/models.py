"""
Modelos da aplicação.

Nesta primeira entrega, o banco de dados ainda não será implementado.
Este arquivo foi criado para manter a arquitetura preparada para a
futura integração com SQLite e SQLAlchemy.
"""

from datetime import datetime, timezone

from app.extensions import db


class UploadRecord(db.Model):
    __tablename__ = "upload_records"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_extension = db.Column(db.String(20), nullable=False)
    file_path = db.Column(db.String(500), nullable=False, default="")
    row_count = db.Column(db.Integer, nullable=False, default=0)
    column_count = db.Column(db.Integer, nullable=False, default=0)
    
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<UploadRecord {self.file_name}>"