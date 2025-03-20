// Componente: Saldo.tsx
// Descripción: Este componente permite consultar el saldo de un usuario en el sistema.

import React, { useState } from "react";
import axios from "axios";

// Definición del componente Saldo
const Saldo: React.FC = () => {
  // Estado para manejar la entrada del ID del usuario
  const [usuarioId, setUsuarioId] = useState<string>("");
  // Estado para almacenar el saldo consultado
  const [saldo, setSaldo] = useState<number | null>(null);

  // Función para consultar el saldo del usuario
  const handleConsultarSaldo = async () => {
    try {
      // Realiza una solicitud GET a la API para obtener el saldo del usuario
      const response = await axios.get(`http://localhost:8000/saldo/consultar/${usuarioId}`);
      setSaldo(response.data.saldo_actual); // Almacena el saldo en el estado
    } catch (error) {
      console.error("Error al obtener el saldo", error); // Manejo de errores
    }
  };

  return (
    <div>
      <h2>Consultar Saldo</h2>
      {/* Campo de entrada para el ID del usuario */}
      <input
        type="text"
        placeholder="ID de Usuario"
        value={usuarioId}
        onChange={(e) => setUsuarioId(e.target.value)}
      />
      {/* Botón para consultar el saldo */}
      <button onClick={handleConsultarSaldo}>Consultar Saldo</button>
      {/* Muestra el saldo si se ha consultado */}
      {saldo !== null && <p>Saldo: {saldo}</p>}
    </div>
  );
};

export default Saldo; // Exportación del componente para su uso en otras partes de la aplicación
