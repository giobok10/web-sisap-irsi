import pandas as pd
from app.models import Estudiante
from app import db
from flask_login import current_user

def procesar_excel(file):
    df = pd.read_excel(file)
    errores = []
    for _, row in df.iterrows():
        if Estudiante.query.filter_by(dni=row['dni']).first():
            errores.append(f"Duplicado: {row['dni']}")
            continue
        estudiante = Estudiante(
            nombre=row['nombre'],
            apellidos=row['apellidos'],
            pais=row['pais'],
            ciudad=row['ciudad'],
            senas_direccion=row['senas_direccion'],
            grado_academico=row['grado_academico'],
            dni=row['dni'],
            fecha_nacimiento=row['fecha_nacimiento'],
            correo=row['correo'],
            telefono=row['telefono'],
            anio_solicitud=row['anio_solicitud']
        )
        db.session.add(estudiante)
    db.session.commit()
    return errores
