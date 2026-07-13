from dataclasses import asdict, is_dataclass
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from werkzeug.utils import secure_filename

from app.services.analyzer import analyze_dataframe
from app.services.charts import generate_automatic_charts
from app.services.data_loader import (
    UnsupportedFileTypeError,
    allowed_file,
    load_spreadsheet,
    load_spreadsheet_metadata,
)
from app.services.history import (
    create_upload_record,
    get_upload_record,
    list_upload_records,
)
from app.services.reports import generate_upload_report


main_bp = Blueprint("main", __name__)


def build_dashboard_analysis(analysis_result, dataframe):
    """
    Organiza o resultado da análise automática para uso no dashboard.
    """

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


def get_existing_upload_file_path(upload_record) -> Path | None:
    """
    Retorna o caminho físico do arquivo de um upload quando ele existe.

    Returns:
        Path: caminho válido para o arquivo físico.
        None: quando o registro não possui caminho ou o arquivo não existe.
    """

    if not upload_record.file_path:
        return None

    file_path = Path(upload_record.file_path)

    if not file_path.is_file():
        return None

    return file_path


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
        flash(
            "Tipo de arquivo não permitido. Envie arquivos CSV, XLSX ou XLS.",
            "error",
        )
        return redirect(url_for("main.upload_file"))

    filename = secure_filename(uploaded_file.filename)

    upload_folder = Path(
        current_app.config.get(
            "UPLOAD_FOLDER",
            "app/uploads",
        )
    )
    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = upload_folder / filename
    uploaded_file.save(file_path)

    try:
        dataframe = load_spreadsheet(file_path)
        metadata = load_spreadsheet_metadata(file_path)
        analysis_result = analyze_dataframe(dataframe)
        analysis = build_dashboard_analysis(
            analysis_result,
            dataframe,
        )
        charts = generate_automatic_charts(dataframe)

        create_upload_record(
            file_name=filename,
            file_extension=file_path.suffix,
            row_count=len(dataframe),
            column_count=len(dataframe.columns),
            file_path=str(file_path),
        )

    except UnsupportedFileTypeError:
        flash("Tipo de arquivo não suportado.", "error")
        return redirect(url_for("main.upload_file"))

    except FileNotFoundError:
        flash(
            "Arquivo enviado não foi encontrado no servidor.",
            "error",
        )
        return redirect(url_for("main.upload_file"))

    flash("Arquivo carregado com sucesso", "success")

    return render_template(
        "dashboard.html",
        filename=filename,
        metadata=metadata,
        analysis=analysis,
        charts=charts,
        success_message="Arquivo carregado com sucesso",
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


@main_bp.route("/history/<int:record_id>")
def upload_detail(record_id):
    record = get_upload_record(record_id)

    if record is None:
        abort(404)

    return render_template(
        "upload_detail.html",
        record=record,
    )


@main_bp.route("/history/<int:record_id>/reprocess")
def reprocess_upload(record_id):
    record = get_upload_record(record_id)

    if record is None:
        abort(404)

    file_path = get_existing_upload_file_path(record)

    if file_path is None:
        flash(
            "O arquivo físico deste upload não foi encontrado no servidor.",
            "error",
        )
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=record.id,
            )
        )

    try:
        dataframe = load_spreadsheet(file_path)
        metadata = load_spreadsheet_metadata(file_path)
        analysis_result = analyze_dataframe(dataframe)
        analysis = build_dashboard_analysis(
            analysis_result,
            dataframe,
        )
        charts = generate_automatic_charts(dataframe)

    except UnsupportedFileTypeError:
        flash(
            "O tipo do arquivo salvo não é mais suportado.",
            "error",
        )
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=record.id,
            )
        )

    except FileNotFoundError:
        flash(
            "O arquivo físico deste upload não foi encontrado no servidor.",
            "error",
        )
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=record.id,
            )
        )

    preview = dataframe.head(10).to_html(
        classes="data-preview-table",
        index=False,
        border=0,
    )

    return render_template(
        "dashboard.html",
        filename=record.file_name,
        metadata=metadata,
        preview=preview,
        analysis=analysis,
        charts=charts,
    )


@main_bp.get("/history/<int:record_id>/report")
def download_upload_report(record_id):
    """
    Gera e disponibiliza para download o relatório PDF de um upload,
    incluindo o resumo da análise automática da planilha.
    """

    upload_record = get_upload_record(record_id)

    if upload_record is None:
        abort(404)

    file_path = get_existing_upload_file_path(upload_record)

    if file_path is None:
        flash(
            "O arquivo físico deste upload não foi encontrado no servidor.",
            "error",
        )
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=upload_record.id,
            )
        )

    try:
        dataframe = load_spreadsheet(file_path)
        analysis_result = analyze_dataframe(dataframe)

        report_path = generate_upload_report(
            upload_record=upload_record,
            analysis_result=analysis_result,
            reports_folder=current_app.config["REPORTS_FOLDER"],
        )

    except UnsupportedFileTypeError:
        flash(
            "O tipo do arquivo salvo não é suportado para geração do relatório.",
            "error",
        )
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=upload_record.id,
            )
        )

    except FileNotFoundError:
        flash(
            "O arquivo físico deste upload não foi encontrado no servidor.",
            "error",
        )
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=upload_record.id,
            )
        )

    return send_file(
        report_path.resolve(),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=report_path.name,
    )