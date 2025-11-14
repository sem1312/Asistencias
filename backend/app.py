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

# ------------------------------
# MODELOS
# ------------------------------
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    asistencias = db.relationship("Asistencia", backref="estudiante", lazy=True)

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiante.id"), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    presente = db.Column(db.Boolean, default=True)

# ------------------------------
# ENDPOINTS
# ------------------------------

@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([
        {"id": e.id, "nombre": e.nombre, "curso": e.curso}
        for e in estudiantes
    ])

@app.route('/api/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    nuevo = Estudiante(nombre=data['nombre'], curso=data['curso'])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"message": "Estudiante agregado"}), 201

@app.route('/api/asistencias', methods=['GET'])
def obtener_asistencias():
    asistencias = Asistencia.query.all()
    data = [
        {
            "id": a.id,
            "estudiante": a.estudiante.nombre,
            "curso": a.estudiante.curso,
            "fecha": a.fecha.strftime("%Y-%m-%d"),
            "presente": a.presente
        }
        for a in asistencias
    ]
    return jsonify(data)

@app.route('/api/asistencias', methods=['POST'])
def registrar_asistencia():
    data = request.get_json()
    estudiante_id = data.get("estudiante_id")
    presente = data.get("presente", True)
    fecha = datetime.strptime(data.get("fecha"), "%Y-%m-%d").date()

    nueva_asistencia = Asistencia(estudiante_id=estudiante_id, presente=presente, fecha=fecha)
    db.session.add(nueva_asistencia)
    db.session.commit()
    return jsonify({"message": "Asistencia registrada"}), 201

# ------------------------------
# RUN
# ------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
