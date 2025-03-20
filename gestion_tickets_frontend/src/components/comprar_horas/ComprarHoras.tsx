// Componente: ComprarHoras.tsx
// Descripción: Este componente permite a un usuario comprar horas en el sistema.

import React, { useState } from "react";
import axios from "axios";

// Definición del componente ComprarHoras
const ComprarHoras: React.FC = () => {
  // Estado para manejar la entrada del ID del usuario
  const [usuarioId, setUsuarioId] = useState<string>("");
  // Estado para manejar la cantidad de horas compradas
  const [horasCompradas, setHorasCompradas] = useState<number>(0);
  // Estado para manejar el precio por hora
  const [precioPorHora, setPrecioPorHora] = useState<number>(0);
  // Estado para almacenar el monto total de la compra
  const [montoTotal, setMontoTotal] = useState<number | null>(null);

  // Función para realizar la compra de horas
  const handleComprarHoras = async () => {
    try {
      // Realiza una solicitud POST a la API para comprar horas
      const response = await axios.post(`http://localhost:8000/comprar_horas/comprar/${usuarioId}`, {
        horas_compradas: horasCompradas,
        precio_por_hora: precioPorHora,
      });
      setMontoTotal(response.data.monto_total); // Almacena el monto total en el estado
    } catch (error) {
      console.error("Error al comprar horas", error); // Manejo de errores
    }
  };

  return (
    <div>
      <h2>Comprar Horas</h2>
      {/* Campo de entrada para el ID del usuario */}
      <input
        type="text"
        placeholder="ID de Usuario"
        value={usuarioId}
        onChange={(e) => setUsuarioId(e.target.value)}
      />
      {/* Campo de entrada para la cantidad de horas compradas */}
      <input
        type="number"
        placeholder="Horas Compradas"
        value={horasCompradas}
        onChange={(e) => setHorasCompradas(Number(e.target.value))}
      />
      {/* Campo de entrada para el precio por hora */}
      <input
        type="number"
        placeholder="Precio por Hora"
        value={precioPorHora}
        onChange={(e) => setPrecioPorHora(Number(e.target.value))}
      />
      {/* Botón para realizar la compra */}
      <button onClick={handleComprarHoras}>Comprar</button>
      {/* Muestra el monto total si se ha realizado la compra */}
      {montoTotal !== null && <p>Monto Total: {montoTotal}</p>}
    </div>
  );
};

export default ComprarHoras; // Exportación del componente para su uso en otras partes de la aplicación
