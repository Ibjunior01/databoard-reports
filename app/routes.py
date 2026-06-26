from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


main_bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}


def allowed_file(filename: str) -> bool:
    """
    Validate if the uploaded file has an allowed spreadsheet extension.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("upload.html")

    if "file" not in request.files:
        flash("Nenhum arquivo foi enviado.", "danger")
        return redirect(url_for("main.upload_file"))

    file = request.files["file"]

    if file.filename == "":
        flash("Selecione um arquivo antes de enviar.", "warning")
        return redirect(url_for("main.upload_file"))

    if not allowed_file(file.filename):
        flash("Formato inválido. Envie apenas arquivos .csv, .xlsx ou .xls.", "danger")
        return redirect(url_for("main.upload_file"))

    filename = secure_filename(file.filename)

    if not filename:
        flash("Nome de arquivo inválido.", "danger")
        return redirect(url_for("main.upload_file"))

    upload_folder = Path(
        current_app.config.get(
            "UPLOAD_FOLDER",
            Path(current_app.root_path) / "uploads",
        )
    )

    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = upload_folder / filename
    file.save(file_path)

    flash(f"Arquivo '{filename}' enviado com sucesso.", "success")
    return redirect(url_for("main.upload_file"))