from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.auth.forms import LoginForm, TwoFactorForm
from app.models import Usuario
from app import db, mail
from flask_login import login_user, logout_user, login_required
import random
from datetime import datetime, timedelta
from flask_mail import Message

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Generar código 2FA
            code = ''.join(random.choices('0123456789', k=6))
            user.two_factor_code = code
            user.two_factor_expiry = datetime.now() + timedelta(minutes=5)
            db.session.commit()

            # Enviar código por correo
            msg = Message('Código 2FA', sender='tu_correo@gmail.com', recipients=[user.username])
            msg.body = f'Tu código es: {code}'
            mail.send(msg)

            flash('Código 2FA enviado a tu correo.')
            return redirect(url_for('auth.two_factor'))
        flash('Credenciales inválidas.')
    return render_template('auth/login.html', form=form)

@auth.route('/two_factor', methods=['GET', 'POST'])
def two_factor():
    form = TwoFactorForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(two_factor_code=form.code.data).first()
        if user and user.two_factor_expiry > datetime.now():
            login_user(user)
            user.two_factor_code = None
            user.two_factor_expiry = None
            db.session.commit()
            return redirect(url_for('main.index'))
        flash('Código inválido o expirado.')
    return render_template('auth/two_factor.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
