from flask_login import UserMixin
from app.extensions import db
import bcrypt
import bleach

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    two_factor_code = db.Column(db.String(6))
    two_factor_expiry = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

class Estudiante(db.Model):
    __tablename__ = 'Estudiantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    senas_direccion = db.Column(db.String(500))
    grado_academico = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    correo = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    anio_solicitud = db.Column(db.Integer, nullable=False)