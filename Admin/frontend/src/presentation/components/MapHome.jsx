import React, { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { carreraApi } from '../../shared/config/api'
import './MapHome.css'

// Configurar los iconos por defecto de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const MapHome = () => {
  const [carreras, setCarreras] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const cargarCarreras = async () => {
      try {
        setLoading(true)
        const data = await carreraApi.obtenerTodas()
        setCarreras(data)
        setError(null)
      } catch (err) {
        setError('Error al cargar las carreras')
        console.error('Error:', err)
      } finally {
        setLoading(false)
      }
    }

    cargarCarreras()
  }, [])

  if (loading) {
    return (
      <div className="map-home-container">
        <div className="map-loading">
          <div className="loading-spinner"></div>
          <p>Cargando carreras...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="map-home-container">
        <div className="map-error">
          <p>{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="map-home-container">
      <div className="map-wrapper">
        <MapContainer
          center={[37.17394434953082, -10.649677562755722]} // Madrid como centro por defecto
          zoom={2}
          style={{ height: '100%', width: '100%' }}
          className="racing-map"
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {carreras.map((carrera) => (
            <Marker
              key={carrera.id}
              position={[carrera.latitud, carrera.longitud]}
            >
              <Popup>
                <div className="popup-content">
                  <h3>{carrera.nombre}</h3>
                  <p><strong>Circuito:</strong> {carrera.circuito}</p>
                  <p><strong>País:</strong> {carrera.pais}</p>
                  <p><strong>Fecha:</strong> {new Date(carrera.fecha).toLocaleDateString()}</p>
                  <p><strong>Categoría ID:</strong> {carrera.categoria_id}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
      <div className="map-info">
        <p>Mostrando {carreras.length} carreras registradas</p>
      </div>
    </div>
  )
}

export default MapHome
import './MapHome.css'

