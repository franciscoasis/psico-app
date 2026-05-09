const API_URL = 'http://localhost:8000/api/v1';

export const getPacientes = async (skip = 0, limit = 10) => {
  try {
    const url = `${API_URL}/pacientes/?skip=${skip}&limit=${limit}`;
    console.log('Pidiendo:', url);
    const response = await fetch(url);
    console.log('Response status:', response.status);
    if (!response.ok) throw new Error(`Error ${response.status}: Error al obtener pacientes`);
    const data = await response.json();
    console.log('Pacientes recibidos:', data);
    return data.pacientes; // Extrae el array de pacientes
  } catch (error) {
    console.error('Error completo:', error);
    throw error;
  }
};

export const getPaciente = async (id) => {
  try {
    const response = await fetch(`${API_URL}/pacientes/${id}`);
    if (!response.ok) throw new Error('Error al obtener paciente');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const crearPaciente = async (paciente) => {
  try {
    const response = await fetch(`${API_URL}/pacientes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(paciente),
    });
    if (!response.ok) throw new Error('Error al crear paciente');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const actualizarPaciente = async (id, paciente) => {
  try {
    const response = await fetch(`${API_URL}/pacientes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(paciente),
    });
    if (!response.ok) throw new Error('Error al actualizar paciente');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const eliminarPaciente = async (id) => {
  try {
    const url = `${API_URL}/pacientes/${id}`;
    console.log('Eliminando paciente en:', url);
    const response = await fetch(url, {
      method: 'DELETE',
    });
    console.log('Response status:', response.status);
    const responseText = await response.text();
    console.log('Response body:', responseText);
    
    if (!response.ok) throw new Error(`Error ${response.status}: Error al eliminar paciente`);
    
    try {
      return JSON.parse(responseText);
    } catch {
      return true;
    }
  } catch (error) {
    console.error('Error al eliminar:', error);
    throw error;
  }
};
