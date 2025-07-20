import React, { useState } from 'react';
import ReactMap from './ReactMap';
import './MapSelector.css'; // Reutilizamos los estilos

// Componente de ejemplo que muestra cómo usar el ReactMap
const MapSelectorExample = () => {
  const [locationData, setLocationData] = useState({
    latitud: '',
    longitud: '',
    pais: '',
    ciudad: '',
    estado: '',
    ubicacionCompleta: ''
  });
  
  const handleLocationSelect = (data) => {
    setLocationData(data);
    console.log('Ubicación seleccionada:', data);
  };
  
  return (
    <div className="map-selector-example">
      <h2>Seleccionar Ubicación (Con React Hooks)</h2>
      
      <ReactMap 
        onLocationSelect={handleLocationSelect}
        height="600px"
        initialPosition={[20, 0]}
        selectedPosition={locationData.latitud && locationData.longitud ? [locationData.latitud, locationData.longitud] : null}
      />
      
      {locationData.ubicacionCompleta && (
        <div className="location-details">
          <h3>Ubicación Seleccionada:</h3>
          <p><strong>País:</strong> {locationData.pais}</p>
          {locationData.ciudad && <p><strong>Ciudad:</strong> {locationData.ciudad}</p>}
          {locationData.estado && <p><strong>Estado/Provincia:</strong> {locationData.estado}</p>}
          <p><strong>Coordenadas:</strong> {locationData.latitud}, {locationData.longitud}</p>
          <p><strong>Dirección completa:</strong> {locationData.ubicacionCompleta}</p>
        </div>
      )}
    </div>
  );
};

export default MapSelectorExample;
