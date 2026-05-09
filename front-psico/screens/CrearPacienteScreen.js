import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ActivityIndicator, Alert } from 'react-native';
import { crearPaciente } from '../services/pacienteService';

export default function CrearPacienteScreen({ navigation }) {
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [telefono, setTelefono] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCrear = async () => {
    if (!nombre || !apellido) {
      Alert.alert('Error', 'Completa los campos obligatorios');
      return;
    }

    try {
      setLoading(true);
      await crearPaciente({
        nombre,
        apellido,
        telefono,
      });
      Alert.alert('Éxito', 'Paciente creado correctamente');
      navigation.goBack();
    } catch (error) {
      Alert.alert('Error', 'No se pudo crear el paciente');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Nombre *</Text>
      <TextInput
        style={styles.input}
        placeholder="Juan"
        value={nombre}
        onChangeText={setNombre}
      />

      <Text style={styles.label}>Apellido *</Text>
      <TextInput
        style={styles.input}
        placeholder="García"
        value={apellido}
        onChangeText={setApellido}
      />

      <Text style={styles.label}>Teléfono</Text>
      <TextInput
        style={styles.input}
        placeholder="555-1234"
        value={telefono}
        onChangeText={setTelefono}
        keyboardType="phone-pad"
      />

      <TouchableOpacity 
        style={styles.buttonCrear}
        onPress={handleCrear}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Crear Paciente</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity 
        style={styles.buttonCancelar}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Cancelar</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 5,
    color: '#333',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
  },
  
  buttonCrear: {
    backgroundColor: '#34C759',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonCancelar: {
    backgroundColor: '#FF3B30',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
