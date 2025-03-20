// Componente: Tickets.tsx
// Descripción: Este componente gestiona la creación y visualización de tickets en el sistema.

import React, { useEffect, useState } from "react";
import axios from "axios";

// Definición del componente Tickets
const Tickets: React.FC = () => {
  // Estado para almacenar la lista de tickets
  const [tickets, setTickets] = useState<any[]>([]);
  
  // Estado para manejar la creación de un nuevo ticket
  const [nuevoTicket, setNuevoTicket] = useState({ estado_ticket: "", asignado: "", solicitante: "" });

  // useEffect para obtener los tickets al montar el componente
  useEffect(() => {
    const fetchTickets = async () => {
      try {
        // Realiza una solicitud GET a la API para obtener la lista de tickets
        const response = await axios.get("http://localhost:8000/tickets/");
        setTickets(response.data); // Almacena los tickets en el estado
      } catch (error) {
        console.error("Error al obtener tickets", error); // Manejo de errores
      }
    };

    fetchTickets(); // Llamada a la función de obtención de tickets
  }, []);

  // Función para manejar la creación de un nuevo ticket
  const handleCrearTicket = async () => {
    try {
      const response = await axios.post("http://localhost:8000/tickets/create/", nuevoTicket);
      alert("Ticket creado: " + response.data.ticket_id);
      setTickets([...tickets, response.data]); // Agregar el nuevo ticket a la lista
    } catch (error) {
      console.error("Error creando ticket", error);
    }
  };

  return (
    <div>
      <h2>Tickets</h2>
      <div>
        {/* Campos de entrada para crear un nuevo ticket */}
        <input
          type="text"
          placeholder="Estado del Ticket"
          value={nuevoTicket.estado_ticket}
          onChange={(e) => setNuevoTicket({ ...nuevoTicket, estado_ticket: e.target.value })}
        />
        <input
          type="text"
          placeholder="Asignado"
          value={nuevoTicket.asignado}
          onChange={(e) => setNuevoTicket({ ...nuevoTicket, asignado: e.target.value })}
        />
        <input
          type="text"
          placeholder="Solicitante"
          value={nuevoTicket.solicitante}
          onChange={(e) => setNuevoTicket({ ...nuevoTicket, solicitante: e.target.value })}
        />
        <button onClick={handleCrearTicket}>Crear Ticket</button>
      </div>
      <ul>
        {/* Mapeo de los tickets obtenidos para mostrarlos en una lista */}
        {tickets.map((ticket) => (
          <li key={ticket.ticket_id}>
            {ticket.ticket_id} - {ticket.estado} - {ticket.asignado}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Tickets; // Exportación del componente para su uso en otras partes de la aplicación
