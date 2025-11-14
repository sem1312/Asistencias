import { Link } from "react-router-dom";

export default function Welcome() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white px-6">
      <h1 className="text-4xl font-bold mb-8">Bienvenido</h1>

      <div className="flex flex-col gap-4 w-full max-w-sm">
        <Link
          to="/login"
          className="bg-blue-600 hover:bg-blue-500 text-white py-3 text-center rounded-lg text-lg font-semibold"
        >
          Iniciar Sesión
        </Link>

        <Link
          to="/register"
          className="bg-green-600 hover:bg-green-500 text-white py-3 text-center rounded-lg text-lg font-semibold"
        >
          Registrarse
        </Link>
      </div>
    </div>
  );
}
