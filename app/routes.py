from dataclasses import asdict, is_dataclass
from pathlib import Path
from uuid import uuid4

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
from app.services.charts import (
    generate_automatic_chart_images,
    generate_automatic_charts,
)
from app.services.data_loader import (
    InvalidSpreadsheetError,
    UnsupportedFileTypeError,
    allowed_file,
    load_spreadsheet,
    load_spreadsheet_metadata,
)
from app.services.history import (
    create_upload_record,
    delete_upload_record,
    get_upload_record,
    list_upload_records,
)
from app.services.report_history import (
    create_report_record,
    delete_report_record,
    get_report_record,
    list_report_records,
    list_report_records_by_upload,
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
        column: (missing_count / total_rows * 100 if total_rows > 0 else 0)
        for column, missing_count in missing_values.items()
    }

    total_cells = total_rows * len(dataframe.columns)
    total_missing = sum(missing_values.values())

    completeness = (
        ((total_cells - total_missing) / total_cells) * 100
        if total_cells > 0
        else 100.0
    )

    affected_columns = sum(
        1 for missing_count in missing_values.values() if missing_count > 0
    )

    return {
        "numeric_columns": analysis_data.get(
            "numeric_columns",
            [],
        ),
        "categorical_columns": analysis_data.get(
            "categorical_columns",
            [],
        ),
        "metric_columns": analysis_data.get(
            "metric_columns",
            [],
        ),
        "identifier_columns": analysis_data.get(
            "identifier_columns",
            [],
        ),
        "datetime_columns": analysis_data.get(
            "datetime_columns",
            [],
        ),
        "date_columns": analysis_data.get(
            "date_columns",
            [],
        ),
        "percentage_columns": analysis_data.get(
            "percentage_columns",
            [],
        ),
        "currency_columns": analysis_data.get(
            "currency_columns",
            [],
        ),
        "boolean_columns": analysis_data.get(
            "boolean_columns",
            [],
        ),
        "quantity_columns": analysis_data.get(
            "quantity_columns",
            [],
        ),
        "category_columns": analysis_data.get(
            "category_columns",
            [],
        ),
        "text_columns": analysis_data.get(
            "text_columns",
            [],
        ),
        "unknown_columns": analysis_data.get(
            "unknown_columns",
            [],
        ),
        "semantic_types": analysis_data.get(
            "semantic_types",
            {},
        ),
        "semantic_confidence": analysis_data.get(
            "semantic_confidence",
            {},
        ),
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
        "total_missing": total_missing,
        "affected_columns": affected_columns,
        "completeness": round(completeness, 2),
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


def get_existing_report_file_path(
    report_record,
) -> Path | None:
    """
    Retorna o caminho físico de um relatório quando
    o arquivo ainda existe no servidor.

    Returns:
        Path: caminho válido para o PDF.
        None: quando o caminho não existe ou não é um arquivo.
    """

    if not report_record.file_path:
        return None

    report_path = Path(report_record.file_path)

    if not report_path.is_file():
        return None

    return report_path


@main_bp.route("/")
def index():
    return render_template("index.html")


def remove_file_safely(file_path: Path) -> None:
    """
    Remove um arquivo físico sem mascarar o erro original
    caso a limpeza também falhe.
    """

    try:
        file_path.unlink(missing_ok=True)
    except OSError:
        current_app.logger.exception(
            "Falha ao remover arquivo temporário de upload: %s",
            file_path,
        )


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

    stored_filename = f"{uuid4().hex}_{filename}"
    file_path = upload_folder / stored_filename

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

        record = create_upload_record(
            file_name=filename,
            file_extension=file_path.suffix,
            file_path=str(file_path),
            row_count=len(dataframe),
            column_count=len(dataframe.columns),
        )

    except UnsupportedFileTypeError:
        remove_file_safely(file_path)

        flash(
            "Tipo de arquivo não suportado.",
            "error",
        )
        return redirect(url_for("main.upload_file"))

    except FileNotFoundError:
        remove_file_safely(file_path)

        flash(
            "Arquivo enviado não foi encontrado no servidor.",
            "error",
        )
        return redirect(url_for("main.upload_file"))

    except InvalidSpreadsheetError:
        remove_file_safely(file_path)

        current_app.logger.warning(
            "Planilha inválida rejeitada durante o upload: %s",
            filename,
        )

        flash(
            (
                "Não foi possível processar o arquivo enviado. "
                "Verifique se ele é uma planilha válida e tente novamente."
            ),
            "error",
        )

        return redirect(url_for("main.upload_file"))

    except Exception:
        remove_file_safely(file_path)

        current_app.logger.exception(
            "Falha ao processar o upload '%s'.",
            filename,
        )

        flash(
            (
                "Não foi possível processar o arquivo enviado. "
                "Verifique se ele é uma planilha válida e tente novamente."
            ),
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
        uploads=list_upload_records(),
        current_record=record,
    )


@main_bp.route("/dashboard")
def dashboard():
    records = list_upload_records()

    if not records:
        return render_template(
            "dashboard.html",
            metadata=None,
            analysis=None,
            charts=[],
            uploads=[],
            current_record=None,
        )

    selected_upload_id = request.args.get(
        "upload_id",
        type=int,
    )

    if selected_upload_id is None:
        record = records[0]
    else:
        record = get_upload_record(selected_upload_id)

        if record is None:
            flash(
                "O upload selecionado não foi encontrado.",
                "error",
            )
            return redirect(url_for("main.dashboard"))

    file_path = get_existing_upload_file_path(record)

    if file_path is None:
        flash(
            ("O arquivo físico do upload selecionado não foi encontrado."),
            "error",
        )

        return render_template(
            "dashboard.html",
            metadata=None,
            analysis=None,
            charts=[],
            uploads=records,
            current_record=record,
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

    except (
        UnsupportedFileTypeError,
        InvalidSpreadsheetError,
        FileNotFoundError,
    ):
        current_app.logger.exception(
            "Falha ao carregar upload %s no dashboard.",
            record.id,
        )

        flash(
            ("Não foi possível carregar a análise deste upload."),
            "error",
        )

        return render_template(
            "dashboard.html",
            metadata=None,
            analysis=None,
            charts=[],
            uploads=records,
            current_record=record,
        )

    return render_template(
        "dashboard.html",
        filename=record.file_name,
        metadata=metadata,
        analysis=analysis,
        charts=charts,
        uploads=records,
        current_record=record,
    )


@main_bp.route("/history")
def history():
    records = list_upload_records()

    return render_template(
        "history.html",
        records=records,
    )


@main_bp.get("/reports")
def reports_history():
    """
    Exibe todos os relatórios PDF persistidos.
    """

    reports = list_report_records()

    return render_template(
        "reports_history.html",
        reports=reports,
    )


@main_bp.route("/history/<int:record_id>")
def upload_detail(record_id):
    record = get_upload_record(record_id)

    if record is None:
        abort(404)

    reports = list_report_records_by_upload(
        upload_id=record.id,
    )

    return render_template(
        "upload_detail.html",
        record=record,
        reports=reports,
    )


@main_bp.post("/history/<int:record_id>/delete")
def delete_upload(record_id):
    """
    Exclui um upload, os relatórios relacionados
    e os arquivos físicos associados.
    """

    upload_record = get_upload_record(record_id)

    if upload_record is None:
        abort(404)

    try:
        deletion_result = delete_upload_record(upload_record)

    except Exception:
        current_app.logger.exception(
            "Falha ao excluir o upload %s.",
            record_id,
        )

        flash(
            ("Não foi possível excluir o upload. Tente novamente."),
            "error",
        )

        return redirect(
            url_for(
                "main.upload_detail",
                record_id=record_id,
            )
        )

    if deletion_result.missing_files > 0:
        flash(
            (
                "Upload e registros associados excluídos. "
                "Alguns arquivos físicos já não estavam "
                "disponíveis."
            ),
            "success",
        )

    else:
        flash(
            ("Upload e arquivos associados excluídos com sucesso."),
            "success",
        )

    return redirect(url_for("main.history"))


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

    return render_template(
        "dashboard.html",
        filename=record.file_name,
        metadata=metadata,
        analysis=analysis,
        charts=charts,
        uploads=list_upload_records(),
        current_record=record,
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
        chart_results = generate_automatic_chart_images(dataframe)

        report_path = generate_upload_report(
            upload_record=upload_record,
            analysis_result=analysis_result,
            reports_folder=current_app.config["REPORTS_FOLDER"],
            chart_results=chart_results,
            dataframe=dataframe,
        )

        create_report_record(
            upload_id=upload_record.id,
            file_name=report_path.name,
            file_path=report_path,
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


@main_bp.get("/reports/<int:report_id>/download")
def download_existing_report(report_id):
    """
    Disponibiliza para download um relatório
    anteriormente gerado e registrado no banco.
    """

    report_record = get_report_record(report_id)

    if report_record is None:
        abort(404)

    report_path = get_existing_report_file_path(report_record)

    if report_path is None:
        flash(
            ("O arquivo físico deste relatório não foi encontrado no servidor."),
            "error",
        )

        return redirect(
            url_for(
                "main.upload_detail",
                record_id=report_record.upload_id,
            )
        )

    return send_file(
        report_path.resolve(),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=report_record.file_name,
    )


@main_bp.post("/reports/<int:report_id>/delete")
def delete_report(report_id):
    """
    Exclui um relatório persistido e remove
    seu arquivo físico quando disponível.
    """

    report_record = get_report_record(report_id)

    if report_record is None:
        abort(404)

    upload_id = report_record.upload_id

    redirect_to = request.form.get(
        "redirect_to",
        "reports",
    )

    try:
        file_deleted = delete_report_record(report_record)

    except Exception:
        current_app.logger.exception(
            "Falha ao excluir o relatório %s.",
            report_id,
        )

        flash(
            ("Não foi possível excluir o relatório. Tente novamente."),
            "error",
        )

        if redirect_to == "upload":
            return redirect(
                url_for(
                    "main.upload_detail",
                    record_id=upload_id,
                )
            )

        return redirect(url_for("main.reports_history"))

    if file_deleted:
        flash(
            "Relatório excluído com sucesso.",
            "success",
        )

    else:
        flash(
            (
                "O registro do relatório foi excluído. "
                "O arquivo físico já não estava disponível."
            ),
            "success",
        )

    if redirect_to == "upload":
        return redirect(
            url_for(
                "main.upload_detail",
                record_id=upload_id,
            )
        )

    return redirect(url_for("main.reports_history"))
