/**
 * Tela Inicial - Dashboard
 */
import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { produtosAPI, movimentacoesAPI } from '../services/api';

const HomeScreen = ({ navigation }) => {
  const [stats, setStats] = useState({
    totalProdutos: 0,
    produtosBaixoEstoque: 0,
    movimentacoesHoje: 0,
  });
  const [produtosBaixoEstoque, setProdutosBaixoEstoque] = useState([]);
  const [movimentacoesRecentes, setMovimentacoesRecentes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useFocusEffect(
    useCallback(() => {
      carregarDados();
    }, [])
  );

  const carregarDados = async () => {
    try {
      setLoading(true);

      // Carrega produtos
      const produtos = await produtosAPI.listar();
      
      // Carrega produtos com baixo estoque
      const baixoEstoque = await produtosAPI.listarBaixoEstoque();
      
      // Carrega movimentações recentes
      const movimentacoes = await movimentacoesAPI.recentes(24);

      setStats({
        totalProdutos: produtos.length,
        produtosBaixoEstoque: baixoEstoque.length,
        movimentacoesHoje: movimentacoes.length,
      });

      setProdutosBaixoEstoque(baixoEstoque.slice(0, 5)); // Apenas 5 primeiros
      setMovimentacoesRecentes(movimentacoes.slice(0, 5)); // Apenas 5 primeiros

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      Alert.alert('Erro', 'Não foi possível carregar os dados');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    carregarDados();
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Bem-vindo ao</Text>
        <Text style={styles.appName}>Estoque Engenho</Text>
      </View>

      {/* Cards de Estatísticas */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Ionicons name="cube-outline" size={32} color="#4CAF50" />
          <Text style={styles.statNumber}>{stats.totalProdutos}</Text>
          <Text style={styles.statLabel}>Produtos</Text>
        </View>

        <View style={styles.statCard}>
          <Ionicons name="warning-outline" size={32} color="#FF9800" />
          <Text style={styles.statNumber}>{stats.produtosBaixoEstoque}</Text>
          <Text style={styles.statLabel}>Estoque Baixo</Text>
        </View>

        <View style={styles.statCard}>
          <Ionicons name="swap-horizontal-outline" size={32} color="#2196F3" />
          <Text style={styles.statNumber}>{stats.movimentacoesHoje}</Text>
          <Text style={styles.statLabel}>Movimentações</Text>
        </View>
      </View>

      {/* Cards de Ações Rápidas */}
      <View style={styles.actionsGrid}>
        <TouchableOpacity 
          style={[styles.actionCard, { backgroundColor: '#4CAF50' }]}
          onPress={() => navigation.navigate('Entrada')}
        >
          <Ionicons name="arrow-down-circle" size={32} color="#fff" />
          <Text style={styles.actionTitle}>Entrada</Text>
          <Text style={styles.actionSubtitle}>Adicionar estoque</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.actionCard, { backgroundColor: '#F44336' }]}
          onPress={() => navigation.navigate('Saida')}
        >
          <Ionicons name="arrow-up-circle" size={32} color="#fff" />
          <Text style={styles.actionTitle}>Saída</Text>
          <Text style={styles.actionSubtitle}>Registrar venda</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.actionCard, { backgroundColor: '#2196F3' }]}
          onPress={() => navigation.navigate('CadastrarProduto')}
        >
          <Ionicons name="add-circle" size={32} color="#fff" />
          <Text style={styles.actionTitle}>Novo Produto</Text>
          <Text style={styles.actionSubtitle}>Cadastrar</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.actionCard, { backgroundColor: '#FF9800' }]}
          onPress={() => navigation.navigate('Produtos')}
        >
          <Ionicons name="cube" size={32} color="#fff" />
          <Text style={styles.actionTitle}>Produtos</Text>
          <Text style={styles.actionSubtitle}>Ver lista</Text>
        </TouchableOpacity>
      </View>

      {/* Produtos com Estoque Baixo */}
      {produtosBaixoEstoque.length > 0 && (
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>⚠️ Estoque Baixo</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Produtos')}>
              <Text style={styles.sectionLink}>Ver todos</Text>
            </TouchableOpacity>
          </View>

          {produtosBaixoEstoque.map((produto) => (
            <View key={produto.id} style={styles.produtoItem}>
              <View style={styles.produtoInfo}>
                <Text style={styles.produtoNome}>{produto.nome}</Text>
                <Text style={styles.produtoDetalhes}>
                  {produto.tipo?.nome} • {produto.cor?.nome}
                </Text>
              </View>
              <View style={styles.estoqueInfo}>
                <Text style={styles.estoqueAtual}>{produto.estoque_atual}</Text>
                <Text style={styles.estoqueLabel}>unidades</Text>
              </View>
            </View>
          ))}
        </View>
      )}

      {/* Movimentações Recentes */}
      {movimentacoesRecentes.length > 0 && (
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>📊 Últimas Movimentações</Text>
          </View>

          {movimentacoesRecentes.map((mov) => (
            <View key={mov.id} style={styles.movimentacaoItem}>
              <View style={[
                styles.movIcon,
                mov.tipo_movimento === 'ENTRADA' 
                  ? styles.movIconEntrada 
                  : styles.movIconSaida
              ]}>
                <Ionicons 
                  name={mov.tipo_movimento === 'ENTRADA' ? 'arrow-down' : 'arrow-up'} 
                  size={16} 
                  color="#fff" 
                />
              </View>
              <View style={styles.movInfo}>
                <Text style={styles.movProduto}>{mov.produto?.nome}</Text>
                <Text style={styles.movDetalhes}>
                  {mov.tipo_movimento} • {mov.quantidade} unidades
                </Text>
              </View>
            </View>
          ))}
        </View>
      )}

      {/* Espaçamento final */}
      <View style={{ height: 30 }} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#4CAF50',
    padding: 30,
    paddingTop: 50,
  },
  welcomeText: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: 'row',
    padding: 15,
    gap: 10,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    gap: 10,
  },
  actionCard: {
    width: '48%',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 10,
  },
  actionSubtitle: {
    fontSize: 12,
    color: '#fff',
    opacity: 0.9,
    marginTop: 5,
  },
  section: {
    padding: 15,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  sectionLink: {
    fontSize: 14,
    color: '#4CAF50',
    fontWeight: '600',
  },
  produtoItem: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 8,
    marginBottom: 8,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 1,
  },
  produtoInfo: {
    flex: 1,
  },
  produtoNome: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  produtoDetalhes: {
    fontSize: 14,
    color: '#666',
    marginTop: 3,
  },
  estoqueInfo: {
    alignItems: 'flex-end',
  },
  estoqueAtual: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FF9800',
  },
  estoqueLabel: {
    fontSize: 12,
    color: '#666',
  },
  movimentacaoItem: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 1,
  },
  movIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  movIconEntrada: {
    backgroundColor: '#4CAF50',
  },
  movIconSaida: {
    backgroundColor: '#F44336',
  },
  movInfo: {
    flex: 1,
  },
  movProduto: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  movDetalhes: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
});

export default HomeScreen;