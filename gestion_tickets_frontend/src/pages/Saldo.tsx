import { useState } from "react";
import axios from "axios";
import "../styles/Saldo.css";

const Saldo = () => {
    const [usuarioId, setUsuarioId] = useState("");
    const [saldo, setSaldo] = useState<number | null>(null);
    const [cambioSaldo, setCambioSaldo] = useState<number>(0);
    const [mensaje, setMensaje] = useState<string>("");

    const consultarSaldo = async () => {
        if (!usuarioId) {
            setMensaje("Por favor, ingresa un ID de usuario.");
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:8000/saldo/consultar/${usuarioId}/`);
            setSaldo(response.data.saldo_actual);
            setMensaje("");
        } catch (error: any) {
            setMensaje(error.response?.data?.error || "Error al consultar saldo.");
        }
    };

    const actualizarSaldo = async () => {
        if (!usuarioId || cambioSaldo === 0) {
            setMensaje("Ingrese un ID de usuario y un monto válido.");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:8000/saldo/actualizar/${usuarioId}/`, {
                cambio_saldo: cambioSaldo,
            });
            setSaldo(response.data.nuevo_saldo);
            setMensaje("Saldo actualizado correctamente.");
        } catch (error: any) {
            setMensaje(error.response?.data?.error || "Error al actualizar saldo.");
        }
    };

    return (
        <div className="saldo-container">
            <h2>Gestión de Saldo</h2>
            <div className="input-group">
                <label>ID de Usuario:</label>
                <input
                    type="text"
                    value={usuarioId}
                    onChange={(e) => setUsuarioId(e.target.value)}
                    placeholder="Ingrese el ID del usuario"
                />
            </div>

            <div className="saldo-info">
                <button className="btn consultar" onClick={consultarSaldo}>
                    Consultar Saldo
                </button>
                {saldo !== null && <p>Saldo Actual: ${saldo}</p>}
            </div>

            <div className="input-group">
                <label>Cambio de Saldo:</label>
                <input
                    type="number"
                    value={cambioSaldo}
                    onChange={(e) => setCambioSaldo(parseFloat(e.target.value))}
                    placeholder="Ingrese el monto a modificar"
                />
            </div>

            <button className="btn actualizar" onClick={actualizarSaldo}>
                Actualizar Saldo
            </button>

            {mensaje && <p className="mensaje">{mensaje}</p>}
        </div>
    );
};

export default Saldo;
