# 🏭 ESTOQUE ENGENHO - GUIA DE INÍCIO RÁPIDO

## 🎉 Parabéns! Seu sistema está pronto!

Criei um sistema completo de controle de estoque com código de barras para a loja da sua esposa.

---

## 📦 O QUE FOI CRIADO?

### ✅ Backend API (Pronto!)
- Sistema completo em FastAPI
- Banco de dados MySQL
- Geração automática de código de barras
- Endpoints para entrada/saída de estoque
- Geração de etiquetas para impressão
- Histórico completo de movimentações

### 📱 Próximo: App Mobile
- React Native (Android + iPhone)
- Scanner de código de barras
- Interface simples e rápida

---

## 🚀 COMO COMEÇAR - 3 PASSOS

### Passo 1: Rode Localmente (Testando)

```bash
# Entre na pasta
cd estoque-engenho/backend

# Copie as configurações
cp .env.example .env

# Suba com Docker (mais fácil!)
docker-compose up -d

# Pronto! API rodando em http://localhost:8000
```

**Acesse:** http://localhost:8000/docs para ver a documentação interativa

### Passo 2: Teste a API

```bash
# Rode o script de teste
python test_api.py
```

Isso vai:
- Criar um produto de exemplo
- Dar entrada no estoque
- Dar saída
- Mostrar como funciona!

### Passo 3: Coloque Online (Grátis!)

Siga o guia completo em: `DEPLOY.md`

**Mais fácil:** Railway.app
1. Crie conta em https://railway.app
2. Conecte seu GitHub
3. Adicione MySQL
4. Deploy automático! 🎉

---

## 📊 COMO FUNCIONA O CÓDIGO DE BARRAS

### Formato: PPPPTTCC (8 dígitos)

```
Exemplo: 00010101
         │   │ │
         │   │ └─ Cor: 01 (Preto)
         │   └─── Tipo: 01 (Blusa)
         └─────── Produto: 0001
```

### Processo:

1. **Cadastra o produto** → Sistema gera código automaticamente
2. **Imprime etiqueta** → Cola no saquinho
3. **Entrada:** Escaneia código → Adiciona quantidade
4. **Saída/Venda:** Escaneia código → Dá baixa no estoque

---

## 🎯 PRINCIPAIS FUNCIONALIDADES

### 1. Cadastrar Produto
```bash
POST /produtos
{
  "nome": "Blusa Manga Longa Preta",
  "tipo_id": 1,      # Blusa
  "cor_id": 1,       # Preto
  "estoque_inicial": 20,
  "preco_custo": 25.00,
  "preco_venda": 59.90
}
```
**Retorna:** Produto com código de barras gerado!

### 2. Dar Entrada no Estoque
```bash
POST /movimentacoes/entrada
{
  "codigo_barras": "00010101",
  "quantidade": 15,
  "observacao": "Chegou do fornecedor"
}
```

### 3. Dar Saída (Venda)
```bash
POST /movimentacoes/saida
{
  "codigo_barras": "00010101",
  "quantidade": 3,
  "observacao": "Venda loja"
}
```

### 4. Gerar Etiqueta
```bash
GET /produtos/1/etiqueta
```
**Retorna:** Imagem pronta para imprimir!

---

## 📂 ESTRUTURA DO PROJETO

```
estoque-engenho/
├── backend/
│   ├── app/
│   │   ├── routers/         # Endpoints da API
│   │   ├── services/        # Gerador de código de barras
│   │   ├── models.py        # Estrutura do banco
│   │   ├── schemas.py       # Validação de dados
│   │   └── database.py      # Conexão com banco
│   ├── database/
│   │   └── schema.sql       # Script do banco
│   ├── main.py              # Aplicação principal
│   ├── requirements.txt     # Dependências
│   ├── Dockerfile           # Container
│   ├── docker-compose.yml   # Orquestração
│   ├── README.md            # Documentação completa
│   ├── DEPLOY.md            # Guia de deploy
│   └── test_api.py          # Testes
└── mobile/                  # (Próximo passo!)
```

---

## 🎨 CORES E TIPOS JÁ CADASTRADOS

### Cores Padrão:
- 01 - Preto
- 02 - Branco
- 03 - Vermelho
- 04 - Azul
- 05 - Verde
- ... (14 cores no total)

### Tipos Padrão (para roupas):
- 01 - Blusa
- 02 - Calça
- 03 - Vestido
- 04 - Saia
- 05 - Short
- ... (10 tipos no total)

**Você pode adicionar mais cores e tipos pela API!**

---

## 🖨️ COMO IMPRIMIR ETIQUETAS

### Opção 1: Impressora Térmica de Etiquetas
- Zebra, Argox, etc.
- Formato: 40mm x 30mm
- Custo: ~R$ 300-600

### Opção 2: Impressora Comum + Etiquetas Adesivas
- Compre etiquetas A4 adesivas
- Papel A4 com 10-20 etiquetas
- Custo: ~R$ 15-30 (pacote com 100 folhas)

### Opção 3: Serviço de Impressão
- Exporte as etiquetas
- Leve numa gráfica rápida
- Imprima em papel adesivo

---

## 📱 PRÓXIMO PASSO: APP MOBILE

Agora vamos criar o app para celular com:
- Scanner de código de barras pela câmera
- Cadastro rápido de produtos
- Entrada/saída em 2 cliques
- Relatórios de estoque
- Funciona offline (sincroniza depois)

**Quer que eu comece a criar o app mobile agora?**

---

## 🆘 PRECISA DE AJUDA?

### Documentação:
- `README.md` - Documentação completa
- `DEPLOY.md` - Guia de deploy
- `/docs` - API interativa (quando rodar)

### Teste rápido:
```bash
python test_api.py
```

### Ver logs:
```bash
docker-compose logs -f api
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [x] Backend API criado
- [x] Banco de dados estruturado
- [x] Geração de código de barras
- [x] Sistema de entrada/saída
- [x] Geração de etiquetas
- [x] Documentação completa
- [ ] App Mobile (próximo!)
- [ ] Deploy online
- [ ] Impressão de etiquetas
- [ ] Treinamento da equipe

---

## 💡 DICAS IMPORTANTES

1. **Comece simples:** Rode localmente primeiro para testar
2. **Imprima algumas etiquetas:** Cole em produtos de teste
3. **Teste o fluxo:** Cadastro → Etiqueta → Entrada → Saída
4. **Depois coloque online:** Quando estiver confortável
5. **Configure backup:** Seus dados são importantes!

---

## 🎯 RESULTADO FINAL

Sua esposa vai poder:
- ✅ Cadastrar produtos rapidamente
- ✅ Gerar etiquetas com código de barras
- ✅ Dar entrada/saída pelo celular
- ✅ Ver estoque em tempo real
- ✅ Receber alertas de estoque baixo
- ✅ Acessar histórico completo

**Tudo pelo celular, rápido e simples!** 📱

---

**Bora criar o app mobile agora?** 🚀

Desenvolvido com ❤️ para facilitar a vida de quem empreende!
