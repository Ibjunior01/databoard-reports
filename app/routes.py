from flask import Blueprint, render_template


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    Página inicial do DataBoard Reports.

    Nesta primeira entrega, a aplicação possui apenas a home page.
    Upload, dashboards, histórico e relatórios serão implementados
    nas próximas conversas.
    """
    return render_template("index.html")