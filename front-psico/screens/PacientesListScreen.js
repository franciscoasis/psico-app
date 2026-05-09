import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator, RefreshControl, Alert, Modal } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { getPacientes, eliminarPaciente } from '../services/pacienteService';

export default function PacientesListScreen({ navigation }) {
  const [pacientes, setPacientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [pacienteSeleccionado, setPacienteSeleccionado] = useState(null);
  const [modalJuegoVisible, setModalJuegoVisible] = useState(false);

  useEffect(() => {
    cargarPacientes();
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      cargarPacientes();
    }, [])
  );

  const cargarPacientes = async () => {
    try {
      setLoading(true);
      const data = await getPacientes();
      console.log('Datos recibidos:', data);
      console.log('Tipo de datos:', typeof data);
      console.log('Es array:', Array.isArray(data));
      setPacientes(data || []);
      setError(null);
    } catch (err) {
      setError('Error al cargar pacientes');
      console.error('Error completo:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    cargarPacientes();
  };

  const handleMenuPaciente = (paciente) => {
    setPacienteSeleccionado(paciente);
    setModalVisible(true);
  };

  const handleHabilitarJuego = () => {
    setModalVisible(false);
    window.alert('Función de editar juego en desarrollo');
  };

  const handleCrearJuego = () => {
    setModalVisible(false);
    setModalJuegoVisible(true);
  };

  const handleSeleccionarJuego = (juego) => {
    setModalJuegoVisible(false);
    
    if (juego === 'Isaac') {
      navigation.navigate('IsaacGame', {
        pacienteId: pacienteSeleccionado?.id,
        pacienteNombre: `${pacienteSeleccionado?.nombre} ${pacienteSeleccionado?.apellido}`,
      });
    } else if (juego === 'Minecraft') {
      window.alert('Función de crear Minecraft en desarrollo');
    }
  };

  const handleEliminar = async (paciente) => {
    const confirmar = window.confirm(
      `¿Estás seguro que quieres eliminar a ${paciente.nombre} ${paciente.apellido}?`
    );
    
    if (confirmar) {
      try {
        await eliminarPaciente(paciente.id);
        await cargarPacientes();
        window.alert('Éxito: Paciente eliminado');
      } catch (error) {
        window.alert('Error: No se pudo eliminar el paciente');
      }
    }
  };

  const renderPaciente = ({ item }) => (
    <View style={styles.pacienteCard}>
      <TouchableOpacity 
        style={styles.cardContent}
        onPress={() => handleMenuPaciente(item)}
        activeOpacity={0.7}
      >
        <Text style={styles.nombre}>{item.nombre} {item.apellido}</Text>
        <Text style={styles.telefono}>{item.telefono}</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={styles.deleteButton}
        onPress={() => handleEliminar(item)}
        activeOpacity={0.7}
      >
        <Text style={styles.deleteButtonText}>✕</Text>
      </TouchableOpacity>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('CrearPaciente')}
      >
        <Text style={styles.buttonText}>+ Agregar Paciente</Text>
      </TouchableOpacity>

      {error && <Text style={styles.error}>{error}</Text>}
      
      <FlatList
        data={pacientes}
        renderItem={renderPaciente}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
      />

      <Modal
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>
              {pacienteSeleccionado?.nombre} {pacienteSeleccionado?.apellido}
            </Text>
            <Text style={styles.modalSubtitle}>Selecciona una opción:</Text>

            <TouchableOpacity 
              style={styles.modalButton}
              onPress={handleHabilitarJuego}
            >
              <Text style={styles.modalButtonText}>Editar Juego</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={styles.modalButton}
              onPress={handleCrearJuego}
            >
              <Text style={styles.modalButtonText}>Crear Juego</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.modalButton, styles.cancelButton]}
              onPress={() => setModalVisible(false)}
            >
              <Text style={styles.modalButtonText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      <Modal
        transparent={true}
        visible={modalJuegoVisible}
        onRequestClose={() => setModalJuegoVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Selecciona un Juego</Text>
            <Text style={styles.modalSubtitle}>Elige qué juego crear para el paciente:</Text>

            <TouchableOpacity 
              style={styles.modalButton}
              onPress={() => handleSeleccionarJuego('Isaac')}
            >
              <Text style={styles.modalButtonText}>🎮 Isaac</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={styles.modalButton}
              onPress={() => handleSeleccionarJuego('Minecraft')}
            >
              <Text style={styles.modalButtonText}>⛏️ Minecraft</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.modalButton, styles.cancelButton]}
              onPress={() => setModalJuegoVisible(false)}
            >
              <Text style={styles.modalButtonText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingTop: 10,
  },
  listContainer: {
    paddingHorizontal: 15,
  },
  pacienteCard: {
    backgroundColor: '#fff',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007AFF',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 10,
  },
  cardContent: {
    flex: 1,
    paddingRight: 10,
  },
  nombre: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  telefono: {
    fontSize: 14,
    color: '#666',
  },
  deleteButton: {
    width: 40,
    height: 40,
    backgroundColor: '#FF3B30',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
    flexShrink: 0,
  },
  deleteButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  error: {
    color: '#FF3B30',
    textAlign: 'center',
    padding: 10,
    marginHorizontal: 15,
    marginBottom: 10,
  },
  button: {
    backgroundColor: '#34C759',
    margin: 15,
    marginBottom: 10,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    width: '80%',
    maxWidth: 400,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
  },
  modalSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
  },
  modalButton: {
    backgroundColor: '#007AFF',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 10,
  },
  cancelButton: {
    backgroundColor: '#999',
  },
  modalButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
});
