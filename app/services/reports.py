"""
Serviço de geração de relatórios.

Futuras responsabilidades:
- Gerar relatórios em PDF com ReportLab.
- Exportar análises consolidadas.
- Criar arquivos dentro da pasta app/reports.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from werkzeug.utils import secure_filename
from xml.sax.saxutils import escape


def _format_datetime(value: datetime | None) -> str:
    """
    Formata valores de data e hora para exibição no relatório.
    """

    if value is None:
        return "Não informado"

    return value.strftime("%d/%m/%Y às %H:%M:%S")


def _build_report_filename(upload_record: Any) -> str:
    """
    Cria um nome seguro e único para o arquivo PDF.
    """

    original_name = Path(upload_record.file_name).stem
    safe_name = secure_filename(original_name) or "upload"

    generated_at = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"relatorio_{upload_record.id}_{safe_name}_{generated_at}.pdf"


def generate_upload_report(
    upload_record: Any,
    reports_folder: str | Path,
) -> Path:
    """
    Gera um relatório PDF simples com os metadados de um upload.

    Args:
        upload_record:
            Registro de upload contendo id, file_name, file_extension,
            row_count, column_count e created_at.

        reports_folder:
            Diretório em que o relatório será salvo.

    Returns:
        Caminho completo do PDF gerado.
    """

    reports_path = Path(reports_folder)
    reports_path.mkdir(parents=True, exist_ok=True)

    report_filename = _build_report_filename(upload_record)
    report_path = reports_path / report_filename

    document = SimpleDocTemplate(
        str(report_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Relatório de Upload - DataBoard Reports",
        author="DataBoard Reports",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="DataBoardTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        name="DataBoardSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=20,
    )

    cell_value_style = ParagraphStyle(
    name="CellValue",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=12,
    textColor=colors.HexColor("#1e293b"),
    wordWrap="CJK",
)

    elements = [
        Paragraph("DataBoard Reports", title_style),
        Paragraph(
            "Relatório básico de processamento de planilha",
            subtitle_style,
        ),
        Spacer(1, 0.4 * cm),
    ]

    report_data = [
        ["Informação", "Valor"],
        ["ID do upload", str(upload_record.id)],
        [
            "Nome do arquivo",
            Paragraph(
                escape(str(upload_record.file_name)),
                cell_value_style,
            ),
        ],
        ["Extensão", str(upload_record.file_extension)],
        ["Quantidade de linhas", str(upload_record.row_count)],
        ["Quantidade de colunas", str(upload_record.column_count)],
        [
            "Data do upload",
            _format_datetime(upload_record.created_at),
        ],
        [
            "Data de geração",
            _format_datetime(datetime.now()),
        ],
    ]

    report_table = Table(
        report_data,
        colWidths=[5.5 * cm, 10 * cm],
        repeatRows=1,
    )

    report_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0f172a"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (0, -1),
                    colors.HexColor("#e2e8f0"),
                ),
                (
                    "BACKGROUND",
                    (1, 1),
                    (1, -1),
                    colors.HexColor("#f8fafc"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#1e293b"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#94a3b8"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )

    elements.append(report_table)

    document.build(elements)

    return report_path