# 📱 Estoque Engenho - App Mobile

App mobile para controle de estoque com scanner de código de barras.

## 🚀 Funcionalidades

- ✅ Scanner de código de barras pela câmera
- ✅ Entrada de estoque rápida
- ✅ Saída de estoque (vendas)
- ✅ Lista de produtos com busca
- ✅ Dashboard com estatísticas
- ✅ Alertas de estoque baixo
- ✅ Interface simples e intuitiva

## 📋 Pré-requisitos

- Node.js 18+ instalado
- Expo CLI (`npm install -g expo-cli`)
- Expo Go app no celular (para testes)

## 🔧 Instalação

```bash
# Entre na pasta mobile
cd estoque-engenho/mobile

# Instale as dependências
npm install

# Configure a URL da API
# Edite o arquivo src/config/api.js
# Altere API_URL para o endereço da sua API
```

## ▶️ Como Rodar

### Desenvolvimento (Expo Go)

```bash
# Inicie o servidor Expo
npm start

# Ou diretamente:
npx expo start

# Escaneie o QR Code com:
# - Android: App Expo Go
# - iOS: Câmera do iPhone
```

### Android Emulator

```bash
npm run android
```

### iOS Simulator (apenas Mac)

```bash
npm run ios
```

## ⚙️ Configuração Importante

### 1. Configure a URL da API

Edite `src/config/api.js`:

```javascript
// Para testes local (Android Emulator)
export const API_URL = 'http://10.0.2.2:8000';

// Para dispositivo físico na mesma rede
export const API_URL = 'http://192.168.1.100:8000';  // Use o IP da sua máquina

// Para produção (após deploy)
export const API_URL = 'https://sua-api.railway.app';
```

### 2. Permissões de Câmera

As permissões já estão configuradas no `app.json`. O app vai solicitar automaticamente.

## 📱 Testando no Celular

1. Instale o **Expo Go** na Play Store (Android) ou App Store (iOS)
2. Rode `npm start`
3. Escaneie o QR Code que aparece no terminal
4. O app abre no celular!

## 🏗️ Build para Produção

### Android (APK)

```bash
# Build desenvolvimento
npx expo build:android -t apk

# Build produção (AAB para Play Store)
npx expo build:android -t app-bundle
```

### iOS (IPA)

```bash
npx expo build:ios
```

## 📖 Uso do App

### Tela Inicial
- Veja estatísticas do estoque
- Acesse ações rápidas
- Veja produtos com estoque baixo

### Entrada de Estoque
1. Toque no botão "Scanner" ou digite o código
2. Confirme o produto
3. Digite a quantidade
4. Confirme!

### Saída de Estoque
1. Escaneie o código do produto vendido
2. Digite a quantidade vendida
3. Adicione observação (opcional)
4. Confirme a saída!

### Lista de Produtos
- Veja todos os produtos
- Busque por nome ou código
- Toque para ver detalhes

## 🎨 Estrutura do Projeto

```
mobile/
├── App.js                      # Entrada principal
├── app.json                    # Configurações Expo
├── package.json                # Dependências
└── src/
    ├── config/
    │   └── api.js             # Configuração da API
    ├── services/
    │   └── api.js             # Serviços de comunicação
    ├── components/
    │   └── BarcodeScanner.js  # Scanner de código de barras
    ├── screens/
    │   ├── HomeScreen.js      # Tela inicial
    │   ├── EntradaScreen.js   # Entrada de estoque
    │   ├── SaidaScreen.js     # Saída de estoque
    │   └── ProdutosScreen.js  # Lista de produtos
    └── navigation/
        └── index.js           # Navegação do app
```

## 🐛 Troubleshooting

### Erro: "Network request failed"
- Verifique se a API está rodando
- Confirme a URL da API no arquivo `config/api.js`
- Em dispositivo físico, use o IP da rede (não localhost)

### Câmera não funciona
- Certifique-se de que deu permissão
- No emulador, a câmera pode não funcionar (use dispositivo físico)

### App não conecta com a API
- API rodando? Teste: `curl http://sua-api:8000/health`
- Firewall bloqueando? Libere a porta 8000
- No Android Emulator: use `10.0.2.2:8000`
- No dispositivo físico: use o IP da máquina na rede

## 📞 Comandos Úteis

```bash
# Limpar cache
npx expo start -c

# Ver logs
npx expo start --dev-client

# Instalar dependência
npm install nome-pacote

# Atualizar Expo
npm install expo@latest
```

## 🎯 Próximos Passos

Depois de testar:

1. ✅ Faça o build para produção
2. 📱 Distribua para sua equipe
3. 🎉 Comece a usar!

## 💡 Dicas

- **Teste primeiro no emulador** antes de fazer build
- **Use Expo Go** para desenvolvimento rápido
- **Faça backup** da configuração da API
- **Documente** mudanças que fizer

---

Desenvolvido com ❤️ para facilitar o controle de estoque!
