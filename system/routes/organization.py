from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from ..forms import OrganizationForm
from ..models import OrganizationModel

org_blp = Blueprint("org_blp", __name__, template_folder='templates', static_folder='static')


@org_blp.route('/organization', methods=['GET'])
@login_required
def all_orgs():
    orgs = OrganizationModel.query.all()
    return render_template('org_templates/all_orgs.html', user=current_user, orgs=orgs)


@org_blp.route('/create_organization', methods=['GET', 'POST'])
@login_required
def create_orgs():
    form = OrganizationForm()
    if request.method == "POST":
        organization = OrganizationModel(
            name=form.name.data,
            description=form.description.data,
            active_date=form.active_date.data,
            is_active=form.is_active.data,
            location=form.location.data,
            user_id=current_user.id
        )
        try:
            organization.save_to_db()
            flash('Organization created successfully!', 'success')
            return redirect(url_for('org_blp.all_orgs'))
        except IntegrityError as e:
            flash('Organization is not unique!', 'success')
        except Exception as e:
            flash('Organization not created successfully!', 'errr')
    return render_template('org_templates/create_org.html', form=form, user=current_user)
