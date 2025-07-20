import React, { useRef, useState, useEffect } from 'react';
import { MapContainer, TileLayer, ZoomControl } from 'react-leaflet';
import { 
  useLeafletReinitializer, 
  useLeafletReady, 
  useGeocoder, 
  useMapMarker 
} from './LeafletUtils';
import 'leaflet/dist/leaflet.css';
import './LeafletFix.css';

// Componente que muestra cómo usar los hooks de Leaflet
const ReactMap = ({ 
  initialPosition = [20, 0],
  height = "600px",
  onLocationSelect = () => {},
  selectedPosition = null 
}) => {
  const mapRef = useRef(null);
  const isLeafletReady = useLeafletReady();
  const [map, setMap] = useState(null);
  const [position, setPosition] = useState(initialPosition);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Usar los hooks personalizados
  useLeafletReinitializer(mapRef);
  const { geocodeAddress, reverseGeocode, isLoading, error } = useGeocoder();
  const { addMarker, removeMarker } = useMapMarker(map);
  
  // Efecto para manejar el mapa cuando esté disponible
  useEffect(() => {
    if (mapRef.current && mapRef.current._leaflet_id) {
      setMap(mapRef.current);
    }
  }, [mapRef.current]);
  
  // Efecto para cuando cambie la posición seleccionada
  useEffect(() => {
    if (selectedPosition && map) {
      setPosition(selectedPosition);
      map.setView(selectedPosition, 10);
      addMarker(selectedPosition);
    }
  }, [selectedPosition, map, addMarker]);
  
  // Manejar clic en el mapa
  const handleMapClick = async (e) => {
    const { lat, lng } = e.latlng;
    const newPosition = [lat, lng];
    
    setPosition(newPosition);
    addMarker(newPosition);
    
    try {
      const data = await reverseGeocode(lat, lng);
      
      if (data) {
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
      }
    } catch (error) {
      console.error('Error al obtener información de ubicación:', error);
    }
  };
  
  // Manejar búsqueda
  const handleSearch = async () => {
    if (!searchQuery.trim() || !map) return;
    
    try {
      const locationData = await geocodeAddress(searchQuery);
      
      if (locationData) {
        const { lat, lng, displayName, address } = locationData;
        const newPosition = [lat, lng];
        
        setPosition(newPosition);
        map.setView(newPosition, 10);
        addMarker(newPosition);
        
        onLocationSelect({
          latitud: lat,
          longitud: lng,
          pais: address?.country || 'País no identificado',
          ubicacionCompleta: displayName || `${lat}, ${lng}`,
          ciudad: address?.city || address?.town || address?.village || '',
          estado: address?.state || ''
        });
      } else {
        // Manejar caso cuando no se encuentra la ubicación
        console.log('No se encontró la ubicación');
      }
    } catch (error) {
      console.error('Error al buscar ubicación:', error);
    }
  };
  
  // Manejar limpiar selección
  const handleClearSelection = () => {
    setSearchQuery('');
    removeMarker();
    onLocationSelect({
      latitud: '',
      longitud: '',
      pais: '',
      ubicacionCompleta: '',
      ciudad: '',
      estado: ''
    });
  };
  
  return (
    <div className="react-map-selector">
      <div className="map-search">
        <div className="search-container">
          <input
            type="text"
            placeholder="Buscar ubicación"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="search-input"
            disabled={isLoading}
          />
          <button
            type="button"
            onClick={handleSearch}
            disabled={isLoading || !searchQuery.trim()}
            className="search-button"
          >
            {isLoading ? '🔍 Buscando...' : '🔍 Buscar'}
          </button>
        </div>
        
        {error && (
          <div className="search-message error">
            <span className="message-text">⚠️ {error}</span>
            <button 
              className="message-close"
              onClick={() => {/* Limpiar error */}}
              type="button"
            >
              ×
            </button>
          </div>
        )}
      </div>
      
      <div className="map-container" style={{ height }}>
        {isLeafletReady && (
          <MapContainer
            center={position}
            zoom={2}
            style={{ height: '100%', width: '100%' }}
            scrollWheelZoom={true}
            whenCreated={(mapInstance) => {
              mapRef.current = mapInstance;
              setMap(mapInstance);
            }}
            ref={mapRef}
            zoomControl={false}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <ZoomControl position="bottomright" />
            
            {/* Usar un evento personalizado para manejar clics en el mapa */}
            {map && (
              <div style={{ display: 'none' }}>
                {map.on('click', handleMapClick)}
              </div>
            )}
          </MapContainer>
        )}
      </div>
      
      <div className="map-controls">
        <button 
          type="button" 
          className="btn-clear-location"
          onClick={handleClearSelection}
        >
          Limpiar Selección
        </button>
      </div>
    </div>
  );
};

export default ReactMap;
