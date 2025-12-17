export const API_URL = 'http://192.168.15.6:8000';

export const API_ENDPOINTS = {
  PRODUTOS: '/produtos',
  PRODUTO_BY_ID: (id) => `/produtos/${id}`,
  PRODUTO_BY_BARCODE: (codigo) => `/produtos/codigo-barras/${codigo}`,
  PRODUTOS_BAIXO_ESTOQUE: '/produtos/baixo-estoque',
  MOVIMENTACOES: '/movimentacoes',
  ENTRADA: '/movimentacoes/entrada',
  SAIDA: '/movimentacoes/saida',
  AJUSTE: '/movimentacoes/ajuste',
  MOVIMENTACOES_RECENTES: '/movimentacoes/recentes',
  CORES: '/cores',
  TIPOS: '/tipos',
};