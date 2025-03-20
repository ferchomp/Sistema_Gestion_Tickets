import React, { useState } from "react";
import { crearUsuario } from "../../services/api";

const CrearUsuario: React.FC = () => {
  // Estados para los campos del formulario
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Función para manejar la creación del usuario
  const handleCrearUsuario = async () => {
    if (!username || !email || !password) {
      alert("Por favor, completa todos los campos.");
      return;
    }

    try {
      const nuevoUsuario = await crearUsuario({ username, email, password });
      alert(`Usuario creado: ${nuevoUsuario.username}`);
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (error) {
      console.error("Error creando usuario", error);
      alert("Hubo un error al crear el usuario. Revisa la consola.");
    }
  };

  return (
    <div>
      <h2>Crear Usuario</h2>
      <input
        type="text"
        placeholder="Nombre de usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleCrearUsuario}>Crear Usuario</button>
    </div>
  );
};

export default CrearUsuario;
