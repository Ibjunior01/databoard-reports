"""
Serviço de geração de gráficos.

Futuras responsabilidades:
- Criar gráficos interativos com Plotly.
- Gerar gráficos de barras, linhas, pizza e indicadores.
- Preparar visualizações para os dashboards.
"""

from dataclasses import dataclass
from typing import Optional

import pandas as pd
import plotly.express as px


@dataclass
class ChartResult:
    title: str
    chart_type: str
    column_name: str
    html: str


PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}


def _validate_dataframe(dataframe: pd.DataFrame) -> None:
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")


def _to_plotly_html(figure) -> str:
    return figure.to_html(
        full_html=False,
        include_plotlyjs=False,
        config=PLOTLY_CONFIG,
    )


def _apply_dark_layout(figure):
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        margin=dict(l=32, r=24, t=56, b=40),
        height=360,
    )
    return figure


def generate_categorical_bar_chart(
    dataframe: pd.DataFrame,
    max_categories: int = 10,
) -> Optional[ChartResult]:
    _validate_dataframe(dataframe)

    if dataframe.empty:
        return None

    categorical_columns = dataframe.select_dtypes(
        include=["object", "category", "string", "bool"]
    ).columns.tolist()

    if not categorical_columns:
        return None

    column_name = categorical_columns[0]

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

    figure.update_traces(marker_color="#38bdf8")
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
    _validate_dataframe(dataframe)

    if dataframe.empty:
        return None

    numeric_columns = dataframe.select_dtypes(include=["number"]).columns.tolist()

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

    figure.update_traces(marker_color="#38bdf8")
    figure = _apply_dark_layout(figure)

    return ChartResult(
        title=f"Distribuição de {column_name}",
        chart_type="histogram",
        column_name=column_name,
        html=_to_plotly_html(figure),
    )


def generate_automatic_charts(dataframe: pd.DataFrame) -> list[ChartResult]:
    _validate_dataframe(dataframe)

    charts = []

    categorical_chart = generate_categorical_bar_chart(dataframe)
    numeric_chart = generate_numeric_histogram(dataframe)

    if categorical_chart:
        charts.append(categorical_chart)

    if numeric_chart:
        charts.append(numeric_chart)

    return charts