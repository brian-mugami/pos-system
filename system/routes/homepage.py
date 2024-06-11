from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_blp = Blueprint("home_blp", __name__, template_folder='templates', static_folder='static')


@home_blp.route("/home")
@login_required
def homepage():
    return render_template("home_templates/home_page.html", user=current_user)
