// Archivo: main.tsx
// Descripción: Punto de entrada principal de la aplicación

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./Styles/index.css"; // Importar estilos globales

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
