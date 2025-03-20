// Componente: ObtenerUsuarios.tsx
// Descripción: Este componente se encarga de obtener y mostrar la lista de usuarios registrados en el sistema.

import React, { useEffect, useState } from "react";
import axios from "axios";

// Definición del componente ObtenerUsuarios
const ObtenerUsuarios: React.FC = () => {
  // Estado para almacenar la lista de usuarios
  const [usuarios, setUsuarios] = useState<any[]>([]);

  // useEffect se ejecuta al montar el componente para obtener los usuarios desde la API
  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        // Realiza una solicitud GET a la API para obtener la lista de usuarios
        const response = await axios.get("http://localhost:8000/usuarios/");
        setUsuarios(response.data); // Almacena los usuarios en el estado
      } catch (error) {
        console.error("Error al obtener usuarios", error); // Manejo de errores en la consola
      }
    };

    fetchUsuarios(); // Llamada a la función de obtención de usuarios
  }, []); // Dependencias vacías para ejecutar el efecto solo una vez al montar el componente

  return (
    <div>
      <h2>Lista de Usuarios</h2>
      <ul>
        {/* Mapeo de los usuarios obtenidos para mostrarlos en una lista */}
        {usuarios.map((usuario) => (
          <li key={usuario.id}>{usuario.username} - {usuario.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default ObtenerUsuarios; // Exportación del componente para su uso en otras partes de la aplicación
