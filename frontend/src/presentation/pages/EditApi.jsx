import React, { useState, useEffect } from 'react';
import './EditApi.css';
import { categoriaApi, carreraApi } from '../../shared/config/api';
import MapSelector from '../components/MapSelector';

const EditApi = () => {
  const [pestanaActiva, setPestanaActiva] = useState('categorias');
  const [cargando, setCargando] = useState(false);
  const [mensaje, setMensaje] = useState('');
  
  // Estados para categorías
  const [categorias, setCategorias] = useState([]);
  const [categoriaForm, setCategoriaForm] = useState({ nombre: '' });
  const [categoriaEditando, setCategoriaEditando] = useState(null);
  
  // Estados para carreras
  const [carreras, setCarreras] = useState([]);
  const [carreraForm, setCarreraForm] = useState({
    nombre: '',
    fecha: '',
    pais: '',
    circuito: '',
    latitud: '',
    longitud: '',
    categoria_id: ''
  });
  const [carreraEditando, setCarreraEditando] = useState(null);

  useEffect(() => {
    cargarDatos();
  }, [pestanaActiva]);

  const cargarDatos = async () => {
    setCargando(true);
    try {
      if (pestanaActiva === 'categorias') {
        const data = await categoriaApi.obtenerTodas();
        setCategorias(data);
      } else {
        const [categoriasData, carrerasData] = await Promise.all([
          categoriaApi.obtenerTodas(),
          carreraApi.obtenerTodas()
        ]);
        setCategorias(categoriasData);
        setCarreras(carrerasData);
      }
      setMensaje('');
    } catch (error) {
      setMensaje('Error al cargar los datos: ' + error.message);
    } finally {
      setCargando(false);
    }
  };

  const mostrarMensaje = (texto, tipo = 'info') => {
    setMensaje(texto);
    setTimeout(() => setMensaje(''), 3000);
  };

  // Funciones para categorías
  const manejarCategoriaForm = (e) => {
    setCategoriaForm({ ...categoriaForm, [e.target.name]: e.target.value });
  };

  const guardarCategoria = async (e) => {
    e.preventDefault();
    if (!categoriaForm.nombre.trim()) {
      mostrarMensaje('El nombre de la categoría es requerido', 'error');
      return;
    }

    setCargando(true);
    try {
      if (categoriaEditando) {
        await categoriaApi.actualizar(categoriaEditando.id, categoriaForm);
        mostrarMensaje('Categoría actualizada correctamente', 'success');
        setCategoriaEditando(null);
      } else {
        await categoriaApi.crear(categoriaForm);
        mostrarMensaje('Categoría creada correctamente', 'success');
      }
      setCategoriaForm({ nombre: '' });
      cargarDatos();
    } catch (error) {
      mostrarMensaje('Error al guardar la categoría: ' + error.message, 'error');
    } finally {
      setCargando(false);
    }
  };

  const editarCategoria = (categoria) => {
    setCategoriaEditando(categoria);
    setCategoriaForm({ nombre: categoria.nombre });
  };

  const eliminarCategoria = async (id) => {
    if (!confirm('¿Estás seguro de que quieres eliminar esta categoría?')) return;

    setCargando(true);
    try {
      await categoriaApi.eliminar(id);
      mostrarMensaje('Categoría eliminada correctamente', 'success');
      cargarDatos();
    } catch (error) {
      mostrarMensaje('Error al eliminar la categoría: ' + error.message, 'error');
    } finally {
      setCargando(false);
    }
  };

  const cancelarEdicionCategoria = () => {
    setCategoriaEditando(null);
    setCategoriaForm({ nombre: '' });
  };

  // Funciones para carreras
  const manejarCarreraForm = (e) => {
    setCarreraForm({ ...carreraForm, [e.target.name]: e.target.value });
  };

  const guardarCarrera = async (e) => {
    e.preventDefault();
    const { nombre, fecha, pais, circuito, latitud, longitud, categoria_id } = carreraForm;
    
    if (!nombre.trim() || !fecha || !pais.trim() || !circuito.trim() || !latitud || !longitud || !categoria_id) {
      mostrarMensaje('Todos los campos son requeridos. Por favor, selecciona una ubicación en el mapa.', 'error');
      return;
    }

    setCargando(true);
    try {
      const carreraData = {
        ...carreraForm,
        fecha: new Date(fecha).toISOString(),
        latitud: parseFloat(latitud),
        longitud: parseFloat(longitud)
      };

      if (carreraEditando) {
        await carreraApi.actualizar(carreraEditando.id, carreraData);
        mostrarMensaje('Carrera actualizada correctamente', 'success');
        setCarreraEditando(null);
      } else {
        await carreraApi.crear(carreraData);
        mostrarMensaje('Carrera creada correctamente', 'success');
      }
      setCarreraForm({
        nombre: '',
        fecha: '',
        pais: '',
        circuito: '',
        latitud: '',
        longitud: '',
        categoria_id: ''
      });
      cargarDatos();
    } catch (error) {
      mostrarMensaje('Error al guardar la carrera: ' + error.message, 'error');
    } finally {
      setCargando(false);
    }
  };

  const editarCarrera = (carrera) => {
    setCarreraEditando(carrera);
    setCarreraForm({
      nombre: carrera.nombre,
      fecha: new Date(carrera.fecha).toISOString().slice(0, 16),
      pais: carrera.pais,
      circuito: carrera.circuito,
      latitud: carrera.latitud.toString(),
      longitud: carrera.longitud.toString(),
      categoria_id: carrera.categoria_id
    });
  };

  const eliminarCarrera = async (id) => {
    if (!confirm('¿Estás seguro de que quieres eliminar esta carrera?')) return;

    setCargando(true);
    try {
      await carreraApi.eliminar(id);
      mostrarMensaje('Carrera eliminada correctamente', 'success');
      cargarDatos();
    } catch (error) {
      mostrarMensaje('Error al eliminar la carrera: ' + error.message, 'error');
    } finally {
      setCargando(false);
    }
  };

  const cancelarEdicionCarrera = () => {
    setCarreraEditando(null);
    setCarreraForm({
      nombre: '',
      fecha: '',
      pais: '',
      circuito: '',
      latitud: '',
      longitud: '',
      categoria_id: ''
    });
  };

  const manejarSeleccionMapa = (locationData) => {
    setCarreraForm(prev => ({
      ...prev,
      latitud: locationData.latitud.toString(),
      longitud: locationData.longitud.toString(),
      pais: locationData.pais
    }));
  };

  return (
    <div className="edit-api-container">
      <div className="edit-api-header">
        <h1>Gestión de Datos API</h1>
        <div className="pestanas">
          <button
            className={`pestana ${pestanaActiva === 'categorias' ? 'activa' : ''}`}
            onClick={() => setPestanaActiva('categorias')}
          >
            Categorías
          </button>
          <button
            className={`pestana ${pestanaActiva === 'carreras' ? 'activa' : ''}`}
            onClick={() => setPestanaActiva('carreras')}
          >
            Carreras
          </button>
        </div>
      </div>

      {mensaje && (
        <div className={`mensaje ${mensaje.includes('Error') ? 'error' : 'success'}`}>
          {mensaje}
        </div>
      )}

      {cargando && <div className="cargando">Cargando...</div>}

      {pestanaActiva === 'categorias' && (
        <div className="seccion-categorias">
          <div className="formulario-card">
            <h2>{categoriaEditando ? 'Editar Categoría' : 'Nueva Categoría'}</h2>
            <form onSubmit={guardarCategoria}>
              <div className="input-group">
                <label>Nombre:</label>
                <input
                  type="text"
                  name="nombre"
                  value={categoriaForm.nombre}
                  onChange={manejarCategoriaForm}
                  placeholder="Ingrese el nombre de la categoría"
                  required
                />
              </div>
              <div className="botones">
                <button type="submit" disabled={cargando}>
                  {categoriaEditando ? 'Actualizar' : 'Crear'}
                </button>
                {categoriaEditando && (
                  <button type="button" onClick={cancelarEdicionCategoria}>
                    Cancelar
                  </button>
                )}
              </div>
            </form>
          </div>

          <div className="lista-card">
            <h2>Categorías Existentes</h2>
            <div className="tabla-container">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {categorias.map(categoria => (
                    <tr key={categoria.id}>
                      <td>{categoria.id}</td>
                      <td>{categoria.nombre}</td>
                      <td>
                        <button
                          className="btn-editar"
                          onClick={() => editarCategoria(categoria)}
                        >
                          Editar
                        </button>
                        <button
                          className="btn-eliminar"
                          onClick={() => eliminarCategoria(categoria.id)}
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {pestanaActiva === 'carreras' && (
        <div className="seccion-carreras-tres-columnas">
          <div className="mapa-columna">
            <div className="mapa-card">
              <h2>📍 Seleccionar Ubicación</h2>
              <MapSelector
                onLocationSelect={manejarSeleccionMapa}
                selectedPosition={
                  carreraForm.latitud && carreraForm.longitud
                    ? [parseFloat(carreraForm.latitud), parseFloat(carreraForm.longitud)]
                    : null
                }
                height="auto"
              />
            </div>
          </div>
          
          <div className="formulario-columna">
            <div className="formulario-card">
              <h2>{carreraEditando ? 'Editar Carrera' : 'Nueva Carrera'}</h2>
              <form onSubmit={guardarCarrera}>
                <div className="input-group">
                  <label>Nombre:</label>
                  <input
                    type="text"
                    name="nombre"
                    value={carreraForm.nombre}
                    onChange={manejarCarreraForm}
                    placeholder="Ingrese el nombre de la carrera"
                    required
                  />
                </div>
                <div className="input-group">
                  <label>Fecha:</label>
                  <input
                    type="datetime-local"
                    name="fecha"
                    value={carreraForm.fecha}
                    onChange={manejarCarreraForm}
                    required
                  />
                </div>
                <div className="input-group">
                  <label>País:</label>
                  <input
                    type="text"
                    name="pais"
                    value={carreraForm.pais}
                    onChange={manejarCarreraForm}
                    placeholder="Se completará automáticamente al seleccionar en el mapa"
                    readOnly
                  />
                </div>
                <div className="input-group">
                  <label>Circuito:</label>
                  <input
                    type="text"
                    name="circuito"
                    value={carreraForm.circuito}
                    onChange={manejarCarreraForm}
                    placeholder="Ingrese el nombre del circuito"
                    required
                  />
                </div>
                
                <div className="coordenadas-display">
                  {carreraForm.latitud && carreraForm.longitud ? (
                    <div className="coordenadas-info">
                      <p><strong>Coordenadas:</strong> {parseFloat(carreraForm.latitud).toFixed(6)}, {parseFloat(carreraForm.longitud).toFixed(6)}</p>
                      <p><strong>País:</strong> {carreraForm.pais}</p>
                    </div>
                  ) : (
                    <p className="no-coordenadas">Selecciona una ubicación en el mapa</p>
                  )}
                </div>
                
                <div className="input-group" style={{ display: 'none' }}>
                  <label>Latitud:</label>
                  <input
                    type="number"
                    name="latitud"
                    value={carreraForm.latitud}
                    onChange={manejarCarreraForm}
                    step="any"
                    readOnly
                  />
                </div>
                <div className="input-group" style={{ display: 'none' }}>
                  <label>Longitud:</label>
                  <input
                    type="number"
                    name="longitud"
                    value={carreraForm.longitud}
                    onChange={manejarCarreraForm}
                    step="any"
                    readOnly
                  />
                </div>
                <div className="input-group">
                  <label>Categoría:</label>
                  <select
                    name="categoria_id"
                    value={carreraForm.categoria_id}
                    onChange={manejarCarreraForm}
                    required
                  >
                    <option value="">Seleccione una categoría</option>
                    {categorias.map(categoria => (
                      <option key={categoria.id} value={categoria.id}>
                        {categoria.nombre}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="botones">
                  <button type="submit" disabled={cargando}>
                    {carreraEditando ? 'Actualizar' : 'Crear'}
                  </button>
                  {carreraEditando && (
                    <button type="button" onClick={cancelarEdicionCarrera}>
                      Cancelar
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          <div className="tabla-columna">
            <div className="lista-card">
              <h2>Carreras Existentes</h2>
              <div className="tabla-container">
                <table>
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Fecha</th>
                      <th>País</th>
                      <th>Circuito</th>
                      <th>Categoría</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {carreras.map(carrera => (
                      <tr key={carrera.id}>
                        <td>{carrera.nombre}</td>
                        <td>{new Date(carrera.fecha).toLocaleDateString()}</td>
                        <td>{carrera.pais}</td>
                        <td>{carrera.circuito}</td>
                        <td>
                          {categorias.find(cat => cat.id === carrera.categoria_id)?.nombre || 'N/A'}
                        </td>
                        <td>
                          <button
                            className="btn-editar"
                            onClick={() => editarCarrera(carrera)}
                          >
                            Editar
                          </button>
                          <button
                            className="btn-eliminar"
                            onClick={() => eliminarCarrera(carrera.id)}
                          >
                            Eliminar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EditApi;
