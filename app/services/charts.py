"""
Serviço responsável pela geração de gráficos do DataBoard Reports.

Responsabilidades:
- Criar gráficos interativos com Plotly para o dashboard.
- Gerar versões estáticas dos gráficos para relatórios PDF.
- Reutilizar a mesma lógica de construção dos gráficos em diferentes saídas.
"""

from dataclasses import dataclass
from typing import Any, Optional

import pandas as pd
import plotly.express as px


@dataclass
class ChartResult:
    """
    Representa um gráfico interativo utilizado no dashboard.
    """

    title: str
    chart_type: str
    column_name: str
    html: str


@dataclass
class StaticChartResult:
    """
    Representa uma versão estática de um gráfico para uso em relatórios.
    """

    title: str
    chart_type: str
    column_name: str
    image_bytes: bytes


PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}

STATIC_IMAGE_WIDTH = 1200
STATIC_IMAGE_HEIGHT = 675
STATIC_IMAGE_SCALE = 1


def _validate_dataframe(dataframe: pd.DataFrame) -> None:
    """
    Valida se o objeto informado é um DataFrame do Pandas.
    """

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def _to_plotly_html(figure: Any) -> str:
    """
    Converte uma figura Plotly para HTML reutilizável no dashboard.
    """

    return figure.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=PLOTLY_CONFIG,
    )


def _to_plotly_image_bytes(figure: Any) -> bytes:
    """
    Converte uma figura Plotly em imagem PNG armazenada em memória.

    A exportação utiliza o Kaleido por meio do método to_image().
    """

    return figure.to_image(
        format="png",
        width=STATIC_IMAGE_WIDTH,
        height=STATIC_IMAGE_HEIGHT,
        scale=STATIC_IMAGE_SCALE,
    )


def _apply_dark_layout(figure: Any) -> Any:
    """
    Aplica o layout utilizado nos gráficos interativos do dashboard.
    """

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        margin=dict(l=32, r=24, t=56, b=40),
        height=360,
    )

    figure.update_traces(
        marker_color="#38bdf8",
    )

    return figure


def _apply_report_layout(figure: Any) -> Any:
    """
    Aplica um layout claro e legível para uso no relatório PDF.
    """

    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8fafc",
        font_color="#1e293b",
        title_font_color="#0f172a",
        margin=dict(l=70, r=40, t=90, b=70),
        width=STATIC_IMAGE_WIDTH,
        height=STATIC_IMAGE_HEIGHT,
    )

    figure.update_traces(
        marker_color="#38bdf8",
    )

    return figure


def _build_categorical_bar_figure(
    dataframe: pd.DataFrame,
    max_categories: int = 10,
) -> Optional[tuple[Any, str]]:
    """
    Cria a figura base do gráfico de barras categórico.

    A figura ainda não recebe o tema específico de dashboard ou relatório.
    """

    if dataframe.empty:
        return None

    categorical_columns = dataframe.select_dtypes(
        include=[
            "object",
            "category",
            "string",
            "bool",
        ]
    ).columns.tolist()

    if not categorical_columns:
        return None

    column_name = categorical_columns[0]

    series = dataframe[column_name].copy()
    series = series.where(series.notna(), "Ausente")
    series = series.astype(str).replace("", "Vazio")

    counts = (
        series.value_counts()
        .head(max_categories)
        .reset_index()
    )

    counts.columns = [
        column_name,
        "Quantidade",
    ]

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
) -> Optional[tuple[Any, str]]:
    """
    Cria a figura base do histograma numérico.

    A figura ainda não recebe o tema específico de dashboard ou relatório.
    """

    if dataframe.empty:
        return None

    numeric_columns = dataframe.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if not numeric_columns:
        return None

    column_name = numeric_columns[0]

    if dataframe[column_name].dropna().empty:
        return None

    figure = px.histogram(
        dataframe,
        x=column_name,
        nbins=nbins,
        title=f"Distribuição de {column_name}",
        labels={
            column_name: column_name,
        },
    )

    return figure, column_name


def generate_categorical_bar_chart(
    dataframe: pd.DataFrame,
    max_categories: int = 10,
) -> Optional[ChartResult]:
    """
    Gera um gráfico de barras interativo para a primeira
    coluna categórica disponível.
    """

    _validate_dataframe(dataframe)

    result = _build_categorical_bar_figure(
        dataframe=dataframe,
        max_categories=max_categories,
    )

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
) -> Optional[ChartResult]:
    """
    Gera um histograma interativo para a primeira
    coluna numérica disponível.
    """

    _validate_dataframe(dataframe)

    result = _build_numeric_histogram_figure(
        dataframe=dataframe,
        nbins=nbins,
    )

    if result is None:
        return None

    figure, column_name = result

    figure = _apply_dark_layout(figure)

    return ChartResult(
        title=f"Distribuição de {column_name}",
        chart_type="histogram",
        column_name=column_name,
        html=_to_plotly_html(figure),
    )


def generate_categorical_bar_chart_image(
    dataframe: pd.DataFrame,
    max_categories: int = 10,
) -> Optional[StaticChartResult]:
    """
    Gera uma imagem PNG do gráfico de barras categórico
    para uso em relatórios PDF.
    """

    _validate_dataframe(dataframe)

    result = _build_categorical_bar_figure(
        dataframe=dataframe,
        max_categories=max_categories,
    )

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
) -> Optional[StaticChartResult]:
    """
    Gera uma imagem PNG do histograma numérico
    para uso em relatórios PDF.
    """

    _validate_dataframe(dataframe)

    result = _build_numeric_histogram_figure(
        dataframe=dataframe,
        nbins=nbins,
    )

    if result is None:
        return None

    figure, column_name = result

    figure = _apply_report_layout(figure)

    return StaticChartResult(
        title=f"Distribuição de {column_name}",
        chart_type="histogram",
        column_name=column_name,
        image_bytes=_to_plotly_image_bytes(figure),
    )


def generate_automatic_charts(
    dataframe: pd.DataFrame,
) -> list[ChartResult]:
    """
    Gera os gráficos interativos disponíveis para o dashboard.
    """

    _validate_dataframe(dataframe)

    charts = []

    categorical_chart = generate_categorical_bar_chart(
        dataframe
    )

    numeric_chart = generate_numeric_histogram(
        dataframe
    )

    if categorical_chart:
        charts.append(categorical_chart)

    if numeric_chart:
        charts.append(numeric_chart)

    return charts


def generate_automatic_chart_images(
    dataframe: pd.DataFrame,
) -> list[StaticChartResult]:
    """
    Gera versões estáticas dos gráficos disponíveis
    para inserção em relatórios PDF.
    """

    _validate_dataframe(dataframe)

    charts = []

    categorical_chart = generate_categorical_bar_chart_image(
        dataframe
    )

    numeric_chart = generate_numeric_histogram_image(
        dataframe
    )

    if categorical_chart:
        charts.append(categorical_chart)

    if numeric_chart:
        charts.append(numeric_chart)

    return charts