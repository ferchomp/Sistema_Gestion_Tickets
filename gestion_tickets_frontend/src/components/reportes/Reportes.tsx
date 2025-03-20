// Componente: Reportes.tsx
// Descripción: Este componente obtiene y muestra los reportes generados del sistema de tickets.

import React, { useEffect, useState } from "react";
import axios from "axios";

// Definición del componente Reportes
const Reportes: React.FC = () => {
  // Estado para almacenar la lista de reportes
  const [reportes, setReportes] = useState<any[]>([]);

  // useEffect para obtener los reportes al montar el componente
  useEffect(() => {
    const fetchReportes = async () => {
      try {
        // Realiza una solicitud GET a la API para obtener la lista de reportes
        const response = await axios.get("http://localhost:8000/reportes/");
        setReportes(response.data); // Almacena los reportes en el estado
      } catch (error) {
        console.error("Error al obtener reportes", error); // Manejo de errores
      }
    };

    fetchReportes(); // Llamada a la función de obtención de reportes
  }, []); // Se ejecuta solo una vez al montar el componente

  return (
    <div>
      <h2>Reportes del Sistema</h2>
      <ul>
        {/* Mapeo de los reportes obtenidos para mostrarlos en una lista */}
        {reportes.map((reporte) => (
          <li key={reporte.id}>
            Reporte ID: {reporte.id} - {reporte.descripcion}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Reportes; // Exportación del componente para su uso en otras partes de la aplicación
