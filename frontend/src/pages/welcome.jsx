import { Link } from "react-router-dom";

export default function Welcome() {
  return (
    <div className="center-page">
      <div className="container">
        <h1>Bienvenido</h1>

        <div className="form-box">
          <Link to="/login">
            <button>Iniciar Sesión</button>
          </Link>

          <Link to="/register">
            <button style={{ background: "#2ecc71" }}>
              Registrarse
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
