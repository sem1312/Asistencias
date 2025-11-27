from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    tipo = db.Column(db.String(20), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.email}>"


class Estudiante(db.Model):
    __tablename__ = "estudiantes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)

    asistencias = db.relationship("Asistencia", backref="estudiante", lazy=True)

    def __repr__(self):
        return f"<Estudiante {self.nombre} - {self.curso}>"


class Asistencia(db.Model):
    __tablename__ = "asistencias"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiantes.id"), nullable=False)

    fecha = db.Column(db.Date, default=datetime.utcnow().date)
    presente = db.Column(db.Boolean, default=True)

    hora_entrada = db.Column(db.Time, nullable=True)
    hora_salida = db.Column(db.Time, nullable=True)

    observaciones = db.Column(db.String(255), nullable=True)
    justificacion = db.Column(db.String(255), nullable=True)

    tipo_asistencia = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Asistencia Est:{self.estudiante_id} Fecha:{self.fecha}>"
