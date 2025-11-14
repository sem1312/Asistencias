export default function TablaAsistencias({ asistencias }) {
  return (
    <table className="w-full border mt-4">
      <thead className="bg-gray-200">
        <tr>
          <th>Estudiante</th>
          <th>Curso</th>
          <th>Fecha</th>
          <th>Presente</th>
        </tr>
      </thead>
      <tbody>
        {asistencias.map((a) => (
          <tr key={a.id} className="text-center border-b">
            <td>{a.estudiante}</td>
            <td>{a.curso}</td>
            <td>{a.fecha}</td>
            <td>{a.presente ? "✅" : "❌"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
