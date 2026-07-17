"""
Serviço responsável pela geração de relatórios PDF do DataBoard Reports.

Responsabilidades:
- Gerar relatórios em PDF com ReportLab.
- Exibir metadados do upload.
- Exibir o resumo da análise automática da planilha.
- Exibir estatísticas básicas das colunas numéricas.
- Inserir gráficos estáticos no relatório.
- Criar os arquivos dentro da pasta configurada de relatórios.
"""

from dataclasses import asdict, is_dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

import pandas as pd
from werkzeug.utils import secure_filename


REPORT_CHART_WIDTH = 15.5 * cm
REPORT_CHART_HEIGHT = REPORT_CHART_WIDTH * (675 / 1200)
PREVIEW_MAX_ROWS = 5
PREVIEW_MAX_COLUMNS = 6
PREVIEW_CELL_MAX_LENGTH = 40


def _format_datetime(value: datetime | None) -> str:
    """
    Formata valores de data e hora para exibição no relatório.
    """

    if value is None:
        return "Não informado"

    return value.strftime("%d/%m/%Y às %H:%M:%S")


def _format_number(value: float | int | None) -> str:
    """
    Formata valores numéricos para exibição no relatório.

    Valores ausentes são representados por "Não disponível".
    """

    if value is None:
        return "Não disponível"

    number = float(value)

    if number.is_integer():
        return f"{int(number):,}".replace(",", ".")

    formatted = f"{number:,.2f}"

    return (
        formatted
        .replace(",", "TEMP")
        .replace(".", ",")
        .replace("TEMP", ".")
    )


def _analysis_to_dict(
    analysis_result: Any,
) -> dict[str, Any]:
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

    return (
        f"relatorio_"
        f"{upload_record.id}_"
        f"{safe_name}_"
        f"{timestamp}.pdf"
    )


def _build_analysis_summary(
    analysis_result: Any,
) -> dict[str, Any]:
    """
    Organiza os dados da análise automática para uso no relatório.
    """

    analysis_data = _analysis_to_dict(analysis_result)

    numeric_columns = [
        str(column)
        for column in analysis_data.get(
            "numeric_columns",
            [],
        )
    ]

    categorical_columns = [
        str(column)
        for column in analysis_data.get(
            "categorical_columns",
            [],
        )
    ]

    missing_values_count = (
        analysis_data.get(
            "missing_values_count",
            {},
        )
        or {}
    )

    missing_values_percent = (
        analysis_data.get(
            "missing_values_percent",
            {},
        )
        or {}
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
                        missing_values_percent.get(
                            column_name,
                            0,
                        ),
                    )
                ),
            }
        )

    return {
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "numeric_columns_count": len(
            numeric_columns
        ),
        "categorical_columns_count": len(
            categorical_columns
        ),
        "total_missing_values": sum(
            int(value)
            for value in missing_values_count.values()
        ),
        "missing_columns": missing_columns,
    }


def _build_numeric_statistics(
    analysis_result: Any,
) -> list[dict[str, str]]:
    """
    Organiza e formata as estatísticas das colunas numéricas
    para uso no relatório PDF.
    """

    analysis_data = _analysis_to_dict(
        analysis_result
    )

    numeric_statistics = (
        analysis_data.get(
            "numeric_statistics",
            {},
        )
        or {}
    )

    formatted_statistics = []

    for column, statistics in numeric_statistics.items():
        formatted_statistics.append(
            {
                "column": str(column),
                "mean": _format_number(
                    statistics.get("mean")
                ),
                "median": _format_number(
                    statistics.get("median")
                ),
                "min": _format_number(
                    statistics.get("min")
                ),
                "max": _format_number(
                    statistics.get("max")
                ),
            }
        )

    return formatted_statistics


def _format_column_list(
    columns: list[str],
    paragraph_style: ParagraphStyle,
) -> Paragraph:
    """
    Formata uma lista de colunas para exibição no PDF.
    """

    if not columns:
        return Paragraph(
            "Nenhuma",
            paragraph_style,
        )

    formatted_columns = ", ".join(columns)

    return Paragraph(
        escape(formatted_columns),
        paragraph_style,
    )

def _format_preview_value(
    value: Any,
    max_length: int = PREVIEW_CELL_MAX_LENGTH,
) -> str:
    """
    Formata um valor da planilha para exibição na prévia do PDF.

    Valores ausentes são exibidos como "-".
    Textos muito longos são truncados para preservar a legibilidade.
    """

    if pd.isna(value):
        return "-"

    text = str(value)

    if len(text) <= max_length:
        return text

    return f"{text[: max_length - 3]}..."


