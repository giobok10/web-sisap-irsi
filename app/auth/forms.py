from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar Sesión')

class TwoFactorForm(FlaskForm):
    code = StringField('Código 2FA', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verificar')
