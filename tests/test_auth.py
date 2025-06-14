from app import db
from app.models import Usuario
from flask import session

def test_login(client, app):
    with app.app_context():
        user = Usuario(username='test@example.com', role='admin')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={
        'username': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert 'Código 2FA enviado' in response.get_data(as_text=True)
