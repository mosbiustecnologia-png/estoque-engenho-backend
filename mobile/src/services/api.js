import axios from 'axios';
import { API_URL, API_ENDPOINTS } from '../config/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

if (__DEV__) {
  api.interceptors.request.use(
    (config) => {
      console.log(`📡 ${config.method.toUpperCase()} ${config.url}`);
      return config;
    },
    (error) => {
      console.error('❌ Erro na requisição:', error);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    (response) => {
      console.log(`✅ Resposta: ${response.status}`);
      return response;
    },
    (error) => {
      console.error('❌ Erro na resposta:', error.response?.status);
      return Promise.reject(error);
    }
  );
}

export const produtosAPI = {
  listar: async (filtros = {}) => {
    const params = new URLSearchParams(filtros).toString();
    const response = await api.get(`${API_ENDPOINTS.PRODUTOS}?${params}`);
    return response.data;
  },

  buscarPorId: async (id) => {
    const response = await api.get(API_ENDPOINTS.PRODUTO_BY_ID(id));
    return response.data;
  },

  buscarPorCodigoBarras: async (codigo) => {
    const response = await api.get(API_ENDPOINTS.PRODUTO_BY_BARCODE(codigo));
    return response.data;
  },

  criar: async (produto) => {
    const response = await api.post(API_ENDPOINTS.PRODUTOS, produto);
    return response.data;
  },

  atualizar: async (id, produto) => {
    const response = await api.put(API_ENDPOINTS.PRODUTO_BY_ID(id), produto);
    return response.data;
  },

  listarBaixoEstoque: async () => {
    const response = await api.get(API_ENDPOINTS.PRODUTOS_BAIXO_ESTOQUE);
    return response.data;
  },

  buscar: async (termo) => {
    const response = await api.get(`${API_ENDPOINTS.PRODUTOS}?busca=${termo}`);
    return response.data;
  },

  gerarPdfEtiquetas: async (produtoIds) => {
    const response = await api.post('/produtos/etiquetas-pdf', produtoIds, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export const movimentacoesAPI = {
  listar: async (filtros = {}) => {
    const params = new URLSearchParams(filtros).toString();
    const response = await api.get(`${API_ENDPOINTS.MOVIMENTACOES}?${params}`);
    return response.data;
  },

  entrada: async (dados) => {
    const response = await api.post(API_ENDPOINTS.ENTRADA, dados);
    return response.data;
  },

  saida: async (dados) => {
    const response = await api.post(API_ENDPOINTS.SAIDA, dados);
    return response.data;
  },

  ajuste: async (dados) => {
    const response = await api.post(API_ENDPOINTS.AJUSTE, dados);
    return response.data;
  },

  recentes: async (horas = 24) => {
    const response = await api.get(`${API_ENDPOINTS.MOVIMENTACOES_RECENTES}?horas=${horas}`);
    return response.data;
  },
};

export const coresAPI = {
  listar: async () => {
    const response = await api.get(API_ENDPOINTS.CORES);
    return response.data;
  },

  criar: async (cor) => {
    const response = await api.post(API_ENDPOINTS.CORES, cor);
    return response.data;
  },
};

export const tiposAPI = {
  listar: async () => {
    const response = await api.get(API_ENDPOINTS.TIPOS);
    return response.data;
  },

  criar: async (tipo) => {
    const response = await api.post(API_ENDPOINTS.TIPOS, tipo);
    return response.data;
  },
};

export const verificarConexao = async () => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch (error) {
    return false;
  }
};

export default api;