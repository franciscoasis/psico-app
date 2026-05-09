import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function HomeScreen({ navigation }) {

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pantalla Principal</Text>

      <TouchableOpacity 
        style={[styles.button, styles.buttonSecondary]} 
        onPress={() => navigation.navigate('PacientesList')}
      >
        <Text style={styles.buttonText}>Soy Psicologa</Text>
      </TouchableOpacity>
      <TouchableOpacity 
        style={[styles.button, styles.buttonSecondary]} 
        onPress={() => navigation.navigate('Paciente')}
      >
        <Text style={styles.buttonText}>Soy paciente</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  counter: {
    fontSize: 18,
    marginBottom: 30,
    color: '#333',
  },
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 12,
    paddingHorizontal: 30,
    borderRadius: 8,
    marginBottom: 15,
  },
  buttonSecondary: {
    backgroundColor: '#ff7ece',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
