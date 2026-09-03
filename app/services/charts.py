"""
Serviço responsável pela geração de gráficos do DataBoard Reports.

Os gráficos automáticos são orientados pela classificação semântica das
colunas. Identificadores e texto livre não são usados automaticamente como
métricas ou dimensões de visualização.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import pandas as pd
import plotly.express as px

from app.services.schema_inference import (
    SemanticClassification,
    SemanticType,
    classify_dataframe_schema,
)

METRIC_SEMANTIC_TYPES = {
    SemanticType.CURRENCY,
    SemanticType.PERCENTAGE,
    SemanticType.QUANTITY,
    SemanticType.NUMERIC,
}

CATEGORY_SEMANTIC_TYPES = {
    SemanticType.CATEGORY,
    SemanticType.BOOLEAN,
}

DATE_SEMANTIC_TYPES = {
    SemanticType.DATE,
    SemanticType.DATETIME,
}

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}

STATIC_IMAGE_WIDTH = 1200
STATIC_IMAGE_HEIGHT = 675
STATIC_IMAGE_SCALE = 1
DEFAULT_MAX_CATEGORIES = 10
MAX_AUTOMATIC_CHARTS = 3


@dataclass
class ChartResult:
    """Representa um gráfico interativo utilizado no dashboard."""

    title: str
    chart_type: str
    column_name: str
    html: str
    metric_name: str | None = None


@dataclass
class StaticChartResult:
    """Representa uma versão estática de um gráfico para relatórios."""

    title: str
    chart_type: str
    column_name: str
    image_bytes: bytes
    metric_name: str | None = None


def _validate_dataframe(dataframe: pd.DataFrame) -> None:
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def _to_plotly_html(figure: Any) -> str:
    return figure.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=PLOTLY_CONFIG,
    )


def _to_plotly_image_bytes(figure: Any) -> bytes:
    return figure.to_image(
        format="png",
        width=STATIC_IMAGE_WIDTH,
        height=STATIC_IMAGE_HEIGHT,
        scale=STATIC_IMAGE_SCALE,
    )


def _apply_dark_layout(figure: Any) -> Any:
    """Aplica o layout base dos gráficos interativos do dashboard."""
    figure.update_layout(
        template="plotly_dark",
        title_text=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        margin={
            "l": 48,
            "r": 16,
            "t": 16,
            "b": 56,
        },
        height=340,
        autosize=True,
    )

    figure.update_xaxes(
        automargin=True,
    )

    figure.update_yaxes(
        automargin=True,
    )

    figure.update_traces(
        marker_color="#38bdf8",
    )

    return figure


def _apply_report_layout(figure: Any) -> Any:
    """Aplica layout claro para gráficos incorporados ao PDF."""
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8fafc",
        font_color="#1e293b",
        title_font_color="#0f172a",
        margin={"l": 70, "r": 40, "t": 90, "b": 70},
        width=STATIC_IMAGE_WIDTH,
        height=STATIC_IMAGE_HEIGHT,
    )
    figure.update_traces(marker_color="#38bdf8")
    return figure


def _classifications(
    dataframe: pd.DataFrame,
) -> dict[str, SemanticClassification]:
    return classify_dataframe_schema(dataframe)


def _columns_of_types(
    dataframe: pd.DataFrame,
    classifications: dict[str, SemanticClassification],
    semantic_types: set[SemanticType],
) -> list[str]:
    return [
        str(column)
        for column in dataframe.columns
        if (
            str(column) in classifications
            and classifications[str(column)].semantic_type in semantic_types
        )
    ]


def _select_category_column(
    dataframe: pd.DataFrame,
    classifications: dict[str, SemanticClassification],
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> str | None:
    """Seleciona dimensão categórica útil e evita cardinalidade excessiva."""
    candidates = _columns_of_types(
        dataframe,
        classifications,
        CATEGORY_SEMANTIC_TYPES,
    )

    cardinality_limit = max(max_categories * 2, 20)

    for column in candidates:
        unique_count = int(dataframe[column].nunique(dropna=True))
        if 0 < unique_count <= cardinality_limit:
            return column

    return None


def _select_metric_columns(
    dataframe: pd.DataFrame,
    classifications: dict[str, SemanticClassification],
) -> list[str]:
    return _columns_of_types(
        dataframe,
        classifications,
        METRIC_SEMANTIC_TYPES,
    )


def _select_date_column(
    dataframe: pd.DataFrame,
    classifications: dict[str, SemanticClassification],
) -> str | None:
    columns = _columns_of_types(
        dataframe,
        classifications,
        DATE_SEMANTIC_TYPES,
    )
    return columns[0] if columns else None


def _parse_metric_value(
    value: Any,
    semantic_type: SemanticType,
) -> float | None:
    if pd.isna(value) or isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    text = text.replace("\u00a0", "").replace(" ", "")

    if semantic_type is SemanticType.CURRENCY:
        text = re.sub(
            r"^(?:R\$|BRL)",
            "",
            text,
            flags=re.IGNORECASE,
        )

    if semantic_type is SemanticType.PERCENTAGE:
        text = text.removesuffix("%")

    if "." in text and "," in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")
    elif semantic_type is SemanticType.CURRENCY and re.fullmatch(
        r"[+-]?\d{1,3}(?:\.\d{3})+", text
    ):
        text = text.replace(".", "")

    try:
        return float(text)
    except ValueError:
        return None


def _coerce_metric_series(
    series: pd.Series,
    semantic_type: SemanticType,
) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series.dtype):
        return pd.to_numeric(series, errors="coerce")

    return pd.to_numeric(
        series.map(lambda value: _parse_metric_value(value, semantic_type)),
        errors="coerce",
    )


def _prepare_metric_dataframe(
    dataframe: pd.DataFrame,
    column: str,
    classification: SemanticClassification,
) -> pd.DataFrame:
    prepared = dataframe.copy()
    prepared[column] = _coerce_metric_series(
        prepared[column],
        classification.semantic_type,
    )
    return prepared


def _build_categorical_bar_figure(
    dataframe: pd.DataFrame,
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> tuple[Any, str] | None:
    if dataframe.empty:
        return None

    classifications = _classifications(dataframe)
    column_name = _select_category_column(
        dataframe,
        classifications,
        max_categories=max_categories,
    )
    if column_name is None:
        return None

    series = dataframe[column_name].copy()
    series = series.where(series.notna(), "Ausente")
    series = series.astype(str).replace("", "Vazio")

    counts = series.value_counts().head(max_categories).reset_index()
    counts.columns = [column_name, "Quantidade"]

    figure = px.bar(
        counts,
        x=column_name,
        y="Quantidade",
        title=f"Distribuição por {column_name}",
        labels={
            column_name: column_name,
            "Quantidade": "Quantidade",
        },
    )
    return figure, column_name


def _build_numeric_histogram_figure(
    dataframe: pd.DataFrame,
    nbins: int = 20,
) -> tuple[Any, str] | None:
    if dataframe.empty:
        return None

    classifications = _classifications(dataframe)
    metric_columns = _select_metric_columns(dataframe, classifications)
    if not metric_columns:
        return None

    column_name = metric_columns[0]
    prepared = _prepare_metric_dataframe(
        dataframe,
        column_name,
        classifications[column_name],
    )

    if prepared[column_name].dropna().empty:
        return None

    figure = px.histogram(
        prepared,
        x=column_name,
        nbins=nbins,
        title=f"Distribuição de {column_name}",
        labels={column_name: column_name},
    )
    return figure, column_name


def _build_category_metric_bar_figure(
    dataframe: pd.DataFrame,
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> tuple[Any, str, str] | None:
    if dataframe.empty:
        return None

    classifications = _classifications(dataframe)
    category_column = _select_category_column(
        dataframe,
        classifications,
        max_categories=max_categories,
    )
    metric_columns = _select_metric_columns(dataframe, classifications)

    if category_column is None or not metric_columns:
        return None

    metric_column = metric_columns[0]
    prepared = _prepare_metric_dataframe(
        dataframe,
        metric_column,
        classifications[metric_column],
    )
    prepared = prepared[[category_column, metric_column]].dropna()

    if prepared.empty:
        return None

    grouped = (
        prepared.groupby(category_column, dropna=False)[metric_column]
        .sum()
        .sort_values(ascending=False)
        .head(max_categories)
        .reset_index()
    )

    figure = px.bar(
        grouped,
        x=category_column,
        y=metric_column,
        title=f"{metric_column} por {category_column}",
        labels={
            category_column: category_column,
            metric_column: metric_column,
        },
    )
    return figure, category_column, metric_column


def _build_time_series_figure(
    dataframe: pd.DataFrame,
) -> tuple[Any, str, str] | None:
    if dataframe.empty:
        return None

    classifications = _classifications(dataframe)
    date_column = _select_date_column(dataframe, classifications)
    metric_columns = _select_metric_columns(dataframe, classifications)

    if date_column is None or not metric_columns:
        return None

    metric_column = metric_columns[0]
    prepared = dataframe[[date_column, metric_column]].copy()
    prepared[date_column] = pd.to_datetime(
        prepared[date_column],
        errors="coerce",
        dayfirst=True,
    )
    prepared[metric_column] = _coerce_metric_series(
        prepared[metric_column],
        classifications[metric_column].semantic_type,
    )
    prepared = prepared.dropna().sort_values(date_column)

    if prepared.empty:
        return None

    grouped = (
        prepared.groupby(date_column, as_index=False)[metric_column]
        .sum()
        .sort_values(date_column)
    )

    figure = px.line(
        grouped,
        x=date_column,
        y=metric_column,
        markers=True,
        title=f"Evolução de {metric_column} por {date_column}",
        labels={
            date_column: date_column,
            metric_column: metric_column,
        },
    )
    return figure, date_column, metric_column


def _build_scatter_figure(
    dataframe: pd.DataFrame,
) -> tuple[Any, str, str] | None:
    if dataframe.empty:
        return None

    classifications = _classifications(dataframe)
    metric_columns = _select_metric_columns(dataframe, classifications)
    if len(metric_columns) < 2:
        return None

    x_column, y_column = metric_columns[:2]
    prepared = dataframe[[x_column, y_column]].copy()

    for column in (x_column, y_column):
        prepared[column] = _coerce_metric_series(
            prepared[column],
            classifications[column].semantic_type,
        )

    prepared = prepared.dropna()
    if prepared.empty:
        return None

    figure = px.scatter(
        prepared,
        x=x_column,
        y=y_column,
        title=f"Relação entre {x_column} e {y_column}",
        labels={
            x_column: x_column,
            y_column: y_column,
        },
    )
    return figure, x_column, y_column


def generate_categorical_bar_chart(
    dataframe: pd.DataFrame,
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> ChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_categorical_bar_figure(dataframe, max_categories)
    if result is None:
        return None

    figure, column_name = result
    figure = _apply_dark_layout(figure)
    return ChartResult(
        title=f"Distribuição por {column_name}",
        chart_type="bar",
        column_name=column_name,
        html=_to_plotly_html(figure),
    )


def generate_numeric_histogram(
    dataframe: pd.DataFrame,
    nbins: int = 20,
) -> ChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_numeric_histogram_figure(dataframe, nbins)
    if result is None:
        return None

    figure, column_name = result
    figure = _apply_dark_layout(figure)
    return ChartResult(
        title=f"Distribuição de {column_name}",
        chart_type="histogram",
        column_name=column_name,
        html=_to_plotly_html(figure),
        metric_name=column_name,
    )


def generate_category_metric_bar_chart(
    dataframe: pd.DataFrame,
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> ChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_category_metric_bar_figure(dataframe, max_categories)
    if result is None:
        return None

    figure, category_column, metric_column = result
    figure = _apply_dark_layout(figure)
    return ChartResult(
        title=f"{metric_column} por {category_column}",
        chart_type="bar",
        column_name=category_column,
        metric_name=metric_column,
        html=_to_plotly_html(figure),
    )


def generate_time_series_chart(
    dataframe: pd.DataFrame,
) -> ChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_time_series_figure(dataframe)
    if result is None:
        return None

    figure, date_column, metric_column = result
    figure = _apply_dark_layout(figure)
    return ChartResult(
        title=f"Evolução de {metric_column} por {date_column}",
        chart_type="line",
        column_name=date_column,
        metric_name=metric_column,
        html=_to_plotly_html(figure),
    )


def generate_scatter_chart(
    dataframe: pd.DataFrame,
) -> ChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_scatter_figure(dataframe)
    if result is None:
        return None

    figure, x_column, y_column = result
    figure = _apply_dark_layout(figure)
    return ChartResult(
        title=f"Relação entre {x_column} e {y_column}",
        chart_type="scatter",
        column_name=x_column,
        metric_name=y_column,
        html=_to_plotly_html(figure),
    )


def generate_categorical_bar_chart_image(
    dataframe: pd.DataFrame,
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> StaticChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_categorical_bar_figure(dataframe, max_categories)
    if result is None:
        return None

    figure, column_name = result
    figure = _apply_report_layout(figure)
    return StaticChartResult(
        title=f"Distribuição por {column_name}",
        chart_type="bar",
        column_name=column_name,
        image_bytes=_to_plotly_image_bytes(figure),
    )


def generate_numeric_histogram_image(
    dataframe: pd.DataFrame,
    nbins: int = 20,
) -> StaticChartResult | None:
    _validate_dataframe(dataframe)
    result = _build_numeric_histogram_figure(dataframe, nbins)
    if result is None:
        return None

    figure, column_name = result
    figure = _apply_report_layout(figure)
    return StaticChartResult(
        title=f"Distribuição de {column_name}",
        chart_type="histogram",
        column_name=column_name,
        metric_name=column_name,
        image_bytes=_to_plotly_image_bytes(figure),
    )


def _static_from_builder_result(
    result: tuple[Any, str, str] | None,
    chart_type: str,
    title_template: str,
) -> StaticChartResult | None:
    if result is None:
        return None

    figure, column_name, metric_name = result
    figure = _apply_report_layout(figure)
    return StaticChartResult(
        title=title_template.format(
            column=column_name,
            metric=metric_name,
        ),
        chart_type=chart_type,
        column_name=column_name,
        metric_name=metric_name,
        image_bytes=_to_plotly_image_bytes(figure),
    )


def generate_category_metric_bar_chart_image(
    dataframe: pd.DataFrame,
    max_categories: int = DEFAULT_MAX_CATEGORIES,
) -> StaticChartResult | None:
    _validate_dataframe(dataframe)
    return _static_from_builder_result(
        _build_category_metric_bar_figure(dataframe, max_categories),
        chart_type="bar",
        title_template="{metric} por {column}",
    )


def generate_time_series_chart_image(
    dataframe: pd.DataFrame,
) -> StaticChartResult | None:
    _validate_dataframe(dataframe)
    return _static_from_builder_result(
        _build_time_series_figure(dataframe),
        chart_type="line",
        title_template="Evolução de {metric} por {column}",
    )


def generate_scatter_chart_image(
    dataframe: pd.DataFrame,
) -> StaticChartResult | None:
    _validate_dataframe(dataframe)
    return _static_from_builder_result(
        _build_scatter_figure(dataframe),
        chart_type="scatter",
        title_template="Relação entre {column} e {metric}",
    )


def generate_automatic_charts(
    dataframe: pd.DataFrame,
    max_charts: int = MAX_AUTOMATIC_CHARTS,
) -> list[ChartResult]:
    """Gera um conjunto pequeno de gráficos semanticamente úteis."""
    _validate_dataframe(dataframe)

    if dataframe.empty or max_charts <= 0:
        return []

    charts: list[ChartResult] = []

    time_chart = generate_time_series_chart(dataframe)
    if time_chart is not None:
        charts.append(time_chart)

    if len(charts) < max_charts:
        category_chart = generate_category_metric_bar_chart(dataframe)
        if category_chart is None:
            category_chart = generate_categorical_bar_chart(dataframe)
        if category_chart is not None:
            charts.append(category_chart)

    if len(charts) < max_charts:
        histogram = generate_numeric_histogram(dataframe)
        if histogram is not None:
            charts.append(histogram)

    if len(charts) < max_charts:
        scatter = generate_scatter_chart(dataframe)
        if scatter is not None:
            charts.append(scatter)

    return charts


def generate_automatic_chart_images(
    dataframe: pd.DataFrame,
    max_charts: int = MAX_AUTOMATIC_CHARTS,
) -> list[StaticChartResult]:
    """Gera versões estáticas dos gráficos automáticos para o PDF."""
    _validate_dataframe(dataframe)

    if dataframe.empty or max_charts <= 0:
        return []

    charts: list[StaticChartResult] = []

    time_chart = generate_time_series_chart_image(dataframe)
    if time_chart is not None:
        charts.append(time_chart)

    if len(charts) < max_charts:
        category_chart = generate_category_metric_bar_chart_image(dataframe)
        if category_chart is None:
            category_chart = generate_categorical_bar_chart_image(dataframe)
        if category_chart is not None:
            charts.append(category_chart)

    if len(charts) < max_charts:
        histogram = generate_numeric_histogram_image(dataframe)
        if histogram is not None:
            charts.append(histogram)

    if len(charts) < max_charts:
        scatter = generate_scatter_chart_image(dataframe)
        if scatter is not None:
            charts.append(scatter)

    return charts
