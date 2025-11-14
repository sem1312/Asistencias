import { useState, useEffect } from "react";

export default function AsistenciasForm({ onSubmit }) {
  const [estudiantes, setEstudiantes] = useState([]);
  const [form, setForm] = useState({
    estudiante_id: "",
    fecha: "",
    presente: true,
  });

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/estudiantes")
      .then((res) => res.json())
      .then((data) => setEstudiantes(data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
    setForm({ estudiante_id: "", fecha: "", presente: true });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 max-w-md">
      <select
        value={form.estudiante_id}
        onChange={(e) => setForm({ ...form, estudiante_id: e.target.value })}
        required
      >
        <option value="">Seleccionar estudiante</option>
        {estudiantes.map((e) => (
          <option key={e.id} value={e.id}>
            {e.nombre} ({e.curso})
          </option>
        ))}
      </select>

      <input
        type="date"
        value={form.fecha}
        onChange={(e) => setForm({ ...form, fecha: e.target.value })}
        required
      />

      <label>
        <input
          type="checkbox"
          checked={form.presente}
          onChange={(e) => setForm({ ...form, presente: e.target.checked })}
        />{" "}
        Presente
      </label>

      <button type="submit" className="bg-blue-600 text-white py-2 rounded">
        Registrar Asistencia
      </button>
    </form>
  );
}
