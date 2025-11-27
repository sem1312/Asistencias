from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Usuario, Estudiante, Asistencia

app = Flask(__name__)
CORS(app)

auth = Blueprint("auth", __name__)


# Config DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ==========================
# ENDPOINTS ESTUDIANTES
# ==========================

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

# ==========================
# ENDPOINT ASISTENCIAS
# ==========================

@app.route('/api/asistencias', methods=['POST'])
def registrar_asistencia():
    data = request.get_json()

    estudiante_id = data["estudiante_id"]
    presente = data.get("presente", True)

    try:
        fecha = datetime.strptime(data.get("fecha"), "%Y-%m-%d").date()
    except:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    hora_entrada = data.get("hora_entrada")
    hora_salida = data.get("hora_salida")

    nueva = Asistencia(
        estudiante_id=estudiante_id,
        fecha=fecha,
        presente=presente,
        tipo_asistencia=data.get("tipo_asistencia"),
        observaciones=data.get("observaciones"),
        justificacion=data.get("justificacion"),
        hora_entrada=datetime.strptime(hora_entrada, "%H:%M").time() if hora_entrada else None,
        hora_salida=datetime.strptime(hora_salida, "%H:%M").time() if hora_salida else None
    )

    db.session.add(nueva)
    db.session.commit()

    return jsonify({"message": "Asistencia registrada"}), 201


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


@app.route('/api/asistencias/<fecha>', methods=['GET'])
def obtener_asistencias_por_fecha(fecha):
    try:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        return jsonify({"error": "Formato inválido"}), 400

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
# REGISTER + LOGIN
# ==========================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")
    tipo = data.get("tipo")

    if not all([nombre, email, password, tipo]):
        return jsonify({"error": "Faltan datos"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    nuevo = Usuario(
        nombre=nombre,
        email=email,
        tipo=tipo,
        password_hash=generate_password_hash(password)
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"message": "Usuario creado"})


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not check_password_hash(usuario.password_hash, password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    return jsonify({
        "message": "Login exitoso",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "tipo": usuario.tipo
        }
    })

app.register_blueprint(auth)

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
