from app.models import Usuario

def test_user_model():
    user = Usuario(username='test@example.com', role='admin')
    user.set_password('password123')
    assert user.username == 'test@example.com'
    assert user.check_password('password123')
