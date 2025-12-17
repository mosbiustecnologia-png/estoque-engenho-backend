/**
 * Tela de Geração de Etiquetas - COM PDF
 */
import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  Linking,
  Clipboard,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { produtosAPI } from '../services/api';
import { API_URL } from '../config/api';

const EtiquetasScreen = () => {
  const [produtos, setProdutos] = useState([]);
  const [selecionados, setSelecionados] = useState([]);
  const [loading, setLoading] = useState(true);

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
    }
  };

  const toggleSelecao = (produtoId) => {
    if (selecionados.includes(produtoId)) {
      setSelecionados(selecionados.filter(id => id !== produtoId));
    } else {
      setSelecionados([...selecionados, produtoId]);
    }
  };

  const selecionarTodos = () => {
    if (selecionados.length === produtos.length) {
      setSelecionados([]);
    } else {
      setSelecionados(produtos.map(p => p.id));
    }
  };

  const abrirEtiqueta = (produto) => {
    const url = `${API_URL}/produtos/${produto.id}/etiqueta`;
    
    Alert.alert(
      `🏷️ ${produto.nome}`,
      `Código: ${produto.codigo_barras}\n\nAbrindo etiqueta no navegador...`,
      [
        {
          text: 'Abrir',
          onPress: () => Linking.openURL(url)
        },
        { text: 'Cancelar', style: 'cancel' }
      ]
    );
  };

  const gerarTodasEtiquetas = () => {
    if (selecionados.length === 0) {
      Alert.alert('Atenção', 'Selecione pelo menos um produto');
      return;
    }

    Alert.alert(
      '🖨️ Gerar Etiquetas',
      `${selecionados.length} produto(s) selecionado(s).\n\nComo deseja gerar?`,
      [
        {
          text: 'PDF Único',
          onPress: () => gerarPDF(),
        },
        {
          text: 'Individual',
          onPress: () => gerarIndividual(),
        },
        {
          text: 'Cancelar',
          style: 'cancel',
        }
      ]
    );
  };

  const gerarPDF = () => {
    const url = `${API_URL}/produtos/etiquetas-pdf`;
    
    Alert.alert(
      '📄 PDF com Todas as Etiquetas',
      `Gerando PDF com ${selecionados.length} etiqueta(s)...\n\nVocê pode:\n\n1. Abrir a documentação da API\n2. Usar o endpoint POST /produtos/etiquetas-pdf\n3. Enviar os IDs: [${selecionados.join(', ')}]`,
      [
        {
          text: 'Copiar IDs',
          onPress: () => {
            const idsText = JSON.stringify(selecionados);
            Clipboard.setString(idsText);
            Alert.alert(
              '✅ IDs Copiados!',
              `Cole isso no navegador em:\n${API_URL}/docs\n\nProcure: POST /produtos/etiquetas-pdf\nClique em "Try it out"\nCole os IDs\nClique em "Execute"\nBaixe o PDF!`
            );
          }
        },
        {
          text: 'Abrir Documentação',
          onPress: () => {
            Linking.openURL(`${API_URL}/docs`);
            setTimeout(() => {
              Alert.alert(
                '💡 Instruções',
                `1. Procure: POST /produtos/etiquetas-pdf\n2. Clique em "Try it out"\n3. Cole: ${JSON.stringify(selecionados)}\n4. Clique em "Execute"\n5. Baixe o PDF!`
              );
            }, 1000);
          }
        }
      ]
    );
  };

  const gerarIndividual = async () => {
    Alert.alert(
      '📱 Abrindo Etiquetas',
      `Abrindo ${selecionados.length} etiqueta(s) individualmente...\n\nCada uma abrirá em uma nova aba.`,
      [
        {
          text: 'OK',
          onPress: async () => {
            for (const id of selecionados) {
              await Linking.openURL(`${API_URL}/produtos/${id}/etiqueta`);
              await new Promise(resolve => setTimeout(resolve, 500));
            }
          }
        },
        { text: 'Cancelar', style: 'cancel' }
      ]
    );
  };

  const renderProduto = ({ item }) => {
    const isSelected = selecionados.includes(item.id);

    return (
      <View style={styles.produtoWrapper}>
        <TouchableOpacity
          style={[styles.produtoCard, isSelected && styles.produtoCardSelected]}
          onPress={() => toggleSelecao(item.id)}
        >
          <Ionicons 
            name={isSelected ? "checkbox" : "square-outline"} 
            size={28} 
            color={isSelected ? "#4CAF50" : "#ccc"} 
          />
          
          <View style={styles.produtoInfo}>
            <Text style={styles.produtoNome}>{item.nome}</Text>
            <Text style={styles.produtoDetalhes}>
              {item.tipo?.nome} • {item.cor?.nome}
            </Text>
            <Text style={styles.codigoBarras}>📊 {item.codigo_barras}</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.abrirButton}
          onPress={() => abrirEtiqueta(item)}
        >
          <Ionicons name="open-outline" size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    );
  };

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
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.headerButton}
          onPress={selecionarTodos}
        >
          <Ionicons 
            name={selecionados.length === produtos.length ? "checkbox" : "square-outline"} 
            size={24} 
            color="#4CAF50" 
          />
          <Text style={styles.headerButtonText}>
            {selecionados.length === produtos.length ? 'Desmarcar' : 'Selecionar Todos'}
          </Text>
        </TouchableOpacity>

        <Text style={styles.contador}>
          {selecionados.length} selecionado(s)
        </Text>
      </View>

      {/* Instruções */}
      <View style={styles.instrucoes}>
        <Ionicons name="information-circle" size={20} color="#2196F3" />
        <Text style={styles.instrucoesText}>
          Toque para selecionar • Botão azul para abrir etiqueta individual
        </Text>
      </View>

      {/* Lista */}
      <FlatList
        data={produtos}
        renderItem={renderProduto}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="pricetag-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>Nenhum produto cadastrado</Text>
          </View>
        }
      />

      {/* Botão Gerar */}
      {selecionados.length > 0 && (
        <TouchableOpacity
          style={styles.gerarButton}
          onPress={gerarTodasEtiquetas}
        >
          <Ionicons name="print" size={24} color="#fff" />
          <Text style={styles.gerarButtonText}>
            Gerar {selecionados.length} Etiqueta(s)
          </Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  loadingContainer: { 
    flex: 1, 
    justifyContent: 'center', 
    alignItems: 'center' 
  },
  loadingText: { marginTop: 10, fontSize: 16, color: '#666' },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  headerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  headerButtonText: {
    fontSize: 14,
    color: '#4CAF50',
    fontWeight: '600',
  },
  contador: {
    fontSize: 14,
    color: '#666',
    fontWeight: '600',
  },
  instrucoes: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E3F2FD',
    padding: 12,
    gap: 10,
  },
  instrucoesText: {
    fontSize: 13,
    color: '#1976D2',
    flex: 1,
  },
  produtoWrapper: {
    flexDirection: 'row',
    marginHorizontal: 15,
    marginBottom: 10,
    gap: 10,
  },
  produtoCard: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#eee',
    gap: 12,
  },
  produtoCardSelected: {
    borderColor: '#4CAF50',
    backgroundColor: '#f1f8f4',
  },
  produtoInfo: { flex: 1 },
  produtoNome: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  produtoDetalhes: { fontSize: 14, color: '#666', marginTop: 3 },
  codigoBarras: { fontSize: 12, color: '#999', marginTop: 5 },
  abrirButton: {
    backgroundColor: '#2196F3',
    width: 50,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 12,
  },
  emptyContainer: { 
    alignItems: 'center', 
    marginTop: 80,
    paddingHorizontal: 40 
  },
  emptyText: { 
    fontSize: 16, 
    color: '#999', 
    marginTop: 10,
    textAlign: 'center' 
  },
  gerarButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 18,
    marginHorizontal: 15,
    marginBottom: 15,
    borderRadius: 12,
    gap: 10,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  gerarButtonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
});

export default EtiquetasScreen;