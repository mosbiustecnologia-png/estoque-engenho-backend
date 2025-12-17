/**
 * Tela de Entrada de Estoque
 */
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Modal,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import BarcodeScanner from '../components/BarcodeScanner';
import { produtosAPI, movimentacoesAPI } from '../services/api';

const EntradaScreen = ({ navigation }) => {
  const [showScanner, setShowScanner] = useState(false);
  const [codigoBarras, setCodigoBarras] = useState('');
  const [produto, setProduto] = useState(null);
  const [quantidade, setQuantidade] = useState('');
  const [observacoes, setObservacoes] = useState('');
  const [loading, setLoading] = useState(false);

  const handleScan = async (codigo) => {
    console.log('Código escaneado:', codigo);
    setCodigoBarras(codigo);
    setShowScanner(false);
    await buscarProduto(codigo);
  };

  const buscarProduto = async (codigo) => {
    try {
      setLoading(true);
      const produtoEncontrado = await produtosAPI.buscarPorCodigoBarras(codigo);
      setProduto(produtoEncontrado);
    } catch (error) {
      console.error('Erro ao buscar produto:', error);
      Alert.alert(
        'Produto não encontrado',
        `O código ${codigo} não foi encontrado no sistema.`,
        [
          { text: 'OK', onPress: () => limparFormulario() }
        ]
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!produto) {
      Alert.alert('Atenção', 'Busque um produto primeiro');
      return;
    }

    if (!quantidade || parseInt(quantidade) <= 0) {
      Alert.alert('Atenção', 'Digite uma quantidade válida');
      return;
    }

    try {
      setLoading(true);

      const dados = {
        produto_id: produto.id,
        codigo_barras: produto.codigo_barras,
        tipo_movimento: 'ENTRADA',
        quantidade: parseInt(quantidade),
        observacoes: observacoes || '',
      };

      await movimentacoesAPI.entrada(dados);

      const novoEstoque = produto.estoque_atual + parseInt(quantidade);

      Alert.alert(
        'Entrada Registrada!',
        `${quantidade} unidade(s) adicionada(s) de ${produto.nome}\nNovo estoque: ${novoEstoque}`,
        [
          { text: 'Nova Entrada', onPress: () => limparFormulario() },
          { text: 'Voltar', onPress: () => navigation.goBack() }
        ]
      );

    } catch (error) {
      console.error('Erro ao registrar entrada:', error);
      Alert.alert('Erro', 'Não foi possível registrar a entrada.');
    } finally {
      setLoading(false);
    }
  };

  const limparFormulario = () => {
    setCodigoBarras('');
    setProduto(null);
    setQuantidade('');
    setObservacoes('');
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView style={styles.scrollView}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerIcon}>
            <Ionicons name="arrow-down-circle" size={40} color="#4CAF50" />
          </View>
          <Text style={styles.headerTitle}>Entrada de Estoque</Text>
          <Text style={styles.headerSubtitle}>
            Adicione produtos ao estoque
          </Text>
        </View>

        {/* Scanner/Input de Código */}
        <View style={styles.section}>
          <Text style={styles.label}>Código de Barras</Text>
          
          <View style={styles.barcodeInputContainer}>
            <TextInput
              style={styles.barcodeInput}
              value={codigoBarras}
              onChangeText={setCodigoBarras}
              placeholder="Digite ou escaneie o código"
              keyboardType="numeric"
              editable={!loading}
            />
            <TouchableOpacity
              style={styles.scanButton}
              onPress={() => setShowScanner(true)}
              disabled={loading}
            >
              <Ionicons name="scan" size={24} color="#fff" />
            </TouchableOpacity>
          </View>

          {codigoBarras && !produto && (
            <TouchableOpacity
              style={styles.searchButton}
              onPress={() => buscarProduto(codigoBarras)}
              disabled={loading}
            >
              <Text style={styles.searchButtonText}>Buscar Produto</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Informações do Produto */}
        {produto && (
          <View style={styles.produtoCard}>
            <View style={styles.produtoHeader}>
              <Ionicons name="cube" size={32} color="#4CAF50" />
              <View style={styles.produtoInfo}>
                <Text style={styles.produtoNome}>{produto.nome}</Text>
                <Text style={styles.produtoDetalhes}>
                  {produto.tipo.nome} • {produto.cor.nome}
                </Text>
              </View>
            </View>

            <View style={styles.produtoStats}>
              <View style={styles.statItem}>
                <Text style={styles.statLabel}>Estoque Atual</Text>
                <Text style={[
                  styles.statValue,
                  produto.estoque_atual <= produto.estoque_minimo && styles.statValueWarning
                ]}>
                  {produto.estoque_atual}
                </Text>
              </View>
              <View style={styles.statDivider} />
              <View style={styles.statItem}>
                <Text style={styles.statLabel}>Estoque Mínimo</Text>
                <Text style={styles.statValue}>{produto.estoque_minimo}</Text>
              </View>
            </View>

            {produto.estoque_atual <= produto.estoque_minimo && (
              <View style={styles.warningBanner}>
                <Ionicons name="warning" size={20} color="#FF9800" />
                <Text style={styles.warningText}>Estoque baixo!</Text>
              </View>
            )}
          </View>
        )}

        {/* Quantidade */}
        <View style={styles.section}>
          <Text style={styles.label}>Quantidade *</Text>
          <TextInput
            style={styles.input}
            value={quantidade}
            onChangeText={setQuantidade}
            placeholder="Quantidade a adicionar"
            keyboardType="number-pad"
            editable={!loading && produto !== null}
          />

          {/* Botões rápidos */}
          <View style={styles.quickButtons}>
            {[1, 5, 10, 20].map((val) => (
              <TouchableOpacity
                key={val}
                style={styles.quickButton}
                onPress={() => setQuantidade(val.toString())}
                disabled={!produto}
              >
                <Text style={styles.quickButtonText}>+{val}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Observação */}
        <View style={styles.section}>
          <Text style={styles.label}>Observação (opcional)</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={observacoes}
            onChangeText={setObservacoes}
            placeholder="Ex: Compra fornecedor, Devolução"
            multiline
            numberOfLines={3}
            editable={!loading}
          />
        </View>

        {/* Botão Confirmar */}
        <TouchableOpacity
          style={[
            styles.confirmButton,
            (!produto || !quantidade || loading) && styles.confirmButtonDisabled
          ]}
          onPress={handleSubmit}
          disabled={!produto || !quantidade || loading}
        >
          <Ionicons name="checkmark-circle" size={24} color="#fff" />
          <Text style={styles.confirmButtonText}>
            {loading ? 'Processando...' : 'Confirmar Entrada'}
          </Text>
        </TouchableOpacity>

        {/* Botão Limpar */}
        {(produto || codigoBarras) && (
          <TouchableOpacity
            style={styles.clearButton}
            onPress={limparFormulario}
          >
            <Text style={styles.clearButtonText}>Limpar Formulário</Text>
          </TouchableOpacity>
        )}
      </ScrollView>

      {/* Scanner Modal */}
      <Modal
        visible={showScanner}
        animationType="slide"
        onRequestClose={() => setShowScanner(false)}
      >
        <BarcodeScanner
          onScan={handleScan}
          onClose={() => setShowScanner(false)}
          title="Escaneie o código do produto"
        />
      </Modal>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  headerIcon: {
    marginBottom: 10,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  section: {
    padding: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 10,
  },
  barcodeInputContainer: {
    flexDirection: 'row',
    gap: 10,
  },
  barcodeInput: {
    flex: 1,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    fontSize: 16,
  },
  scanButton: {
    backgroundColor: '#4CAF50',
    width: 56,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchButton: {
    backgroundColor: '#2196F3',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  searchButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  produtoCard: {
    backgroundColor: '#fff',
    marginHorizontal: 20,
    padding: 20,
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  produtoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  produtoInfo: {
    marginLeft: 15,
    flex: 1,
  },
  produtoNome: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  produtoDetalhes: {
    fontSize: 14,
    color: '#666',
    marginTop: 3,
  },
  produtoStats: {
    flexDirection: 'row',
    borderTopWidth: 1,
    borderTopColor: '#eee',
    paddingTop: 15,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginTop: 5,
  },
  statValueWarning: {
    color: '#FF9800',
  },
  statDivider: {
    width: 1,
    backgroundColor: '#eee',
  },
  warningBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF3E0',
    padding: 10,
    borderRadius: 8,
    marginTop: 15,
    gap: 10,
  },
  warningText: {
    color: '#FF9800',
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    fontSize: 16,
  },
  textArea: {
    height: 80,
    textAlignVertical: 'top',
  },
  quickButtons: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 10,
  },
  quickButton: {
    flex: 1,
    backgroundColor: '#E8F5E9',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  quickButtonText: {
    color: '#4CAF50',
    fontSize: 16,
    fontWeight: '600',
  },
  confirmButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 18,
    marginHorizontal: 20,
    borderRadius: 12,
    gap: 10,
  },
  confirmButtonDisabled: {
    backgroundColor: '#ccc',
  },
  confirmButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  clearButton: {
    padding: 15,
    marginHorizontal: 20,
    marginTop: 10,
    marginBottom: 30,
    alignItems: 'center',
  },
  clearButtonText: {
    color: '#666',
    fontSize: 16,
  },
});

export default EntradaScreen;