from dataclasses import asdict, is_dataclass
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.services.analyzer import analyze_dataframe
from app.services.charts import generate_automatic_charts
from app.services.data_loader import (
    UnsupportedFileTypeError,
    allowed_file,
    load_spreadsheet,
    load_spreadsheet_metadata,
)
from app.services.history import create_upload_record, list_upload_records

main_bp = Blueprint("main", __name__)


def build_dashboard_analysis(analysis_result, dataframe):
    if is_dataclass(analysis_result):
        analysis_data = asdict(analysis_result)
    elif isinstance(analysis_result, dict):
        analysis_data = analysis_result
    else:
        analysis_data = vars(analysis_result)

    total_rows = len(dataframe)

    missing_values = dataframe.isna().sum().to_dict()

    missing_percentage = {
        column: (missing_count / total_rows * 100) if total_rows > 0 else 0
        for column, missing_count in missing_values.items()
    }

    return {
        "numeric_columns": analysis_data.get("numeric_columns", []),
        "categorical_columns": analysis_data.get("categorical_columns", []),
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
        "numeric_statistics": (
            analysis_data.get("numeric_statistics")
            or analysis_data.get("numeric_statistics_by_column")
            or analysis_data.get("summary_statistics")
            or {}
        ),
    }


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("upload.html")

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        flash("Nenhum arquivo foi selecionado.", "error")
        return redirect(url_for("main.upload_file"))

    if not allowed_file(uploaded_file.filename):
        flash("Tipo de arquivo não permitido. Envie arquivos CSV, XLSX ou XLS.", "error")
        return redirect(url_for("main.upload_file"))

    filename = secure_filename(uploaded_file.filename)

    upload_folder = Path(current_app.config.get("UPLOAD_FOLDER", "app/uploads"))
    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = upload_folder / filename
    uploaded_file.save(file_path)

    try:
        dataframe = load_spreadsheet(file_path)
        metadata = load_spreadsheet_metadata(file_path)
        analysis_result = analyze_dataframe(dataframe)
        analysis = build_dashboard_analysis(analysis_result, dataframe)
        charts = generate_automatic_charts(dataframe)

        create_upload_record(
            file_name=filename,
            file_extension=file_path.suffix,
            row_count=len(dataframe),
            column_count=len(dataframe.columns),
        )

    except UnsupportedFileTypeError:
        flash("Tipo de arquivo não suportado.", "error")
        return redirect(url_for("main.upload_file"))
    except FileNotFoundError:
        flash("Arquivo enviado não foi encontrado no servidor.", "error")
        return redirect(url_for("main.upload_file"))
    except Exception:
        flash("Não foi possível ler a planilha enviada. Verifique o formato do arquivo.", "error")
        return redirect(url_for("main.upload_file"))

    flash("Arquivo carregado com sucesso.", "success")

    return render_template(
        "dashboard.html",
        metadata=metadata,
        analysis=analysis,
        charts=charts,
    )


@main_bp.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        metadata=None,
        analysis=None,
        charts=[],
    )


@main_bp.route("/history")
def history():
    records = list_upload_records()

    return render_template(
        "history.html",
        records=records,
    )