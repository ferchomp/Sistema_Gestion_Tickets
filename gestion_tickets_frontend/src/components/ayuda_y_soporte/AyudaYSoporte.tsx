// Componente: AyudaYSoporte.tsx
// Descripción: Este componente se encarga de obtener y mostrar la lista de solicitudes de ayuda y soporte registradas en el sistema.

import React, { useEffect, useState } from "react";
import axios from "axios";

// Definición del componente AyudaYSoporte
const AyudaYSoporte: React.FC = () => {
  // Estado para almacenar la lista de tickets de ayuda y soporte
  const [ticketsAyuda, setTicketsAyuda] = useState<any[]>([]);

  // useEffect se ejecuta al montar el componente para obtener los tickets de ayuda desde la API
  useEffect(() => {
    const fetchTicketsAyuda = async () => {
      try {
        // Realiza una solicitud GET a la API para obtener la lista de tickets de ayuda
        const response = await axios.get("http://localhost:8000/ayuda_y_soporte/");
        setTicketsAyuda(response.data); // Almacena los tickets en el estado
      } catch (error) {
        console.error("Error al obtener tickets de ayuda", error); // Manejo de errores en la consola
      }
    };

    fetchTicketsAyuda(); // Llamada a la función de obtención de tickets de ayuda
  }, []); // Dependencias vacías para ejecutar el efecto solo una vez al montar el componente

  return (
    <div>
      <h2>Tickets de Ayuda y Soporte</h2>
      <ul>
        {/* Mapeo de los tickets obtenidos para mostrarlos en una lista */}
        {ticketsAyuda.map((ticket) => (
          <li key={ticket.ticket_id}>
            {ticket.ticket_id} - {ticket.estado_ticket} - {ticket.asignado}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AyudaYSoporte; // Exportación del componente para su uso en otras partes de la aplicación
