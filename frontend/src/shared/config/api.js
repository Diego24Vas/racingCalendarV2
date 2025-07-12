// Configuración de la API
const API_CONFIG = {
  BASE_URL: 'http://localhost:8001',
  TIMEOUT: 5000,
  HEADERS: {
    'Content-Type': 'application/json',
  }
};

// Función para verificar si la API está funcionando
export const verificarEstadoApi = async () => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);

    const response = await fetch(`${API_CONFIG.BASE_URL}/`, {
      method: 'GET',
      headers: API_CONFIG.HEADERS,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      return {
        success: true,
        data: data,
        message: 'API conectada correctamente'
      };
    } else {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      return {
        success: false,
        error: 'Timeout - La API no responde',
        message: 'La conexión ha tardado demasiado'
      };
    }
    return {
      success: false,
      error: error.message,
      message: 'No se pudo conectar con la API'
    };
  }
};

// Función genérica para hacer peticiones a la API
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;
  const config = {
    headers: API_CONFIG.HEADERS,
    ...options
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en petición API:', error);
    throw error;
  }
};

// Funciones para gestionar categorías
export const categoriaApi = {
  obtenerTodas: async () => {
    return await apiRequest('/categorias');
  },
  
  obtenerPorId: async (id) => {
    return await apiRequest(`/categorias/${id}`);
  },
  
  crear: async (categoria) => {
    return await apiRequest('/categorias', {
      method: 'POST',
      body: JSON.stringify(categoria)
    });
  },
  
  actualizar: async (id, categoria) => {
    return await apiRequest(`/categorias/${id}`, {
      method: 'PUT',
      body: JSON.stringify(categoria)
    });
  },
  
  eliminar: async (id) => {
    return await apiRequest(`/categorias/${id}`, {
      method: 'DELETE'
    });
  }
};

// Funciones para gestionar carreras
export const carreraApi = {
  obtenerTodas: async () => {
    return await apiRequest('/carreras');
  },
  
  obtenerPorId: async (id) => {
    return await apiRequest(`/carreras/${id}`);
  },
  
  crear: async (carrera) => {
    return await apiRequest('/carreras', {
      method: 'POST',
      body: JSON.stringify(carrera)
    });
  },
  
  actualizar: async (id, carrera) => {
    return await apiRequest(`/carreras/${id}`, {
      method: 'PUT',
      body: JSON.stringify(carrera)
    });
  },
  
  eliminar: async (id) => {
    return await apiRequest(`/carreras/${id}`, {
      method: 'DELETE'
    });
  }
};

export default API_CONFIG;
