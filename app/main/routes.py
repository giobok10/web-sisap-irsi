# app/main/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.main.forms import StudentForm, ExcelUploadForm
from app.models import Estudiante
from app import db
from flask_login import login_required
from app.main.utils import procesar_excel
from app.decorators import role_required
import bleach
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

@main.route('/')
@login_required
@role_required('admin', 'director', 'consulta')
def index():
    return render_template('main/index.html')

@main.route('/form_estudiante', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'director')
def form_estudiante():
    form = StudentForm()
    if form.validate_on_submit():
        cleaned_senas_direccion = bleach.clean(
            form.senas_direccion.data,
            tags=[], attributes={}, protocols=[],
            strip=True
        )
        estudiante = Estudiante(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            pais=form.pais.data,
            ciudad=form.ciudad.data,
            senas_direccion=cleaned_senas_direccion,
            grado_academico=form.grado_academico.data,
            dni=form.dni.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            correo=form.correo.data,
            telefono=form.telefono.data,
            anio_solicitud=form.anio_solicitud.data
        )
        db.session.add(estudiante)
        try:
            db.session.commit()
            flash('Estudiante registrado con éxito', 'success')
            return redirect(url_for('main.form_estudiante'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: El DNI ya está registrado. Por favor, elija otro.', 'danger')

    return render_template('main/form_estudiante.html', form=form)

@main.route('/carga_excel', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def carga_excel():
    form = ExcelUploadForm()
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            flash('Debe seleccionar un archivo.', 'danger')
            return redirect(url_for('main.carga_excel'))

        if not file.filename.endswith('.xlsx'):
            flash('Formato inválido. Solo se permiten archivos .xlsx', 'danger')
            return redirect(url_for('main.carga_excel'))

        try:
            errores = procesar_excel(file)
            if not errores:
                flash('Archivo cargado exitosamente.', 'success')
            else:
                for e in errores:
                    flash(e, 'danger')
        except Exception as e:
            flash(f'Error al procesar el archivo: {str(e)}', 'danger')

    return render_template('main/carga_excel.html', form=form)

@main.route('/reporte')
@login_required
@role_required('admin', 'director', 'consulta')
def reporte():
    estudiantes = Estudiante.query.all()
    return render_template('main/reporte.html', estudiantes=estudiantes)
