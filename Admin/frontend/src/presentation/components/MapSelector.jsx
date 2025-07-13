import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './MapSelector.css';

// Configurar iconos por defecto de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Componente para manejar clics en el mapa
const MapClickHandler = ({ onLocationSelect }) => {
  useMapEvents({
    click: async (event) => {
      const { lat, lng } = event.latlng;
      
      try {
        // Usar API de geocodificación inversa para obtener información del país
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=3&addressdetails=1`
        );
        const data = await response.json();
        
        const pais = data.address?.country || 'País no identificado';
        const ciudad = data.address?.city || data.address?.town || data.address?.village || '';
        const estado = data.address?.state || '';
        
        onLocationSelect({
          latitud: lat,
          longitud: lng,
          pais: pais,
          ubicacionCompleta: data.display_name || `${lat}, ${lng}`,
          ciudad: ciudad,
          estado: estado
        });
      } catch (error) {
        console.error('Error al obtener información de ubicación:', error);
        onLocationSelect({
          latitud: lat,
          longitud: lng,
          pais: 'País no identificado',
          ubicacionCompleta: `${lat}, ${lng}`,
          ciudad: '',
          estado: ''
        });
      }
    }
  });

  return null;
};

const MapSelector = ({ 
  onLocationSelect, 
  initialPosition = [20, 0], // Vista mundial centrada
  selectedPosition = null,
  height = "400px" 
}) => {
  const [position, setPosition] = useState(initialPosition);
  const [markerPosition, setMarkerPosition] = useState(selectedPosition);

  useEffect(() => {
    if (selectedPosition) {
      setMarkerPosition(selectedPosition);
      setPosition(selectedPosition);
    }
  }, [selectedPosition]);

  const handleLocationSelect = (locationData) => {
    const newPosition = [locationData.latitud, locationData.longitud];
    setMarkerPosition(newPosition);
    onLocationSelect(locationData);
  };

  return (
    <div className="map-selector">
      <div className="map-instructions">
        <p>🗺️ Haz clic en el mapa para seleccionar la ubicación del circuito</p>
        {markerPosition && (
          <div className="selected-location">
            <strong>Ubicación seleccionada:</strong>
            <br />
            📍 Coordenadas: {markerPosition[0].toFixed(6)}, {markerPosition[1].toFixed(6)}
          </div>
        )}
      </div>
      
      <div className="map-container" style={{ height }}>
        <MapContainer
          center={position}
          zoom={2} // Vista mundial
          style={{ height: '100%', width: '100%' }}
          scrollWheelZoom={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          <MapClickHandler onLocationSelect={handleLocationSelect} />
          
          {markerPosition && (
            <Marker position={markerPosition} />
          )}
        </MapContainer>
      </div>
      
      <div className="map-controls">
        <button 
          type="button" 
          className="btn-clear-location"
          onClick={() => {
            setMarkerPosition(null);
            onLocationSelect({
              latitud: '',
              longitud: '',
              pais: '',
              ubicacionCompleta: '',
              ciudad: '',
              estado: ''
            });
          }}
        >
          Limpiar Selección
        </button>
      </div>
    </div>
  );
};

export default MapSelector;
