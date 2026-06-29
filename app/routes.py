from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.services.data_loader import (
    UnsupportedFileTypeError,
    allowed_file,
    load_spreadsheet_metadata,
)

main_bp = Blueprint("main", __name__)


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
        metadata = load_spreadsheet_metadata(file_path)
    except UnsupportedFileTypeError:
        flash("Tipo de arquivo não suportado.", "error")
        return redirect(url_for("main.uploa_filed"))
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
    )


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", metadata=None)


@main_bp.route("/history")
def history():
    return render_template("history.html")