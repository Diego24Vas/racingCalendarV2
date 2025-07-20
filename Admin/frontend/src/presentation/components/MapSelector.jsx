import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './MapSelector.css';
import './LeafletFix.css'; // Importar arreglos específicos para Leaflet
import { reinitializeLeaflet, isLeafletReady } from './LeafletUtils';

// Configurar iconos por defecto de Leaflet
delete L.Icon.Default.prototype._getIconUrl;

// Utilizar un enfoque más directo para configurar los iconos
const DefaultIcon = L.icon({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

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

// Componente para obtener la referencia del mapa
const MapController = ({ position, onMapReady }) => {
  const map = useMapEvents({
    load: () => {
      if (onMapReady) onMapReady(map);
    }
  });
  
  useEffect(() => {
    if (onMapReady && map) {
      onMapReady(map);
    }
  }, [map, onMapReady]);

  useEffect(() => {
    if (position && map) {
      map.setView(position, 10); // Ajustar zoom para mejor visualización
    }
  }, [position, map]);

  return null;
};

const MapSelector = ({ 
  onLocationSelect, 
  initialPosition = [20, 0], // Vista mundial centrada
  selectedPosition = null,
  height = "600px" // Altura aumentada para que el mapa sea más largo hacia abajo
}) => {
  const [position, setPosition] = useState(initialPosition);
  const [markerPosition, setMarkerPosition] = useState(selectedPosition);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [mapInstance, setMapInstance] = useState(null);
  const [searchMessage, setSearchMessage] = useState(null);
  const mapContainerRef = useRef(null);
  
  // Asegurar que Leaflet tenga acceso al objeto window
  useEffect(() => {
    // Forzar a Leaflet a reconocer el entorno
    if (typeof window !== 'undefined') {
      window.L = L;
    }
    
    // Verificar y reinicializar el mapa si es necesario
    const checkMapLoaded = () => {
      if (mapContainerRef.current && mapInstance) {
        reinitializeLeaflet(mapInstance);
      }
    };
    
    checkMapLoaded();
    
    // Reiniciar el mapa cuando la ventana cambia de tamaño
    window.addEventListener('resize', checkMapLoaded);
    return () => {
      window.removeEventListener('resize', checkMapLoaded);
    };
  }, [mapInstance]);

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

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    setSearchMessage(null); // Limpiar mensaje anterior
    
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=1&addressdetails=1`
      );
      const results = await response.json();
      
      if (results.length > 0) {
        const result = results[0];
        const lat = parseFloat(result.lat);
        const lng = parseFloat(result.lon);
        
        const locationData = {
          latitud: lat,
          longitud: lng,
          pais: result.address?.country || 'País no identificado',
          ubicacionCompleta: result.display_name || `${lat}, ${lng}`,
          ciudad: result.address?.city || result.address?.town || result.address?.village || '',
          estado: result.address?.state || ''
        };
        
        const newPosition = [lat, lng];
        setMarkerPosition(newPosition);
        setPosition(newPosition);
        onLocationSelect(locationData);
        
        // Centrar el mapa en la ubicación encontrada
        if (mapInstance) {
          mapInstance.setView(newPosition, 12);
        }
        
        // Mostrar mensaje de éxito
        setSearchMessage({
          type: 'success',
          text: `✅ Ubicación encontrada: ${result.display_name}`
        });
        
        // Limpiar mensaje después de 5 segundos
        setTimeout(() => setSearchMessage(null), 5000);
        
      } else {
        setSearchMessage({
          type: 'error',
          text: `❌ No se encontró la ubicación "${searchQuery}". Intenta con un término diferente.`
        });
        
        // Limpiar mensaje después de 7 segundos
        setTimeout(() => setSearchMessage(null), 7000);
      }
    } catch (error) {
      console.error('Error al buscar ubicación:', error);
      setSearchMessage({
        type: 'error',
        text: '⚠️ Error al buscar la ubicación. Verifica tu conexión e inténtalo de nuevo.'
      });
      
      // Limpiar mensaje después de 7 segundos
      setTimeout(() => setSearchMessage(null), 7000);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="map-selector">
      <div className="map-search">
        <div className="search-container">
          <input
            type="text"
            placeholder="Buscar ubicación"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            className="search-input"
            disabled={isSearching}
          />
          <button
            type="button"
            onClick={handleSearch}
            disabled={isSearching || !searchQuery.trim()}
            className="search-button"
          >
            {isSearching ? '🔍 Buscando...' : '🔍 Buscar'}
          </button>
        </div>
        
        {/* Mensaje de resultado de búsqueda */}
        {searchMessage && (
          <div className={`search-message ${searchMessage.type}`}>
            <span className="message-text">{searchMessage.text}</span>
            <button 
              className="message-close"
              onClick={() => setSearchMessage(null)}
              type="button"
            >
              ×
            </button>
          </div>
        )}
      </div>
      
      <div className="map-container" style={{ height }} ref={mapContainerRef}>
        {isLeafletReady() && (
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
            <MapController position={markerPosition} onMapReady={setMapInstance} />
            
            {markerPosition && (
              <Marker position={markerPosition} icon={DefaultIcon} />
            )}
          </MapContainer>
        )}
      </div>
      
      <div className="map-controls">
        <button 
          type="button" 
          className="btn-clear-location"
          onClick={() => {
            setMarkerPosition(null);
            setSearchQuery('');
            setSearchMessage(null); // Limpiar mensaje al resetear
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
