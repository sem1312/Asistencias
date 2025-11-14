from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Config DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# MODELOS
# ==========================
class Estudiante(db.Model):
    __tablename__ = "estudiantes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)

    asistencias = db.relationship("Asistencia", backref="estudiante", lazy=True)


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

# ==========================
# ENDPOINTS
# ==========================

# Obtener todos los estudiantes
@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([
        {
            "id": e.id,
            "nombre": e.nombre,
            "curso": e.curso
        }
        for e in estudiantes
    ])


# Agregar estudiante
@app.route('/api/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    nuevo = Estudiante(
        nombre=data.get("nombre"),
        curso=data.get("curso")
    )
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"message": "Estudiante agregado correctamente"}), 201


# Registrar asistencia del día
@app.route('/api/asistencias', methods=['POST'])
def registrar_asistencia():
    data = request.get_json()

    estudiante_id = data["estudiante_id"]
    presente = data.get("presente", True)

    fecha = datetime.strptime(data.get("fecha"), "%Y-%m-%d").date()

    hora_entrada = data.get("hora_entrada")
    hora_salida = data.get("hora_salida")

    nueva_asistencia = Asistencia(
        estudiante_id=estudiante_id,
        fecha=fecha,
        presente=presente,
        tipo_asistencia=data.get("tipo_asistencia"),
        observaciones=data.get("observaciones"),
        justificacion=data.get("justificacion"),
        hora_entrada=datetime.strptime(hora_entrada, "%H:%M").time() if hora_entrada else None,
        hora_salida=datetime.strptime(hora_salida, "%H:%M").time() if hora_salida else None
    )

    db.session.add(nueva_asistencia)
    db.session.commit()

    return jsonify({"message": "Asistencia registrada"}), 201


# Obtener TODAS las asistencias
@app.route('/api/asistencias', methods=['GET'])
def obtener_asistencias():
    asistencias = Asistencia.query.all()

    return jsonify([
        {
            "id": a.id,
            "estudiante_id": a.estudiante_id,
            "estudiante": a.estudiante.nombre,
            "curso": a.estudiante.curso,
            "fecha": a.fecha.strftime("%Y-%m-%d"),
            "presente": a.presente,
            "tipo_asistencia": a.tipo_asistencia,
            "hora_entrada": a.hora_entrada.strftime("%H:%M") if a.hora_entrada else None,
            "hora_salida": a.hora_salida.strftime("%H:%M") if a.hora_salida else None,
            "observaciones": a.observaciones,
            "justificacion": a.justificacion
        }
        for a in asistencias
    ])


# Obtener asistencias por fecha
@app.route('/api/asistencias/<fecha>', methods=['GET'])
def obtener_asistencias_por_fecha(fecha):
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    asistencias = Asistencia.query.filter_by(fecha=fecha_dt).all()

    return jsonify([
        {
            "id": a.id,
            "estudiante_id": a.estudiante_id,
            "estudiante": a.estudiante.nombre,
            "curso": a.estudiante.curso,
            "fecha": a.fecha.strftime("%Y-%m-%d"),
            "presente": a.presente,
            "tipo_asistencia": a.tipo_asistencia,
            "hora_entrada": a.hora_entrada.strftime("%H:%M") if a.hora_entrada else None,
            "hora_salida": a.hora_salida.strftime("%H:%M") if a.hora_salida else None,
            "observaciones": a.observaciones,
            "justificacion": a.justificacion
        }
        for a in asistencias
    ])


# ==========================
# RUN SERVER
# ==========================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # ---- CARGA INICIAL DE ESTUDIANTES ----
        if Estudiante.query.count() == 0:
            alumnos = [
                Estudiante(nombre="Patricio Gallo Dillon", curso="7P"),
                Estudiante(nombre="Fabricio Fernando Silveyra", curso="7P"),
                Estudiante(nombre="Lautaro Cuesta", curso="7P"),
                Estudiante(nombre="Ismael Medrano", curso="7P"),
            ]
            db.session.add_all(alumnos)
            db.session.commit()
            print("✔ Estudiantes cargados exitosamente")
        else:
            print("✔ Estudiantes ya existen (no se vuelven a cargar)")

    app.run(debug=True)
