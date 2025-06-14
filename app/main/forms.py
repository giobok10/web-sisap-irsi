# app/main/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models import Estudiante

PAISES = ['Guatemala', 'El Salvador', 'Honduras', 'Panamá', 'República Dominicana', 'Paraguay', 'Colombia', 'Costa Rica', 'Nicaragua', 'México']
CIUDADES = {
    'Guatemala': ['Guatemala City', 'Quetzaltenango', 'Zacapa'],
    'El Salvador': ['San Salvador', 'Santa Ana', 'Sonsonate']
}

class StudentForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    pais = SelectField('País de Origen', choices=[(p, p) for p in PAISES], validators=[DataRequired()])
    ciudad = SelectField('Ciudad', choices=[(c, c) for c in CIUDADES['Guatemala']], validators=[DataRequired()])
    senas_direccion = TextAreaField('Otras Señas de Dirección')
    grado_academico = StringField('Último Grado Académico', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired(), Length(max=20)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono')
    anio_solicitud = IntegerField('Año de Solicitud', validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def validate_dni(self, field):
        if Estudiante.query.filter_by(dni=field.data).first():
            raise ValidationError('El DNI ya está registrado. Por favor, elija otro.')

# Aquí agregas la clase para la carga de Excel
class ExcelUploadForm(FlaskForm):
    file = FileField('Archivo Excel', validators=[DataRequired()])
