import { useState } from "react";
import axios from "axios";
import "../styles/ComprarHoras.css";

const ComprarHoras = () => {
    const [usuarioId, setUsuarioId] = useState("");
    const [horasCompradas, setHorasCompradas] = useState<number>(0);
    const [precioPorHora, setPrecioPorHora] = useState<number>(0);
    const [mensaje, setMensaje] = useState<string>("");
    const [compras, setCompras] = useState<any[]>([]);

    const comprarHoras = async () => {
        if (!usuarioId || horasCompradas <= 0 || precioPorHora <= 0) {
            setMensaje("Ingrese valores válidos para la compra.");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:8000/comprar_horas/comprar/${usuarioId}/`, {
                horas_compradas: horasCompradas,
                precio_por_hora: precioPorHora,
            });

            setMensaje("Compra realizada con éxito.");
            setCompras([...compras, response.data]); // Agregar la nueva compra a la lista
        } catch (error: any) {
            setMensaje(error.response?.data?.error || "Error al comprar horas.");
        }
    };

    const consultarCompras = async () => {
        if (!usuarioId) {
            setMensaje("Ingrese un ID de usuario para consultar.");
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:8000/comprar_horas/consultar/${usuarioId}/`);
            setCompras(response.data.compras);
            setMensaje("");
        } catch (error: any) {
            setMensaje(error.response?.data?.error || "No se encontraron compras.");
            setCompras([]);
        }
    };

    return (
        <div className="comprar-horas-container">
            <h1>Compra de Horas</h1>

            <div className="input-group">
                <label>ID de Usuario:</label>
                <input
                    type="text"
                    value={usuarioId}
                    onChange={(e) => setUsuarioId(e.target.value)}
                    placeholder="Ingrese el ID del usuario"
                />
            </div>

            <div className="input-group">
                <label>Horas a Comprar:</label>
                <input
                    type="number"
                    value={horasCompradas}
                    onChange={(e) => setHorasCompradas(parseInt(e.target.value))}
                    placeholder="Ingrese cantidad de horas"
                />
            </div>

            <div className="input-group">
                <label>Precio por Hora:</label>
                <input
                    type="number"
                    value={precioPorHora}
                    onChange={(e) => setPrecioPorHora(parseFloat(e.target.value))}
                    placeholder="Ingrese el precio por hora"
                />
            </div>

            <button className="btn comprar" onClick={comprarHoras}>
                Comprar Horas
            </button>

            <button className="btn consultar" onClick={consultarCompras}>
                Consultar Compras
            </button>

            {mensaje && <p className="mensaje">{mensaje}</p>}

            {compras.length > 0 && (
                <div className="compras-lista">
                    <h3>Historial de Compras</h3>
                    <ul>
                        {compras.map((compra, index) => (
                            <li key={index}>
                                <span>{compra.horas_compradas} horas</span> - 
                                <span> ${compra.precio_por_hora} por hora</span> - 
                                <span> Total: ${compra.monto_total}</span> - 
                                <span> {compra.fecha_compra}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ComprarHoras;
