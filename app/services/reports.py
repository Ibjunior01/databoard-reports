"""
Serviço responsável pela geração de relatórios PDF do DataBoard Reports.

Responsabilidades:
- Gerar relatórios em PDF com ReportLab.
- Exibir metadados do upload.
- Exibir o resumo da análise automática da planilha.
- Criar os arquivos dentro da pasta configurada de relatórios.
"""

from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

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


def _format_datetime(value: datetime | None) -> str:
    """
    Formata valores de data e hora para exibição no relatório.
    """

    if value is None:
        return "Não informado"

    return value.strftime("%d/%m/%Y às %H:%M:%S")


def _analysis_to_dict(analysis_result: Any) -> dict[str, Any]:
    """
    Converte o resultado da análise para dicionário.

    Aceita:
    - instâncias de DataAnalysisResult;
    - outras dataclasses;
    - dicionários;
    - objetos com atributos públicos.
    """

    if hasattr(analysis_result, "to_dict"):
        return analysis_result.to_dict()

    if is_dataclass(analysis_result):
        return asdict(analysis_result)

    if isinstance(analysis_result, dict):
        return analysis_result

    return vars(analysis_result)


def _build_report_filename(
    upload_record: Any,
    generated_at: datetime,
) -> str:
    """
    Cria um nome seguro e único para o arquivo PDF.
    """

    original_name = Path(upload_record.file_name).stem
    safe_name = secure_filename(original_name) or "upload"

    timestamp = generated_at.strftime("%Y%m%d_%H%M%S")

    return f"relatorio_{upload_record.id}_{safe_name}_{timestamp}.pdf"


def _build_analysis_summary(
    analysis_result: Any,
) -> dict[str, Any]:
    """
    Organiza os dados da análise automática para uso no relatório.
    """

    analysis_data = _analysis_to_dict(analysis_result)

    numeric_columns = [
        str(column)
        for column in analysis_data.get("numeric_columns", [])
    ]

    categorical_columns = [
        str(column)
        for column in analysis_data.get("categorical_columns", [])
    ]

    missing_values_count = (
        analysis_data.get("missing_values_count", {}) or {}
    )

    missing_values_percent = (
        analysis_data.get("missing_values_percent", {}) or {}
    )

    missing_columns = []

    for column, missing_count in missing_values_count.items():
        normalized_count = int(missing_count)

        if normalized_count <= 0:
            continue

        column_name = str(column)

        missing_columns.append(
            {
                "column": column_name,
                "count": normalized_count,
                "percent": float(
                    missing_values_percent.get(
                        column,
                        missing_values_percent.get(column_name, 0),
                    )
                ),
            }
        )

    return {
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "numeric_columns_count": len(numeric_columns),
        "categorical_columns_count": len(categorical_columns),
        "total_missing_values": sum(
            int(value)
            for value in missing_values_count.values()
        ),
        "missing_columns": missing_columns,
    }


def _format_column_list(
    columns: list[str],
    paragraph_style: ParagraphStyle,
) -> Paragraph:
    """
    Formata uma lista de colunas para exibição no PDF.
    """

    if not columns:
        return Paragraph("Nenhuma", paragraph_style)

    formatted_columns = ", ".join(columns)

    return Paragraph(
        escape(formatted_columns),
        paragraph_style,
    )


def _apply_information_table_style(table: Table) -> None:
    """
    Aplica o estilo padrão das tabelas de informações do relatório.
    """

    table.setStyle(
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


def generate_upload_report(
    upload_record: Any,
    analysis_result: Any,
    reports_folder: str | Path,
) -> Path:
    """
    Gera um relatório PDF com os metadados do upload e o resumo
    da análise automática da planilha.

    Args:
        upload_record:
            Registro contendo id, file_name, file_extension,
            row_count, column_count e created_at.

        analysis_result:
            Resultado retornado pela função analyze_dataframe().

        reports_folder:
            Diretório em que o relatório será salvo.

    Returns:
        Caminho completo do PDF gerado.
    """

    reports_path = Path(reports_folder)
    reports_path.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now()

    report_filename = _build_report_filename(
        upload_record=upload_record,
        generated_at=generated_at,
    )

    report_path = reports_path / report_filename

    analysis_summary = _build_analysis_summary(analysis_result)

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

    section_title_style = ParagraphStyle(
        name="DataBoardSectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=10,
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

    note_style = ParagraphStyle(
        name="DataBoardNote",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569"),
        spaceAfter=6,
    )

    elements = [
        Paragraph("DataBoard Reports", title_style),
        Paragraph(
            "Relatório de processamento e análise automática de planilha",
            subtitle_style,
        ),
        Spacer(1, 0.2 * cm),
        Paragraph("Informações do upload", section_title_style),
    ]

    upload_data = [
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
            _format_datetime(generated_at),
        ],
    ]

    upload_table = Table(
        upload_data,
        colWidths=[5.5 * cm, 10 * cm],
        repeatRows=1,
    )

    _apply_information_table_style(upload_table)

    elements.extend(
        [
            upload_table,
            Spacer(1, 0.7 * cm),
            Paragraph(
                "Resumo da análise automática",
                section_title_style,
            ),
        ]
    )

    analysis_data = [
        ["Indicador", "Resultado"],
        [
            "Colunas numéricas",
            str(analysis_summary["numeric_columns_count"]),
        ],
        [
            "Colunas categóricas/texto",
            str(analysis_summary["categorical_columns_count"]),
        ],
        [
            "Total de valores ausentes",
            str(analysis_summary["total_missing_values"]),
        ],
        [
            "Nomes das colunas numéricas",
            _format_column_list(
                analysis_summary["numeric_columns"],
                cell_value_style,
            ),
        ],
        [
            "Nomes das colunas categóricas/texto",
            _format_column_list(
                analysis_summary["categorical_columns"],
                cell_value_style,
            ),
        ],
    ]

    analysis_table = Table(
        analysis_data,
        colWidths=[5.5 * cm, 10 * cm],
        repeatRows=1,
    )

    _apply_information_table_style(analysis_table)

    elements.extend(
        [
            analysis_table,
            Spacer(1, 0.7 * cm),
            Paragraph(
                "Valores ausentes por coluna",
                section_title_style,
            ),
        ]
    )

    missing_columns = analysis_summary["missing_columns"]

    if not missing_columns:
        elements.append(
            Paragraph(
                "Nenhum valor ausente foi identificado na planilha.",
                note_style,
            )
        )
    else:
        missing_data = [
            [
                "Coluna",
                "Valores ausentes",
                "Percentual",
            ]
        ]

        for item in missing_columns:
            missing_data.append(
                [
                    Paragraph(
                        escape(item["column"]),
                        cell_value_style,
                    ),
                    str(item["count"]),
                    f'{item["percent"]:.2f}%',
                ]
            )

        missing_table = Table(
            missing_data,
            colWidths=[7 * cm, 4.2 * cm, 4.3 * cm],
            repeatRows=1,
        )

        missing_table.setStyle(
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
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
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
                        "ALIGN",
                        (1, 1),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ]
            )
        )

        elements.append(missing_table)

    document.build(elements)

    return report_path