def _build_dataframe_preview(
    dataframe: pd.DataFrame,
    max_rows: int = PREVIEW_MAX_ROWS,
    max_columns: int = PREVIEW_MAX_COLUMNS,
) -> dict[str, Any]:
    """
    Prepara uma prévia limitada do DataFrame para exibição no PDF.

    A função limita a quantidade de linhas e colunas para preservar
    a legibilidade do relatório em formato A4.
    """

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(
            "O objeto informado deve ser um pandas.DataFrame."
        )

    if max_rows < 0:
        raise ValueError(
            "max_rows deve ser maior ou igual a zero."
        )

    if max_columns < 0:
        raise ValueError(
            "max_columns deve ser maior ou igual a zero."
        )

    total_rows = len(dataframe)
    total_columns = len(dataframe.columns)

    preview_dataframe = dataframe.iloc[
        :max_rows,
        :max_columns,
    ].copy()

    columns = [
        str(column)
        for column in preview_dataframe.columns
    ]

    rows = [
        [
            _format_preview_value(value)
            for value in row
        ]
        for row in preview_dataframe.itertuples(
            index=False,
            name=None,
        )
    ]

    return {
        "columns": columns,
        "rows": rows,
        "total_rows": total_rows,
        "total_columns": total_columns,
        "displayed_rows": len(rows),
        "displayed_columns": len(columns),
        "omitted_rows": max(
            total_rows - len(rows),
            0,
        ),
        "omitted_columns": max(
            total_columns - len(columns),
            0,
        ),
    }


def _apply_information_table_style(
    table: Table,
) -> None:
    """
    Aplica o estilo padrão das tabelas de informações
    do relatório.
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


def _apply_data_table_style(
    table: Table,
) -> None:
    """
    Aplica o estilo padrão das tabelas de dados
    do relatório.
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


def _build_chart_elements(
    chart_results: list[Any],
    chart_title_style: ParagraphStyle,
) -> list[Any]:
    """
    Converte os gráficos estáticos em elementos
    compatíveis com o ReportLab.

    As imagens são lidas diretamente da memória,
    sem criação de arquivos PNG temporários.
    """

    chart_elements = []

    for chart in chart_results:
        image_stream = BytesIO(
            chart.image_bytes
        )

        chart_image = Image(
            image_stream,
            width=REPORT_CHART_WIDTH,
            height=REPORT_CHART_HEIGHT,
        )

        chart_block = KeepTogether(
            [
                Paragraph(
                    escape(str(chart.title)),
                    chart_title_style,
                ),
                Spacer(1, 0.2 * cm),
                chart_image,
            ]
        )

        chart_elements.append(
            chart_block
        )

        chart_elements.append(
            Spacer(1, 0.6 * cm)
        )

    return chart_elements


