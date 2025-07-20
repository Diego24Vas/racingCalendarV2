import React, { useState, useEffect } from "react";  
import './EstadoApi.css'
import { verificarEstadoApi } from '../../shared/config/api';

const EstadoApi = () => {
  const [estadoApi, setEstadoApi] = useState({
    conectado: null,
    cargando: true
  });

  const verificarConexionApi = async () => {
    setEstadoApi(prev => ({ 
      ...prev, 
      cargando: true
    }));
    
    try {
      const resultado = await verificarEstadoApi();
      
      setEstadoApi({
        conectado: resultado.success,
        cargando: false
      });
    } catch (error) {
      setEstadoApi({
        conectado: false,
        cargando: false
      });
    }
  };

  useEffect(() => {
    verificarConexionApi();
  }, []);

  const obtenerMensaje = () => {
    if (estadoApi.cargando) return 'Verificando conexión...';
    return estadoApi.conectado ? 'Conectado' : 'Desconectado';
  };

  return (
    <div className="estado-api-container">
      <div className="estado-api-card">
        <div className="estado-api-content">
          <div className={`estado-circulo ${estadoApi.cargando ? 'cargando' : estadoApi.conectado ? 'conectado' : 'desconectado'}`}>
            {estadoApi.cargando && <div className="spinner"></div>}
          </div>
          <div className="estado-texto">
            <p className="estado-mensaje">{obtenerMensaje()}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EstadoApi;


