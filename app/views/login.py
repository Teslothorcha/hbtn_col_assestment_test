"""
Login view
"""
from flask import (render_template, redirect, url_for, Blueprint,
                   request, current_app, abort)
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse, urljoin
from flask_mail import Message
from decimal import Decimal

from app.forms.login import LoginForm, SignupForm
from app import app, login_manager, mail
from app.models.userModel import User
from app.models.paymentModel import Wallet

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route("/signup/", methods=["GET", "POST"])
def signup():
    """
    Sign up
    """
    if current_user.is_authenticated:
        return redirect(url_for('public_bp.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        gov_id = form.gov_id.data
        email = form.email.data
        company = form.company.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_user_by_email(email)
        if user is not None:
            error = f'An user with this {email} already exists'
        else:
            user = User(name=name, last_name=last_name, gov_id=gov_id,
                        email=email, company=company, password=password)
            user.save_user()

            wallet = Wallet(balance=Decimal(0), user=user)
            wallet.save()

            with app.app_context():
                msg = Message(subject='Welcome to dreamful',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=[email],
                        body=f'Hi {name}, welcome to dreamful',
                        html=f'<p>Hi <strong>{name}</strong>, Welcome to dreamful</p>')
                mail.send(msg)

            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                return abort(400)

            return redirect(url_for('public_bp.index'))
    return render_template("user/signup.html", form=form, error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    login route
    """
    if current_user.is_authenticated:
        return redirect(url_for('public_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_email(email=form.email.data)
        if user is not None and user.validate_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                return abort(400)

            return redirect(url_for('public_bp.index'))
    return render_template('user/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public_bp.index'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(int(user_id))