# 🏭 Estoque Engenho - Backend API

Sistema completo de controle de estoque com geração automática de código de barras.

## 📋 Funcionalidades

- ✅ Cadastro de produtos com geração automática de código de barras
- ✅ Controle de entrada e saída de estoque
- ✅ Geração de etiquetas para impressão
- ✅ Histórico completo de movimentações
- ✅ Relatórios de estoque baixo
- ✅ Busca por código de barras
- ✅ Gestão de cores e tipos de produtos

## 🚀 Como Rodar

### Opção 1: Com Docker (Recomendado)

```bash
# Clone o repositório
cd estoque-engenho/backend

# Copie o arquivo de configuração
cp .env.example .env

# Inicie os containers
docker-compose up -d

# A API estará disponível em http://localhost:8000
# Documentação em http://localhost:8000/docs
```

### Opção 2: Sem Docker (Manual)

```bash
# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados MySQL
# Execute o script database/schema.sql no seu MySQL

# Configure o arquivo .env
cp .env.example .env
# Edite o .env com suas configurações de banco

# Rode a aplicação
python main.py

# Ou com uvicorn
uvicorn main:app --reload
```

## 🗄️ Estrutura do Banco de Dados

```
estoque_engenho/
├── cores          # Cores dos produtos (preto, branco, etc)
├── tipos          # Tipos/categorias (blusa, calça, etc)
├── produtos       # Produtos cadastrados
└── movimentacoes  # Histórico de entrada/saída
```

## 📊 Formato do Código de Barras

O código de barras é gerado automaticamente no formato:

```
PPPPTTCC
│   │ │
│   │ └─ Código da Cor (2 dígitos)
│   └─── Código do Tipo (2 dígitos)
└─────── Código do Produto (4 dígitos)
```

**Exemplo:**
- Produto #0001
- Tipo: Blusa (01)
- Cor: Preto (01)
- **Código de Barras: 00010101**

## 🔌 Principais Endpoints

### Produtos
- `GET /produtos` - Lista produtos
- `GET /produtos/{id}` - Busca produto por ID
- `GET /produtos/codigo-barras/{codigo}` - Busca por código de barras
- `POST /produtos` - Cria novo produto
- `PUT /produtos/{id}` - Atualiza produto
- `GET /produtos/{id}/etiqueta` - Gera etiqueta para impressão
- `GET /produtos/baixo-estoque` - Lista produtos com estoque baixo

### Movimentações
- `POST /movimentacoes/entrada` - Registra entrada de estoque
- `POST /movimentacoes/saida` - Registra saída de estoque
- `POST /movimentacoes/ajuste` - Ajusta estoque
- `GET /movimentacoes` - Lista movimentações
- `GET /movimentacoes/produto/{id}/historico` - Histórico do produto

### Cores e Tipos
- `GET /cores` - Lista cores
- `POST /cores` - Cria nova cor
- `GET /tipos` - Lista tipos
- `POST /tipos` - Cria novo tipo

## 📱 Exemplo de Uso - Entrada de Estoque

```bash
# Dar entrada de 10 unidades do produto
curl -X POST http://localhost:8000/movimentacoes/entrada \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_barras": "00010101",
    "quantidade": 10,
    "observacao": "Chegou do fornecedor",
    "usuario": "Maria"
  }'
```

## 📱 Exemplo de Uso - Criar Produto

```bash
curl -X POST http://localhost:8000/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Blusa Manga Longa Feminina",
    "tipo_id": 1,
    "cor_id": 1,
    "estoque_inicial": 50,
    "estoque_minimo": 10,
    "preco_custo": 25.00,
    "preco_venda": 59.90
  }'
```

## 🖨️ Geração de Etiquetas

A API gera etiquetas prontas para impressão com:
- Nome do produto
- Tipo e cor
- Preço
- Código de barras (Code 128)

```bash
# Gerar etiqueta
curl http://localhost:8000/produtos/1/etiqueta

# Retorna imagem em base64 pronta para impressão
```

## 🌐 Deploy Online (Gratuito)

### Railway.app

1. Crie conta no [Railway](https://railway.app)
2. Conecte seu repositório GitHub
3. Adicione um serviço MySQL
4. Configure as variáveis de ambiente
5. Deploy automático! 🚀

### Render.com

1. Crie conta no [Render](https://render.com)
2. Crie um Web Service
3. Adicione PostgreSQL (gratuito)
4. Configure variáveis de ambiente
5. Deploy! 🎉

## 🔧 Variáveis de Ambiente

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=estoque_engenho

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# CORS (domínios permitidos)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19006
```

## 📚 Documentação Interativa

Acesse `/docs` para ver a documentação Swagger completa com exemplos e testes!

## 🐛 Troubleshooting

### Erro de conexão com banco
- Verifique se o MySQL está rodando
- Confira as credenciais no arquivo `.env`

### Erro ao gerar código de barras
- Certifique-se de ter instalado todas as dependências: `pip install -r requirements.txt`

### Porta já em uso
- Altere a porta no `.env` ou no `docker-compose.yml`

## 📞 Próximos Passos

Agora você pode:
1. ✅ Rodar a API localmente
2. ✅ Testar os endpoints no `/docs`
3. ✅ Fazer deploy online
4. 📱 Criar o app mobile!

---

Desenvolvido com ❤️ para controle de estoque eficiente
