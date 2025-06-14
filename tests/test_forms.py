# tests/test_forms.py

import pytest
from flask import current_app
from app.auth.forms import LoginForm, TwoFactorForm
from app import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

def test_login_form(app):
    with app.app_context():
        form = LoginForm(username='test@example.com', password='password123')
        assert form.validate()

def test_two_factor_form(app):
    with app.app_context():
        form = TwoFactorForm(code='123456')
        assert form.validate()
