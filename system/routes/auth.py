import traceback
from datetime import datetime

from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import current_user, login_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..db import db
from ..forms import RegistrationForm, LoginForm, ForgotPasswordForm
from ..models import UserModel

auth_blp = Blueprint("auth_blp", __name__, template_folder='templates', static_folder='static')

EXISTING_USER_ERROR = "A user withe the details provided is already registered"
PASSWORD_MATCH_ERROR = "Passwords must match"
USER_SAVE_ERROR = "Failed to save user, Please contact support"
CREATION_SUCCESS = "User Created Successfully"
WRONG_PASSWORD_ERROR = "Incorrect Password! Try Again"
LOGIN_SUCCESS = "Login success"
WRONG_PHONE_NO = "Wrong phone number error"
LOGOUT_SUCCESS = "You have logged out"
EMAIL_MISSING_ERROR = "This is the super admin, please give the email"
EMAIL_MATCH_ERROR = "This is the wrong email"
PASSWORD_UPDATE_SUCCESS = "Password updated successfully"
USER_UNAVAILABLE_ERROR = "User not found"


@auth_blp.route('/register/new/pos/user', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_no = form.phone_no.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        existing_user = UserModel.query.filter_by(phone_no=phone_no).first()
        if existing_user:
            flash(EXISTING_USER_ERROR, category="error")
        else:
            if password == confirm_password:
                new_user = UserModel(first_name=first_name, last_name=last_name, phone_no=phone_no,
                                     password=pbkdf2_sha256.hash(password),
                                     user_type="super_admin")
                try:
                    new_user.save_to_db()
                    flash(CREATION_SUCCESS, category="success")
                    return redirect(url_for("auth_blp.login"))
                except IntegrityError as e:
                    traceback.print_exc()
                    db.session.rollback()
                    flash(EXISTING_USER_ERROR, category="error")
                except Exception as e:
                    print(e)
                    flash(USER_SAVE_ERROR, category="error")
            else:
                flash(PASSWORD_MATCH_ERROR, category="error")

    return render_template('user_templates/register.html', form=form, user=current_user)


@auth_blp.route("/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        phone_no = form.phone_no.data
        password = form.password.data

        user = UserModel.query.filter_by(phone_no=phone_no).first()
        if user:
            if user.check_pwd(password):
                flash(LOGIN_SUCCESS, category="success")
                user.last_login = datetime.utcnow()
                user.update_db()
                login_user(user, remember=True)
                return redirect(url_for("home_blp.homepage"))
            else:
                flash(WRONG_PASSWORD_ERROR, category="error")
        else:
            flash(WRONG_PHONE_NO, category="error")
    return render_template("user_templates/login.html", form=form, user=current_user)


@auth_blp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(LOGOUT_SUCCESS, category="success")
    return redirect(url_for("auth_blp.login"))


@auth_blp.route("/forgot", methods=["POST", "GET"])
def forgot():
    form = ForgotPasswordForm()
    email = form.email.data
    pass_1 = form.password.data
    pass_2 = form.confirm_password.data
    phone_no = form.phone_no.data

    if request.method == "POST":
        user = UserModel.find_by_phone_no(phone_no)
        if not user:
            flash(USER_UNAVAILABLE_ERROR, category="error")
        else:
            if user.user_type == "super_admin":
                if email is None:
                    flash(EMAIL_MISSING_ERROR, category="error")
                elif email != user.email:
                    flash(EMAIL_MATCH_ERROR, category="error")
                elif pass_1 != pass_2:
                    flash(PASSWORD_MATCH_ERROR, category="error")
                else:
                    user.password = pbkdf2_sha256.hash(pass_1)
                    user.update_db()
                    flash(PASSWORD_UPDATE_SUCCESS, category="success")
                    return redirect(url_for("auth_blp.login"))
            else:
                if pass_1 != pass_2:
                    flash(PASSWORD_MATCH_ERROR, category="error")
                else:
                    user.password = pbkdf2_sha256.hash(pass_1)
                    user.update_db()
                    flash(PASSWORD_UPDATE_SUCCESS, category="success")
                    return redirect(url_for("auth_blp.login"))

    return render_template("user_templates/forgot.html", form=form, user=current_user)
