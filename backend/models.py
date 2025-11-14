from app import db
from datetime import datetime

class Estudiante(db.Model):
    __tablename__ = "estudiantes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)

    # Relación correcta
    asistencias = db.relationship("Asistencia", backref="estudiante", lazy=True)

    def __repr__(self):
        return f"<Estudiante {self.nombre} - {self.curso}>"


class Asistencia(db.Model):
    __tablename__ = "asistencias"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiantes.id"), nullable=False)

    # Fecha (solo día)
    fecha = db.Column(db.Date, default=datetime.utcnow().date)

    # Presente / ausente
    presente = db.Column(db.Boolean, default=True)

    # Horarios opcionales
    hora_entrada = db.Column(db.Time, nullable=True)
    hora_salida = db.Column(db.Time, nullable=True)

    # Info adicional
    observaciones = db.Column(db.String(255), nullable=True)
    justificacion = db.Column(db.String(255), nullable=True)

    # Tipo de asistencia
    tipo_asistencia = db.Column(db.String(50), nullable=True)
    # Ejemplos:
    #   "presente"
    #   "tarde"
    #   "salida anticipada"
    #   "ausente justificado"
    #   "ausente injustificado"

    def __repr__(self):
        return f"<Asistencia Est:{self.estudiante_id} Fecha:{self.fecha}>"
