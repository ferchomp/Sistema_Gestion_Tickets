import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableHeader, TableBody, TableRow, TableCell } from "@/components/ui/table";
import { Download } from "lucide-react";
import "@/styles/Reportes.css"; // Asegúrate de que el archivo existe

interface Ticket {
  ticket_id: string;
  estado_ticket: string;
  asignado: string;
}

export default function ReporteTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [estado, setEstado] = useState("");
  const [asignado, setAsignado] = useState("");
  const [solicitante, setSolicitante] = useState("");

  const fetchReportes = async () => {
    try {
      let queryParams = new URLSearchParams();
      if (estado) queryParams.append("estado", estado);
      if (asignado) queryParams.append("asignado", asignado);
      if (solicitante) queryParams.append("solicitante", solicitante);
      
      const response = await fetch(`/reporte-tickets/?${queryParams.toString()}`);
      const data = await response.json();
      if (response.ok) {
        setTickets(data.tickets);
      } else {
        setTickets([]);
      }
    } catch (error) {
      console.error("Error al obtener reportes", error);
    }
  };

  const descargarExcel = async () => {
    let queryParams = new URLSearchParams();
    if (estado) queryParams.append("estado", estado);
    if (asignado) queryParams.append("asignado", asignado);
    if (solicitante) queryParams.append("solicitante", solicitante);
    
    window.location.href = `/exportar-reporte-tickets/?${queryParams.toString()}`;
  };

  useEffect(() => {
    fetchReportes();
  }, []);

  return (
    <div className="container">
      <div className="content">
        <h1 className="title">Reportes de Tickets</h1>
        <div className="filter-section">
          <Input 
            placeholder="Estado" 
            value={estado} 
            onChange={(e) => setEstado(e.target.value)} 
            className="input-field"
          />
          <Input 
            placeholder="Asignado" 
            value={asignado} 
            onChange={(e) => setAsignado(e.target.value)} 
            className="input-field"
          />
          <Input 
            placeholder="Solicitante" 
            value={solicitante} 
            onChange={(e) => setSolicitante(e.target.value)} 
            className="input-field"
          />
        </div>
          <div className="button-section">
          <Button onClick={fetchReportes} className="filter-button">
            Filtrar
          </Button>
          <Button onClick={descargarExcel} className="export-button">
            <Download className="icon" size={14} /> Exportar Excel
          </Button>
        </div>
        <Table className="table">
          <TableHeader>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Estado</TableCell>
              <TableCell>Asignado</TableCell>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tickets.length > 0 ? (
              tickets.map((ticket) => (
                <TableRow key={ticket.ticket_id}>
                  <TableCell>{ticket.ticket_id}</TableCell>
                  <TableCell>{ticket.estado_ticket}</TableCell>
                  <TableCell>{ticket.asignado}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} className="no-data">
                  No hay reportes disponibles
                </TableCell>
              </TableRow>
            )}
            </TableBody>
        </Table>
      </div>
    </div>
    
  );
}
