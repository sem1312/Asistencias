import { useState, useEffect } from "react";

export default function AsistenciasForm({ onSubmit }) {
  const [estudiantes, setEstudiantes] = useState([]);
  const [asistencias, setAsistencias] = useState({});
  const [cursoSeleccionado, setCursoSeleccionado] = useState("");

  // FECHA AUTOMÁTICA (hoy)
  const fechaHoy = new Date().toISOString().split("T")[0];

  // Cargar estudiantes del backend
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/estudiantes")
      .then((res) => res.json())
      .then((data) => {
        setEstudiantes(data);

        const estadoInicial = {};
        data.forEach((e) => (estadoInicial[e.id] = true));
        setAsistencias(estadoInicial);
      });
  }, []);

  const togglePresente = (id) => {
    setAsistencias({ ...asistencias, [id]: !asistencias[id] });
  };

  // Filtrar por curso
  const estudiantesFiltrados = cursoSeleccionado
    ? estudiantes.filter((e) => e.curso === cursoSeleccionado)
    : [];

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = estudiantesFiltrados.map((e) => ({
      estudiante_id: e.id,
      fecha: fechaHoy,
      presente: asistencias[e.id],
    }));

    onSubmit(payload);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-6 w-full max-w-4xl mx-auto p-6 bg-gray-900 rounded-xl text-white"
    >
      {/* TITULO */}
      <h2 className="text-2xl font-bold">
        Asistencias del <span className="text-blue-400">{fechaHoy}</span>
      </h2>

      {/* SELECT CURSO */}
      <div className="flex gap-4 items-center">
        <label className="text-lg">Curso:</label>
        <select
          value={cursoSeleccionado}
          onChange={(e) => setCursoSeleccionado(e.target.value)}
          className="bg-black text-white p-2 rounded border border-gray-600"
        >
          <option value="">Seleccionar curso…</option>
          <option value="7P">7P</option>
          <option value="7A">7A</option>
          <option value="7B">7B</option>
        </select>
      </div>

      {/* MOSTRAR TABLA SOLO SI SELECCIONÓ CURSO */}
      {cursoSeleccionado !== "" && (
        <>
          <h3 className="text-xl font-semibold">
            Lista de estudiantes – {cursoSeleccionado}
          </h3>

          <table className="w-full text-white border border-gray-700">
            <thead className="bg-gray-800">
              <tr>
                <th className="p-2 border border-gray-700">Estudiante</th>
                <th className="p-2 border border-gray-700">Curso</th>
                <th className="p-2 border border-gray-700">Fecha</th>
                <th className="p-2 border border-gray-700">Presente</th>
              </tr>
            </thead>

            <tbody>
              {estudiantesFiltrados.map((e) => (
                <tr key={e.id} className="bg-gray-900">
                  <td className="p-2 border border-gray-700">{e.nombre}</td>
                  <td className="p-2 border border-gray-700">{e.curso}</td>
                  <td className="p-2 border border-gray-700">{fechaHoy}</td>
                  <td className="p-2 border border-gray-700 text-center">
                    <input
                      type="checkbox"
                      checked={asistencias[e.id]}
                      onChange={() => togglePresente(e.id)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <button
            type="submit"
            className="bg-blue-600 text-white py-2 mt-4 rounded-lg font-semibold hover:bg-blue-500"
          >
            Guardar Asistencias
          </button>
        </>
      )}
    </form>
  );
}
