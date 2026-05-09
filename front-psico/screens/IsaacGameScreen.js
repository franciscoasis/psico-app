import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ActivityIndicator, Alert, ScrollView } from 'react-native';

export default function IsaacGameScreen({ navigation, route }) {
  const { pacienteId, pacienteNombre } = route.params || {};
  
  const [personaje, setPersonaje] = useState('');
  const [dificultad, setDificultad] = useState('Normal');
  const [progresoPisos, setProgresoPisos] = useState('0');
  const [itemsRecolectados, setItemsRecolectados] = useState('');
  const [logros, setLogros] = useState('');
  const [bossId, setBossId] = useState('');
  const [cronogramaSemanal, setCronogramaSemanal] = useState('');
  const [fraseSemanal, setFraseSemanal] = useState('');
  const [objetivos, setObjetivos] = useState('');
  const [recompensas, setRecompensas] = useState('');
  const [corazones, setCorazones] = useState('3');
  const [keys, setKeys] = useState('0');
  const [bombas, setBombas] = useState('0');
  const [monedas, setMonedas] = useState('0');
  const [loading, setLoading] = useState(false);

  const handleCrearJuego = async () => {
    if (!personaje) {
      Alert.alert('Error', 'Por favor selecciona un personaje');
      return;
    }

    try {
      setLoading(true);
      
      const datosJuego = {
        tipo_juego: 'Isaac',
        personaje,
        dificultad,
        progreso_pisos: parseInt(progresoPisos),
        items_recolectados: itemsRecolectados || null,
        logros: logros || null,
        boss_id: bossId ? parseInt(bossId) : null,
        cronograma_semanal: cronogramaSemanal || null,
        frase_semanal: fraseSemanal || null,
        objetivos: objetivos || null,
        recompensas: recompensas || null,
        corazones: parseInt(corazones),
        keys: parseInt(keys),
        bombas: parseInt(bombas),
        monedas: parseInt(monedas),
        paciente_id: pacienteId,
      };

      // TODO: Hacer la llamada a la API para crear el juego
      console.log('Datos del juego Isaac:', datosJuego);
      
      Alert.alert('Éxito', 'Juego de Isaac creado correctamente');
      navigation.goBack();
    } catch (error) {
      Alert.alert('Error', 'No se pudo crear el juego');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Crear Juego: Isaac</Text>
        <Text style={styles.subtitle}>Paciente: {pacienteNombre}</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.label}>Personaje *</Text>
        <TextInput
          style={styles.input}
          placeholder="ej: Isaac, Magdalena, Cain..."
          value={personaje}
          onChangeText={setPersonaje}
        />

        <Text style={styles.label}>Dificultad *</Text>
        <View style={styles.dificultadContainer}>
          {['Fácil', 'Normal', 'Difícil'].map((nivel) => (
            <TouchableOpacity
              key={nivel}
              style={[
                styles.dificultadBtn,
                dificultad === nivel && styles.dificultadBtnActive
              ]}
              onPress={() => setDificultad(nivel)}
            >
              <Text style={styles.dificultadBtnText}>{nivel}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>Progreso de Pisos</Text>
        <TextInput
          style={styles.input}
          placeholder="0"
          value={progresoPisos}
          onChangeText={setProgresoPisos}
          keyboardType="numeric"
        />

        <Text style={styles.label}>Items Recolectados</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          placeholder="Lista de items..."
          value={itemsRecolectados}
          onChangeText={setItemsRecolectados}
          multiline={true}
          numberOfLines={2}
        />

        <Text style={styles.label}>Logros</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          placeholder="Logros obtenidos..."
          value={logros}
          onChangeText={setLogros}
          multiline={true}
          numberOfLines={2}
        />

        <Text style={styles.label}>Boss ID</Text>
        <TextInput
          style={styles.input}
          placeholder="0"
          value={bossId}
          onChangeText={setBossId}
          keyboardType="numeric"
        />

        <Text style={styles.label}>Cronograma Semanal</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          placeholder="Cronograma..."
          value={cronogramaSemanal}
          onChangeText={setCronogramaSemanal}
          multiline={true}
          numberOfLines={2}
        />

        <Text style={styles.label}>Frase Semanal</Text>
        <TextInput
          style={styles.input}
          placeholder="Frase motivacional..."
          value={fraseSemanal}
          onChangeText={setFraseSemanal}
        />

        <Text style={styles.label}>Objetivos</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          placeholder="Objetivos de la sesión..."
          value={objetivos}
          onChangeText={setObjetivos}
          multiline={true}
          numberOfLines={2}
        />

        <Text style={styles.label}>Recompensas</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          placeholder="Recompensas..."
          value={recompensas}
          onChangeText={setRecompensas}
          multiline={true}
          numberOfLines={2}
        />

        <View style={styles.statsContainer}>
          <View style={styles.statInput}>
            <Text style={styles.label}>❤️ Corazones</Text>
            <TextInput
              style={styles.input}
              placeholder="3"
              value={corazones}
              onChangeText={setCorazones}
              keyboardType="numeric"
            />
          </View>
          <View style={styles.statInput}>
            <Text style={styles.label}>🔑 Keys</Text>
            <TextInput
              style={styles.input}
              placeholder="0"
              value={keys}
              onChangeText={setKeys}
              keyboardType="numeric"
            />
          </View>
        </View>

        <View style={styles.statsContainer}>
          <View style={styles.statInput}>
            <Text style={styles.label}>💣 Bombas</Text>
            <TextInput
              style={styles.input}
              placeholder="0"
              value={bombas}
              onChangeText={setBombas}
              keyboardType="numeric"
            />
          </View>
          <View style={styles.statInput}>
            <Text style={styles.label}>💰 Monedas</Text>
            <TextInput
              style={styles.input}
              placeholder="0"
              value={monedas}
              onChangeText={setMonedas}
              keyboardType="numeric"
            />
          </View>
        </View>

        <TouchableOpacity
          style={styles.buttonCrear}
          onPress={handleCrearJuego}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Crear Juego</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.buttonCancelar}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.buttonText}>Cancelar</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#007AFF',
    paddingVertical: 20,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
  },
  form: {
    padding: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 8,
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
  textArea: {
    textAlignVertical: 'top',
    paddingTop: 10,
  },
  dificultadContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  dificultadBtn: {
    flex: 1,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingVertical: 10,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  dificultadBtnActive: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  dificultadBtnText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
    marginBottom: 10,
  },
  statInput: {
    flex: 1,
    marginHorizontal: 5,
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
