import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './screens/HomeScreen';
import DetailScreen from './screens/DetailScreen';
import PacienteScreen from './screens/PacienteScreen';
import PacientesListScreen from './screens/PacientesListScreen';
import CrearPacienteScreen from './screens/CrearPacienteScreen';
import IsaacGameScreen from './screens/IsaacGameScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: true,
          headerStyle: {
            backgroundColor: '#007AFF',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: 'Inicio' }}
        />
        <Stack.Screen 
          name="Detail" 
          component={DetailScreen}
          options={{ title: 'Detalles' }}
        />
        <Stack.Screen 
          name="Paciente" 
          component={PacienteScreen}
          options={{ title: 'Paciente' }}
        />
        <Stack.Screen 
          name="PacientesList" 
          component={PacientesListScreen}
          options={{ title: 'Mis Pacientes' }}
        />
        <Stack.Screen 
          name="CrearPaciente" 
          component={CrearPacienteScreen}
          options={{ title: 'Crear Paciente' }}
        />
        <Stack.Screen 
          name="IsaacGame" 
          component={IsaacGameScreen}
          options={{ title: 'Crear Juego Isaac' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