def generate_upload_report(
    upload_record: Any,
    analysis_result: Any,
    reports_folder: str | Path,
    chart_results: list[Any] | None = None,
    dataframe: pd.DataFrame | None = None,
) -> Path:
    """
    Gera um relatório PDF com:
    - metadados do upload;
    - resumo da análise automática;
    - estatísticas das colunas numéricas;
    - gráficos estáticos disponíveis.

    Args:
        upload_record:
            Registro contendo id, file_name,
            file_extension, row_count,
            column_count e created_at.

        analysis_result:
            Resultado retornado pela função
            analyze_dataframe().

        reports_folder:
            Diretório em que o relatório será salvo.

        chart_results:
            Lista opcional de gráficos estáticos
            contendo título e image_bytes.

        dataframe:
            DataFrame opcional utilizado para gerar uma prévia
            limitada das primeiras linhas e colunas da planilha.

    Returns:
        Caminho completo do PDF gerado.
    """

    reports_path = Path(reports_folder)

    reports_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_at = datetime.now()

    report_filename = _build_report_filename(
        upload_record=upload_record,
        generated_at=generated_at,
    )

    report_path = (
        reports_path
        / report_filename
    )

    analysis_summary = (
        _build_analysis_summary(
            analysis_result
        )
    )

    numeric_statistics = (
        _build_numeric_statistics(
            analysis_result
        )
    )

    chart_results = chart_results or []

    dataframe_preview = None

    if dataframe is not None:
        dataframe_preview = _build_dataframe_preview(
            dataframe
        )

    document = SimpleDocTemplate(
        str(report_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=(
            "Relatório de Upload - "
            "DataBoard Reports"
        ),
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
        textColor=colors.HexColor(
            "#0f172a"
        ),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        name="DataBoardSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor(
            "#475569"
        ),
        spaceAfter=20,
    )

    section_title_style = ParagraphStyle(
        name="DataBoardSectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor(
            "#0f172a"
        ),
        spaceBefore=8,
        spaceAfter=10,
    )

    chart_title_style = ParagraphStyle(
        name="DataBoardChartTitle",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor(
            "#1e293b"
        ),
        spaceAfter=4,
    )

    cell_value_style = ParagraphStyle(
        name="CellValue",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor(
            "#1e293b"
        ),
        wordWrap="CJK",
    )

    note_style = ParagraphStyle(
        name="DataBoardNote",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor(
            "#475569"
        ),
        spaceAfter=6,
    )

    elements = [
        Paragraph(
            "DataBoard Reports",
            title_style,
        ),
        Paragraph(
            (
                "Relatório de processamento e "
                "análise automática de planilha"
            ),
            subtitle_style,
        ),
        Spacer(
            1,
            0.2 * cm,
        ),
        Paragraph(
            "Informações do upload",
            section_title_style,
        ),
    ]

    upload_data = [
        [
            "Informação",
            "Valor",
        ],
        [
            "ID do upload",
            str(upload_record.id),
        ],
        [
            "Nome do arquivo",
            Paragraph(
                escape(
                    str(
                        upload_record.file_name
                    )
                ),
                cell_value_style,
            ),
        ],
        [
            "Extensão",
            str(
                upload_record.file_extension
            ),
        ],
        [
            "Quantidade de linhas",
            str(
                upload_record.row_count
            ),
        ],
        [
            "Quantidade de colunas",
            str(
                upload_record.column_count
            ),
        ],
        [
            "Data do upload",
            _format_datetime(
                upload_record.created_at
            ),
        ],
        [
            "Data de geração",
            _format_datetime(
                generated_at
            ),
        ],
    ]

    upload_table = Table(
        upload_data,
        colWidths=[
            5.5 * cm,
            10 * cm,
        ],
        repeatRows=1,
    )

    _apply_information_table_style(
        upload_table
    )

    elements.extend(
        [
            upload_table,
            Spacer(
                1,
                0.7 * cm,
            ),
            Paragraph(
                "Resumo da análise automática",
                section_title_style,
            ),
        ]
    )

    analysis_data = [
        [
            "Indicador",
            "Resultado",
        ],
        [
            "Colunas numéricas",
            str(
                analysis_summary[
                    "numeric_columns_count"
                ]
            ),
        ],
        [
            "Colunas categóricas/texto",
            str(
                analysis_summary[
                    "categorical_columns_count"
                ]
            ),
        ],
        [
            "Total de valores ausentes",
            str(
                analysis_summary[
                    "total_missing_values"
                ]
            ),
        ],
        [
            "Nomes das colunas numéricas",
            _format_column_list(
                analysis_summary[
                    "numeric_columns"
                ],
                cell_value_style,
            ),
        ],
        [
            (
                "Nomes das colunas "
                "categóricas/texto"
            ),
            _format_column_list(
                analysis_summary[
                    "categorical_columns"
                ],
                cell_value_style,
            ),
        ],
    ]

    analysis_table = Table(
        analysis_data,
        colWidths=[
            5.5 * cm,
            10 * cm,
        ],
        repeatRows=1,
    )

    _apply_information_table_style(
        analysis_table
    )

    elements.extend(
        [
            analysis_table,
            Spacer(
                1,
                0.7 * cm,
            ),
            Paragraph(
                "Valores ausentes por coluna",
                section_title_style,
            ),
        ]
    )

    missing_columns = (
        analysis_summary[
            "missing_columns"
        ]
    )

    if not missing_columns:
        elements.append(
            Paragraph(
                (
                    "Nenhum valor ausente foi "
                    "identificado na planilha."
                ),
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
                        escape(
                            item["column"]
                        ),
                        cell_value_style,
                    ),
                    str(
                        item["count"]
                    ),
                    (
                        f'{item["percent"]:.2f}%'
                    ),
                ]
            )

        missing_table = Table(
            missing_data,
            colWidths=[
                7 * cm,
                4.2 * cm,
                4.3 * cm,
            ],
            repeatRows=1,
        )

        _apply_data_table_style(
            missing_table
        )

        elements.append(
            missing_table
        )

    elements.extend(
        [
            Spacer(
                1,
                0.7 * cm,
            ),
            Paragraph(
                (
                    "Estatísticas das "
                    "colunas numéricas"
                ),
                section_title_style,
            ),
        ]
    )

    if not numeric_statistics:
        elements.append(
            Paragraph(
                (
                    "Nenhuma coluna numérica "
                    "foi identificada na planilha."
                ),
                note_style,
            )
        )

    else:
        statistics_data = [
            [
                "Coluna",
                "Média",
                "Mediana",
                "Mínimo",
                "Máximo",
            ]
        ]

        for item in numeric_statistics:
            statistics_data.append(
                [
                    Paragraph(
                        escape(
                            item["column"]
                        ),
                        cell_value_style,
                    ),
                    item["mean"],
                    item["median"],
                    item["min"],
                    item["max"],
                ]
            )

        statistics_table = Table(
            statistics_data,
            colWidths=[
                5.1 * cm,
                2.6 * cm,
                2.6 * cm,
                2.6 * cm,
                2.6 * cm,
            ],
            repeatRows=1,
        )

        _apply_data_table_style(
            statistics_table
        )

        elements.append(
            statistics_table
        )

    elements.extend(
        [
            Spacer(
                1,
                0.8 * cm,
            ),
            Paragraph(
                "Prévia dos dados",
                section_title_style,
            ),
        ]
    )

    if dataframe_preview is None:
        elements.append(
            Paragraph(
                (
                    "Nenhuma prévia de dados foi "
                    "disponibilizada para este relatório."
                ),
                note_style,
            )
        )

    elif not dataframe_preview["columns"]:
        elements.append(
            Paragraph(
                (
                    "A planilha não possui colunas "
                    "disponíveis para exibição."
                ),
                note_style,
            )
        )

    elif not dataframe_preview["rows"]:
        elements.append(
            Paragraph(
                (
                    "A planilha possui colunas, mas "
                    "não contém linhas de dados."
                ),
                note_style,
            )
        )

    else:
        preview_table_data = [
            [
                Paragraph(
                    escape(column),
                    cell_value_style,
                )
                for column in dataframe_preview[
                    "columns"
                ]
            ]
        ]

        for row in dataframe_preview["rows"]:
            preview_table_data.append(
                [
                    Paragraph(
                        escape(value),
                        cell_value_style,
                    )
                    for value in row
                ]
            )

        available_width = 15.5 * cm

        column_width = (
            available_width
            / dataframe_preview[
                "displayed_columns"
            ]
        )

        preview_table = Table(
            preview_table_data,
            colWidths=[
                column_width
                for _ in dataframe_preview[
                    "columns"
                ]
            ],
            repeatRows=1,
        )

        _apply_data_table_style(
            preview_table
        )

        elements.append(
            preview_table
        )

        preview_note_parts = [
            (
                f'Exibindo '
                f'{dataframe_preview["displayed_rows"]} '
                f'de {dataframe_preview["total_rows"]} '
                f'linhas'
            ),
            (
                f'{dataframe_preview["displayed_columns"]} '
                f'de {dataframe_preview["total_columns"]} '
                f'colunas'
            ),
        ]

        elements.append(
            Spacer(
                1,
                0.2 * cm,
            )
        )

        elements.append(
            Paragraph(
                " — ".join(
                    preview_note_parts
                ),
                note_style,
            )
        )

        if (
            dataframe_preview["omitted_rows"] > 0
            or dataframe_preview["omitted_columns"] > 0
        ):
            elements.append(
                Paragraph(
                    (
                        "A prévia foi limitada para "
                        "preservar a legibilidade do relatório."
                    ),
                    note_style,
                )
            )

    elements.extend(
        [
            Spacer(
                1,
                0.8 * cm,
            ),
            Paragraph(
                "Visualizações gráficas",
                section_title_style,
            ),
        ]
    )

    if not chart_results:
        elements.append(
            Paragraph(
                (
                    "Nenhum gráfico compatível "
                    "foi gerado para esta planilha."
                ),
                note_style,
            )
        )

    else:
        elements.extend(
            _build_chart_elements(
                chart_results=chart_results,
                chart_title_style=(
                    chart_title_style
                ),
            )
        )

    document.build(
        elements
    )

    return report_path