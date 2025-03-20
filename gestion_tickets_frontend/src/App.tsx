import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Panel from "./pages/Panel";
import Tickets from "./pages/Tickets";
import Ayuda from "./pages/Ayuda";
import Reportes from "./pages/Reportes";
import Saldo from "./pages/Saldo";
import ComprarHoras from "./pages/ComprarHoras";
import "./styles/App.css";

// Función para verificar si el usuario está autenticado
const isAuthenticated = () => {
  return localStorage.getItem("token") !== null;
};

const ProtectedRoute: React.FC<{ element: JSX.Element }> = ({ element }) => {
  return isAuthenticated() ? element : <Navigate to="/" />;
};

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/panel" element={<ProtectedRoute element={<Panel />} />} />
        <Route path="/tickets" element={<ProtectedRoute element={<Tickets />} />} />
        <Route path="/ayuda" element={<ProtectedRoute element={<Ayuda />} />} />
        <Route path="/reportes" element={<ProtectedRoute element={<Reportes />} />} />
        <Route path="/saldo" element={<ProtectedRoute element={<Saldo />} />} />
        <Route path="/comprar-horas" element={<ProtectedRoute element={<ComprarHoras />} />} />
      </Routes>
    </Router>
  );
};

export default App;
