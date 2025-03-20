import React, { useState, useEffect } from "react";
import "../Styles/Tickets.css";
import { FaChevronLeft, } from "react-icons/fa";


// 🔹 Definir la interfaz para que TypeScript reconozca los datos correctamente
interface FormDataType {
  asignado: string;
  solicitante: string;
  departamento: string;
  fecha_creacion: string;
  asunto: string;
  descripcion: string;
  tipo_ticket: string;
  estado_ticket: string;
  prioridad: string;
  fecha_resolucion: string;
  archivo: File | null;
}

const Tickets: React.FC = () => {
  const [usuarios, setUsuarios] = useState<any[]>([]);
  const [departamentos, setDepartamentos] = useState<any[]>([]);
  const [mensaje, setMensaje] = useState<string | null>(null);

  // 🔹 Estado del formulario con el tipo correcto
  const [formData, setFormData] = useState<FormDataType>({
    asignado: "",
    solicitante: "",
    departamento: "",
    fecha_creacion: "",
    asunto: "",
    descripcion: "",
    tipo_ticket: "",
    estado_ticket: "",
    prioridad: "",
    fecha_resolucion:"",
    archivo: null,
  });

  useEffect(() => {
    // 🔹 Cargar usuarios
    fetch("http://localhost:8000/usuarios/usuarios/")
      .then((res) => res.json())
      .then((data) => {
        console.log("✅ Usuarios cargados:", data);
        setUsuarios(Array.isArray(data) ? data : []);
      })
      .catch((error) => console.error("❌ Error al obtener usuarios:", error));

    // 🔹 Cargar departamentos
    fetch("http://localhost:8000/departamentos/")
      .then((res) => res.json())
      .then((data) => {
        console.log("✅ Departamentos cargados:", data);
        setDepartamentos(Array.isArray(data) ? data : []);
      })
      .catch((error) => console.error("❌ Error al obtener departamentos:", error));
  }, []);

  // 🔹 Manejo de cambios en los inputs
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 🔹 Manejo de archivo adjunto
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;
    setFormData({ ...formData, archivo: file });
  };

  // 🔹 Enviar formulario
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMensaje(null);

    const formDataToSend = new FormData();
Object.entries(formData).forEach(([key, value]) => {
  if (value !== null && value !== "" && key !== "archivo") {
    formDataToSend.append(key, value as string | Blob);
  }
});

// ✅ Si no se seleccionó una prioridad, asigna un valor predeterminado
if (!formData.prioridad) {
  formDataToSend.append("prioridad", "Media");  // Puedes cambiar "Media" por otro valor por defecto
}

if (formData.archivo) {
  formDataToSend.append("archivo", formData.archivo);
}


    console.log("📤 Enviando datos:", [...formDataToSend.entries()]);

    try {
      const response = await fetch("http://localhost:8000/tickets/create/", {
        method: "POST",
        body: formDataToSend,
      });

      const result = await response.json();
      console.log("📥 Respuesta del servidor:", response.status, result);

      if (response.ok) {
        setMensaje("✅ ¡Ticket creado con éxito!");
        setFormData({
          asignado: "",
          solicitante: "",
          departamento: "",
          fecha_creacion: "", 
          asunto: "",
          descripcion: "",
          tipo_ticket: "",
          estado_ticket: "",
          prioridad: "",
          fecha_resolucion:"",
          archivo: null,
        });
      } else {
        console.error("❌ Error en respuesta:", result);
        setMensaje(`❌ Error: ${result.error || "No se pudo crear el ticket"}`);
      }
    } catch (error) {
      console.error("❌ Error al enviar ticket:", error);
      setMensaje("❌ Error de conexión con el servidor.");
    }
  };

  return (
    <div className="ticket-container">
      <h2>Creación De Tickets</h2>
      {mensaje && <p className="mensaje">{mensaje}</p>}
      <form className="ticket-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="input-group">
            <label>Asignado a:</label>
            <select name="asignado" onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              {usuarios.map((user) => (
                <option key={user.id} value={user.username}>{user.username}</option>
              ))}
            </select>
          </div>
          <div className="input-group">
            <label>Solicitante:</label>
            <select name="solicitante" onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              {usuarios.map((user) => (
                <option key={user.id} value={user.username}>{user.username}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="input-group">
            <label>Departamento:</label>
            <select name="departamento" onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              {departamentos.map((dep) => (
                <option key={dep.id} value={dep.nombre}>{dep.nombre}</option>
              ))}
            </select>
          </div>
          <div className="input-group">
            <label>Fecha de Creación:</label>
            <input type="date" name="fecha_creacion" value={formData.fecha_creacion} onChange={handleChange} required />
          </div>
        </div>

        <div className="input-group">
          <label>Asunto:</label>
          <input type="text" name="asunto" value={formData.asunto} onChange={handleChange} required />
        </div>
        <div className="input-group">
          <label>Descripción:</label>
          <textarea name="descripcion" value={formData.descripcion} onChange={handleChange} required></textarea>
          </div>

        <div className="form-row">
          <div className="input-group">
            <label>Tipo de Ticket:</label>
            <select name="tipo_ticket" onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              <option value="Problema">Problema</option>
              <option value="Solicitud de Servicio">Solicitud de Servicio</option>
              <option value="Consulta">Consulta</option>
              <option value="Incidente">Incidente</option>
            </select>
          </div>
          <div className="input-group">
            <label>Estado del Ticket:</label>
            <select name="estado_ticket" onChange={handleChange} required>
              <option value="">Selecciona una opción</option>
              <option value="Abierto">Abierto</option>
              <option value="En Proceso">En Proceso</option>
              <option value="Cerrado">Cerrado</option>
            </select>
          </div>
        </div>

        <div className="input-group">
          <label>Adjuntar Archivo:</label>
          <input type="file" onChange={handleFileChange} />
        </div>

        <div className="ayuda-icons">
        <a href="/panel" className="ayuda-icon-button ayuda-icon-back">
         <FaChevronLeft size={20} />
        </a>
        <button type="submit" className="ticket-button">Crear Ticket</button>
        </div>
      </form>
    </div>
  );
};

export default Tickets;
