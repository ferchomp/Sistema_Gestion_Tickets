// Archivo: api.ts
// Descripción: Configuración de la API y funciones para realizar solicitudes HTTP

import axios from "axios";

// Configuración base de Axios
const api = axios.create({
  baseURL: "http://localhost:8000", // Cambiar según el entorno de producción
  headers: {
    "Content-Type": "application/json",
  },
});

// Función para obtener la lista de usuarios
export const obtenerUsuarios = async () => {
  try {
    const response = await api.get("/usuarios/");
    return response.data;
  } catch (error) {
    console.error("Error al obtener usuarios", error);
    throw error;
  }
};

// Función para crear un nuevo usuario
export const crearUsuario = async (datosUsuario: { username: string; email: string; password: string }) => {
  try {
    const response = await api.post("/usuarios/", datosUsuario);
    return response.data;
  } catch (error) {
    console.error("Error al crear usuario", error);
    throw error;
  }
};

// Función para obtener la lista de tickets
export const obtenerTickets = async () => {
  try {
    const response = await api.get("/tickets/");
    return response.data;
  } catch (error) {
    console.error("Error al obtener tickets", error);
    throw error;
  }
};

// Función para crear un nuevo ticket
export const crearTicket = async (datosTicket: { estado: string; asignado: string; solicitante: string }) => {
  try {
    const response = await api.post("/tickets/create/", datosTicket);
    return response.data;
  } catch (error) {
    console.error("Error al crear ticket", error);
    throw error;
  }
};

// Función para consultar el saldo de un usuario
export const consultarSaldo = async (usuarioId: string) => {
  try {
    const response = await api.get(`/saldo/consultar/${usuarioId}`);
    return response.data;
  } catch (error) {
    console.error("Error al consultar saldo", error);
    throw error;
  }
};

// Función para comprar horas
export const comprarHoras = async (usuarioId: string, horasCompradas: number, precioPorHora: number) => {
  try {
    const response = await api.post(`/comprar_horas/comprar/${usuarioId}`, {
      horas_compradas: horasCompradas,
      precio_por_hora: precioPorHora,
    });
    return response.data;
  } catch (error) {
    console.error("Error al comprar horas", error);
    throw error;
  }
};

export default api; // Exportación de la instancia Axios para uso en otros archivos
