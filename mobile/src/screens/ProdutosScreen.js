/**
 * Tela de Lista de Produtos
 */
import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  RefreshControl,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { produtosAPI } from '../services/api';

const ProdutosScreen = ({ navigation }) => {
  const [produtos, setProdutos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [busca, setBusca] = useState('');

  useFocusEffect(
    useCallback(() => {
      carregarProdutos();
    }, [])
  );

  const carregarProdutos = async () => {
    try {
      setLoading(true);
      const data = await produtosAPI.listar();
      setProdutos(data);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
      Alert.alert('Erro', 'Não foi possível carregar os produtos');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const buscarProdutos = async (termo) => {
    if (!termo) {
      carregarProdutos();
      return;
    }
    try {
      const data = await produtosAPI.buscar(termo);
      setProdutos(data);
    } catch (error) {
      console.error('Erro ao buscar:', error);
    }
  };

  const renderProduto = ({ item }) => (
    <TouchableOpacity style={styles.produtoCard}>
      <View style={styles.produtoHeader}>
        <View style={[
          styles.estoqueBadge,
          item.estoque_atual <= item.estoque_minimo && styles.estoqueBaixo
        ]}>
          <Text style={styles.estoqueText}>{item.estoque_atual}</Text>
        </View>
        <View style={styles.produtoInfo}>
          <Text style={styles.produtoNome}>{item.nome}</Text>
          <Text style={styles.produtoDetalhes}>
            {item.tipo?.nome || 'N/A'} • {item.cor?.nome || 'N/A'}
          </Text>
          <Text style={styles.codigoBarras}>📊 {item.codigo_barras}</Text>
        </View>
      </View>
      {item.preco_venda && (
        <View style={styles.precoContainer}>
          <Text style={styles.preco}>
            R$ {parseFloat(item.preco_venda).toFixed(2)}
          </Text>
        </View>
      )}
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Carregando produtos...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Busca */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color="#666" />
        <TextInput
          style={styles.searchInput}
          value={busca}
          onChangeText={(text) => {
            setBusca(text);
            buscarProdutos(text);
          }}
          placeholder="Buscar produto..."
        />
        {busca.length > 0 && (
          <TouchableOpacity onPress={() => {
            setBusca('');
            carregarProdutos();
          }}>
            <Ionicons name="close-circle" size={20} color="#999" />
          </TouchableOpacity>
        )}
      </View>

      {/* Lista */}
      <FlatList
        data={produtos}
        renderItem={renderProduto}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={carregarProdutos} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="cube-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>
              {busca ? 'Nenhum produto encontrado' : 'Nenhum produto cadastrado'}
            </Text>
            {!busca && (
              <TouchableOpacity
                style={styles.emptyButton}
                onPress={() => navigation.navigate('CadastrarProduto')}
              >
                <Text style={styles.emptyButtonText}>Cadastrar Primeiro Produto</Text>
              </TouchableOpacity>
            )}
          </View>
        }
      />

      {/* Botão Adicionar */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.navigate('CadastrarProduto')}
      >
        <Ionicons name="add" size={30} color="#fff" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  loadingContainer: { 
    flex: 1, 
    justifyContent: 'center', 
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    margin: 15,
    paddingHorizontal: 15,
    borderRadius: 8,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  searchInput: { 
    flex: 1, 
    padding: 12, 
    fontSize: 16,
  },
  produtoCard: {
    backgroundColor: '#fff',
    marginHorizontal: 15,
    marginBottom: 10,
    padding: 15,
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  produtoHeader: { flexDirection: 'row' },
  estoqueBadge: {
    backgroundColor: '#4CAF50',
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  estoqueBaixo: { backgroundColor: '#FF9800' },
  estoqueText: { 
    color: '#fff', 
    fontSize: 18, 
    fontWeight: 'bold',
  },
  produtoInfo: { flex: 1 },
  produtoNome: { 
    fontSize: 16, 
    fontWeight: 'bold', 
    color: '#333',
  },
  produtoDetalhes: { 
    fontSize: 14, 
    color: '#666', 
    marginTop: 3,
  },
  codigoBarras: { 
    fontSize: 12, 
    color: '#999', 
    marginTop: 5,
  },
  precoContainer: { 
    marginTop: 10, 
    alignItems: 'flex-end',
  },
  preco: { 
    fontSize: 18, 
    fontWeight: 'bold', 
    color: '#4CAF50',
  },
  emptyContainer: { 
    alignItems: 'center', 
    marginTop: 80,
    paddingHorizontal: 40,
  },
  emptyText: { 
    fontSize: 16, 
    color: '#999', 
    marginTop: 10,
    textAlign: 'center',
  },
  emptyButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    marginTop: 20,
  },
  emptyButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  fab: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    backgroundColor: '#4CAF50',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
});

export default ProdutosScreen;