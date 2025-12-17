/**
 * Navegação Principal - COM ETIQUETAS
 */
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';

// Screens
import HomeScreen from '../screens/HomeScreen';
import EntradaScreen from '../screens/EntradaScreen';
import SaidaScreen from '../screens/SaidaScreen';
import ProdutosScreen from '../screens/ProdutosScreen';
import CadastrarProdutoScreen from '../screens/CadastrarProdutoScreen';
import EtiquetasScreen from '../screens/EtiquetasScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

// Stack do Home
const HomeStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="HomeMain" 
      component={HomeScreen}
      options={{ headerShown: false }}
    />
    <Stack.Screen 
      name="CadastrarProduto" 
      component={CadastrarProdutoScreen}
      options={{ 
        title: 'Cadastrar Produto',
        headerStyle: { backgroundColor: '#2196F3' },
        headerTintColor: '#fff',
      }}
    />
  </Stack.Navigator>
);

// Stack dos Produtos
const ProdutosStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="ProdutosLista" 
      component={ProdutosScreen}
      options={{ title: 'Produtos' }}
    />
    <Stack.Screen 
      name="CadastrarProduto" 
      component={CadastrarProdutoScreen}
      options={{ 
        title: 'Cadastrar Produto',
        headerStyle: { backgroundColor: '#2196F3' },
        headerTintColor: '#fff',
      }}
    />
  </Stack.Navigator>
);

// Navegação Principal
export default function Navigation() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;
            
            switch(route.name) {
              case 'Home':
                iconName = focused ? 'home' : 'home-outline';
                break;
              case 'Entrada':
                iconName = focused ? 'arrow-down-circle' : 'arrow-down-circle-outline';
                break;
              case 'Saida':
                iconName = focused ? 'arrow-up-circle' : 'arrow-up-circle-outline';
                break;
              case 'Produtos':
                iconName = focused ? 'cube' : 'cube-outline';
                break;
              case 'Etiquetas':
                iconName = focused ? 'pricetag' : 'pricetag-outline';
                break;
              default:
                iconName = 'help-outline';
            }
            
            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#4CAF50',
          tabBarInactiveTintColor: '#999',
          headerShown: false,
        })}
      >
        <Tab.Screen 
          name="Home" 
          component={HomeStack}
          options={{ title: 'Início' }}
        />
        <Tab.Screen 
          name="Entrada" 
          component={EntradaScreen}
          options={{ 
            title: 'Entrada',
            headerShown: true,
            headerStyle: { backgroundColor: '#4CAF50' },
            headerTintColor: '#fff',
          }}
        />
        <Tab.Screen 
          name="Saida" 
          component={SaidaScreen}
          options={{ 
            title: 'Saída',
            headerShown: true,
            headerStyle: { backgroundColor: '#F44336' },
            headerTintColor: '#fff',
          }}
        />
        <Tab.Screen 
          name="Produtos" 
          component={ProdutosStack}
          options={{ title: 'Produtos' }}
        />
        <Tab.Screen 
          name="Etiquetas" 
          component={EtiquetasScreen}
          options={{ 
            title: 'Etiquetas',
            headerShown: true,
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}