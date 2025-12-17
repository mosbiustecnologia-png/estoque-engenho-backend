/**
 * Tela de Cadastro de Produto
 */
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { produtosAPI, coresAPI, tiposAPI } from '../services/api';

const CadastrarProdutoScreen = ({ navigation }) => {
  const [nome, setNome] = useState('');
  const [tipoSelecionado, setTipoSelecionado] = useState(null);
  const [corSelecionada, setCorSelecionada] = useState(null);
  const [estoqueInicial, setEstoqueInicial] = useState('');
  const [estoqueMinimo, setEstoqueMinimo] = useState('');
  const [precoCusto, setPrecoCusto] = useState('');
  const [precoVenda, setPrecoVenda] = useState('');
  const [observacoes, setObservacoes] = useState('');

  const [tipos, setTipos] = useState([]);
  const [cores, setCores] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      setLoadingData(true);
      const [tiposData, coresData] = await Promise.all([
        tiposAPI.listar(),
        coresAPI.listar(),
      ]);
      setTipos(tiposData);
      setCores(coresData);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      Alert.alert('Erro', 'Não foi possível carregar tipos e cores');
    } finally {
      setLoadingData(false);
    }
  };

  const handleSubmit = async () => {
    // Validações
    if (!nome.trim()) {
      Alert.alert('Atenção', 'Digite o nome do produto');
      return;
    }

    if (!tipoSelecionado) {
      Alert.alert('Atenção', 'Selecione o tipo do produto');
      return;
    }

    if (!corSelecionada) {
      Alert.alert('Atenção', 'Selecione a cor do produto');
      return;
    }

    try {
      setLoading(true);

      const dados = {
        nome: nome.trim(),
        tipo_id: tipoSelecionado,
        cor_id: corSelecionada,
        estoque_inicial: parseInt(estoqueInicial) || 0,
        estoque_minimo: parseInt(estoqueMinimo) || 0,
        preco_custo: parseFloat(precoCusto) || 0,
        preco_venda: parseFloat(precoVenda) || 0,
        observacoes: observacoes || '',
      };

      console.log('📤 Enviando dados:', dados);

      // RETRY: tenta até 3 vezes
      let tentativas = 0;
      let sucesso = false;
      let resultado = null;

      while (tentativas < 3 && !sucesso) {
        try {
          tentativas++;
          console.log(`🔄 Tentativa ${tentativas}/3...`);
          
          resultado = await produtosAPI.criar(dados);
          sucesso = true;
          
        } catch (error) {
          console.error(`❌ Tentativa ${tentativas} falhou:`, error.message);
          
          if (tentativas === 3) {
            throw error; // Última tentativa falhou
          }
          
          // Espera 2 segundos antes de tentar de novo
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
      }

      Alert.alert(
        'Produto Cadastrado!',
        `Código gerado: ${resultado.codigo_barras}`,
        [
          { text: 'Cadastrar Outro', onPress: limparFormulario },
          { text: 'Ver Produtos', onPress: () => navigation.navigate('Produtos') }
        ]
      );

    } catch (error) {
      console.error('❌ Erro final ao cadastrar:', error);
      Alert.alert('Erro', 'Não foi possível cadastrar o produto após 3 tentativas.');
    } finally {
      setLoading(false);
    }
  };

  const limparFormulario = () => {
    setNome('');
    setTipoSelecionado(null);
    setCorSelecionada(null);
    setEstoqueInicial('');
    setEstoqueMinimo('');
    setPrecoCusto('');
    setPrecoVenda('');
    setObservacoes('');
  };

  if (loadingData) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Carregando...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.form}>
        {/* Nome */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Nome do Produto *</Text>
          <TextInput
            style={styles.input}
            value={nome}
            onChangeText={setNome}
            placeholder="Ex: Blusa Manga Longa"
            editable={!loading}
          />
        </View>

        {/* Tipo */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Tipo *</Text>
          <View style={styles.optionsGrid}>
            {tipos.map((tipo) => (
              <TouchableOpacity
                key={tipo.id}
                style={[
                  styles.optionButton,
                  tipoSelecionado === tipo.id && styles.optionButtonSelected,
                ]}
                onPress={() => setTipoSelecionado(tipo.id)}
                disabled={loading}
              >
                <Text
                  style={[
                    styles.optionText,
                    tipoSelecionado === tipo.id && styles.optionTextSelected,
                  ]}
                >
                  {tipo.nome}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Cor */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Cor *</Text>
          <View style={styles.optionsGrid}>
            {cores.map((cor) => (
              <TouchableOpacity
                key={cor.id}
                style={[
                  styles.optionButton,
                  corSelecionada === cor.id && styles.optionButtonSelected,
                ]}
                onPress={() => setCorSelecionada(cor.id)}
                disabled={loading}
              >
                <Text
                  style={[
                    styles.optionText,
                    corSelecionada === cor.id && styles.optionTextSelected,
                  ]}
                >
                  {cor.nome}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Estoque */}
        <View style={styles.row}>
          <View style={[styles.inputGroup, styles.halfWidth]}>
            <Text style={styles.label}>Estoque Inicial</Text>
            <TextInput
              style={styles.input}
              value={estoqueInicial}
              onChangeText={setEstoqueInicial}
              placeholder="0"
              keyboardType="number-pad"
              editable={!loading}
            />
          </View>

          <View style={[styles.inputGroup, styles.halfWidth]}>
            <Text style={styles.label}>Estoque Mínimo</Text>
            <TextInput
              style={styles.input}
              value={estoqueMinimo}
              onChangeText={setEstoqueMinimo}
              placeholder="0"
              keyboardType="number-pad"
              editable={!loading}
            />
          </View>
        </View>

        {/* Preços */}
        <View style={styles.row}>
          <View style={[styles.inputGroup, styles.halfWidth]}>
            <Text style={styles.label}>Preço Custo</Text>
            <TextInput
              style={styles.input}
              value={precoCusto}
              onChangeText={setPrecoCusto}
              placeholder="0.00"
              keyboardType="decimal-pad"
              editable={!loading}
            />
          </View>

          <View style={[styles.inputGroup, styles.halfWidth]}>
            <Text style={styles.label}>Preço Venda</Text>
            <TextInput
              style={styles.input}
              value={precoVenda}
              onChangeText={setPrecoVenda}
              placeholder="0.00"
              keyboardType="decimal-pad"
              editable={!loading}
            />
          </View>
        </View>

        {/* Observações */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Observações</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={observacoes}
            onChangeText={setObservacoes}
            placeholder="Informações adicionais (opcional)"
            multiline
            numberOfLines={3}
            editable={!loading}
          />
        </View>

        {/* Botão Cadastrar */}
        <TouchableOpacity
          style={[styles.submitButton, loading && styles.submitButtonDisabled]}
          onPress={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <>
              <ActivityIndicator color="#fff" />
              <Text style={styles.submitButtonText}>Cadastrando...</Text>
            </>
          ) : (
            <>
              <Ionicons name="checkmark-circle" size={24} color="#fff" />
              <Text style={styles.submitButtonText}>Cadastrar Produto</Text>
            </>
          )}
        </TouchableOpacity>

        {/* Botão Limpar */}
        {!loading && (
          <TouchableOpacity style={styles.clearButton} onPress={limparFormulario}>
            <Text style={styles.clearButtonText}>Limpar Formulário</Text>
          </TouchableOpacity>
        )}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
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
  form: {
    padding: 20,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
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
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  optionButton: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 20,
  },
  optionButtonSelected: {
    backgroundColor: '#4CAF50',
    borderColor: '#4CAF50',
  },
  optionText: {
    fontSize: 14,
    color: '#333',
    fontWeight: '600',
  },
  optionTextSelected: {
    color: '#fff',
  },
  row: {
    flexDirection: 'row',
    gap: 10,
  },
  halfWidth: {
    flex: 1,
  },
  submitButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 18,
    borderRadius: 12,
    gap: 10,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
  },
  submitButtonDisabled: {
    backgroundColor: '#ccc',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  clearButton: {
    padding: 15,
    marginTop: 10,
    alignItems: 'center',
  },
  clearButtonText: {
    color: '#666',
    fontSize: 16,
  },
});

export default CadastrarProdutoScreen;