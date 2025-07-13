import React, { useState, useEffect } from "react";  
import { useNavigate } from "react-router-dom";
import './EstadoApi.css'
import { verificarEstadoApi } from '../../shared/config/api';

const EstadoApi = () => {
  const navigate = useNavigate();
  const [estadoApi, setEstadoApi] = useState({
    conectado: null,
    cargando: true,
    ultimaVerificacion: null,
    detalles: null,
    mensaje: 'Iniciando verificación...'
  });

  const verificarConexionApi = async () => {
    setEstadoApi(prev => ({ 
      ...prev, 
      cargando: true, 
      mensaje: 'Verificando conexión...' 
    }));
    
    try {
      const resultado = await verificarEstadoApi();
      
      if (resultado.success) {
        setEstadoApi({
          conectado: true,
          cargando: false,
          ultimaVerificacion: new Date().toLocaleTimeString(),
          detalles: resultado.data,
          mensaje: resultado.message
        });
      } else {
        setEstadoApi({
          conectado: false,
          cargando: false,
          ultimaVerificacion: new Date().toLocaleTimeString(),
          detalles: null,
          mensaje: resultado.message
        });
      }
    } catch (error) {
      setEstadoApi({
        conectado: false,
        cargando: false,
        ultimaVerificacion: new Date().toLocaleTimeString(),
        detalles: null,
        mensaje: 'Error inesperado al conectar'
      });
    }
  };

  useEffect(() => {
    verificarConexionApi();
  }, []);

  const obtenerEstilo = () => {
    if (estadoApi.cargando) return 'estado-cargando';
    return estadoApi.conectado ? 'estado-conectado' : 'estado-desconectado';
  };

  const obtenerIcono = () => {
    if (estadoApi.cargando) return '⏳';
    return estadoApi.conectado ? '✅' : '❌';
  };

  const obtenerMensaje = () => {
    if (estadoApi.cargando) return 'Verificando conexión...';
    return estadoApi.mensaje || (estadoApi.conectado ? 'API Conectada' : 'API Desconectada');
  };

  return (
    <div className={`estado-api-card ${obtenerEstilo()}`}>
      <div className="estado-api-header">
        <span className="estado-api-icono">{obtenerIcono()}</span>
        <h3 className="estado-api-titulo">Estado de la API</h3>
      </div>
      
      <div className="estado-api-contenido">
        <p className="estado-api-mensaje">{obtenerMensaje()}</p>
        
        {estadoApi.conectado && estadoApi.detalles && (
          <div className="api-detalles">
            <p><strong>API:</strong> {estadoApi.detalles.mensaje}</p>
            <p><strong>Versión:</strong> {estadoApi.detalles.version}</p>
          </div>
        )}
        
        {estadoApi.ultimaVerificacion && (
          <p className="estado-api-tiempo">
            Última verificación: {estadoApi.ultimaVerificacion}
          </p>
        )}
        
        <button 
          className="estado-api-boton"
          onClick={verificarConexionApi}
          disabled={estadoApi.cargando}
        >
          {estadoApi.cargando ? 'Verificando...' : 'Verificar Conexión'}
        </button>
        
        {estadoApi.conectado && (
          <button 
            className="estado-api-boton editar-api-boton"
            onClick={() => navigate('/edit-api')}
          >
            Editar API
          </button>
        )}
      </div>
    </div>
  );
};

export default EstadoApi;


