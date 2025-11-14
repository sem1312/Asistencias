from app import db
from datetime import datetime

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)

    inasistencias = db.relationship("Asistencia", backref="estudiante", lazy=True)

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiante.id"), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    presente = db.Column(db.Boolean, default=True)
    hora_entrada = db.Column(db.Time, nullable=True)
    hora_salida = db.Column(db.Time, nullable=True)
    observaciones = db.Column(db.String(255), nullable=True)
    justificacion = db.Column(db.String(255), nullable=True)
    tipo_asistencia = db.Column(db.String(50), nullable=True)  # e.g., "tarde", "salida anticipada"