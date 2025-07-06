import React from "react";
import EstadoApi from "../components/EstadoApi";
import "./ApiPage.css";

const ApiPage = () => {
    return (
        <div className="api-page">
            <div className="api-page-header">
                <h1>Estado de la API</h1>
                <p>Monitoreo de la conexión con el backend</p>
            </div>
            <EstadoApi />
            <button className="boton-edit-api">
              Editar API
            </button>
        </div>
    )
}

export default ApiPage

