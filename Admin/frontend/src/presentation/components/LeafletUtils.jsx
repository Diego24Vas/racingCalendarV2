import React, { useEffect, useState, useCallback, useRef } from 'react';
import L from 'leaflet';

// Hook para reinicializar el mapa si no se carga correctamente
export const useLeafletReinitializer = (mapRef) => {
  useEffect(() => {
    if (!mapRef.current) return;
    
    const handleResize = () => {
      if (mapRef.current && mapRef.current._leaflet_id) {
        mapRef.current.invalidateSize(true);
      }
    };
    
    // Inicializar y volver a calcular tamaño después de renderizado
    const timer = setTimeout(() => {
      handleResize();
    }, 200);
    
    // Escuchar eventos de resize
    window.addEventListener('resize', handleResize);
    
    // Limpieza
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(timer);
    };
  }, [mapRef]);
};

// Hook para verificar si Leaflet está listo
export const useLeafletReady = () => {
  const [isReady, setIsReady] = useState(false);
  
  useEffect(() => {
    const isLeafletAvailable = 
      typeof window !== 'undefined' && 
      typeof L !== 'undefined' && 
      typeof L.map === 'function';
    
    setIsReady(isLeafletAvailable);
    
    // Comprobar periódicamente si Leaflet está disponible (útil para carga asíncrona)
    if (!isLeafletAvailable) {
      const checkInterval = setInterval(() => {
        if (typeof window !== 'undefined' && typeof L !== 'undefined' && typeof L.map === 'function') {
          setIsReady(true);
          clearInterval(checkInterval);
        }
      }, 100);
      
      return () => clearInterval(checkInterval);
    }
  }, []);
  
  return isReady;
};

// Hook para geocodificar direcciones
export const useGeocoder = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const geocodeAddress = useCallback(async (address) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1&addressdetails=1`
      );
      const results = await response.json();
      
      if (results.length > 0) {
        const result = results[0];
        return {
          lat: parseFloat(result.lat),
          lng: parseFloat(result.lon),
          displayName: result.display_name,
          address: result.address
        };
      }
      return null;
    } catch (error) {
      console.error('Error al geocodificar dirección:', error);
      setError(error.message || 'Error al geocodificar dirección');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const reverseGeocode = useCallback(async (lat, lng) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=3&addressdetails=1`
      );
      return await response.json();
    } catch (error) {
      console.error('Error al obtener información de ubicación:', error);
      setError(error.message || 'Error al obtener información de ubicación');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  return { geocodeAddress, reverseGeocode, isLoading, error };
};

// Hook personalizado para manejar un marcador en el mapa
export const useMapMarker = (map) => {
  const [marker, setMarker] = useState(null);
  
  const addMarker = useCallback((position, options = {}) => {
    if (!map) return null;
    
    // Eliminar el marcador anterior si existe
    if (marker) {
      marker.remove();
    }
    
    // Crear un nuevo marcador
    const newMarker = L.marker(position, options).addTo(map);
    setMarker(newMarker);
    return newMarker;
  }, [map, marker]);
  
  const removeMarker = useCallback(() => {
    if (marker) {
      marker.remove();
      setMarker(null);
    }
  }, [marker]);
  
  // Limpiar al desmontar
  useEffect(() => {
    return () => {
      if (marker) {
        marker.remove();
      }
    };
  }, [marker]);
  
  return { marker, addMarker, removeMarker };
};

// Función auxiliar: mantener compatibilidad con código existente
export const reinitializeLeaflet = (mapContainer) => {
  if (!mapContainer) return;
  
  // Forzar recálculo del tamaño del contenedor
  setTimeout(() => {
    const event = new Event('resize');
    window.dispatchEvent(event);
    
    // Si hay una instancia de mapa disponible
    if (mapContainer._leaflet_id) {
      mapContainer.invalidateSize(true);
    }
  }, 200);
};

// Función auxiliar: mantener compatibilidad con código existente
export const isLeafletReady = () => {
  return typeof window !== 'undefined' && 
         typeof L !== 'undefined' && 
         typeof L.map === 'function';
};
