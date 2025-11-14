import { useState, useEffect } from "react";
import TablaAsistencias from "../components/TablaAsistencias";
import AsistenciasForm from "../components/AsistenciasForm";

export default function Home() {
  const [asistencias, setAsistencias] = useState([]);

  const cargarAsistencias = () => {
    fetch("http://127.0.0.1:5000/api/asistencias")
      .then((res) => res.json())
      .then((data) => setAsistencias(data));
  };

  useEffect(() => {
    cargarAsistencias();
  }, []);

const registrarAsistencia = async (lista) => {
  for (const a of lista) {
    await fetch("http://127.0.0.1:5000/api/asistencias", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(a),
    });
  }
  cargarAsistencias();
};



  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Registro de Asistencias</h2>
      <AsistenciasForm onSubmit={registrarAsistencia} />
    </div>
  );
}
