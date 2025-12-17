# 🚀 Guia de Deploy - Estoque Engenho

## Opção 1: Railway.app (Recomendado - Mais Fácil)

### Passo a Passo:

1. **Crie uma conta gratuita**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Crie um novo projeto**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Autorize o Railway a acessar seus repositórios
   - Selecione o repositório `estoque-engenho`

3. **Adicione o banco de dados MySQL**
   - No projeto, clique em "+ New"
   - Selecione "Database" → "Add MySQL"
   - Railway vai criar automaticamente

4. **Configure as variáveis de ambiente**
   - Clique no serviço da API
   - Vá em "Variables"
   - Adicione:
     ```
     DB_HOST=${{MySQL.MYSQL_HOST}}
     DB_PORT=${{MySQL.MYSQL_PORT}}
     DB_USER=${{MySQL.MYSQL_USER}}
     DB_PASSWORD=${{MySQL.MYSQL_PASSWORD}}
     DB_NAME=${{MySQL.MYSQL_DATABASE}}
     API_HOST=0.0.0.0
     API_PORT=8000
     ALLOWED_ORIGINS=*
     ```

5. **Deploy!**
   - Railway vai fazer o deploy automaticamente
   - Você receberá uma URL pública tipo: `estoque-engenho.up.railway.app`

**Custo:** Gratuito para começar (500 horas/mês)

---

## Opção 2: Render.com (Alternativa Gratuita)

### Passo a Passo:

1. **Crie uma conta gratuita**
   - Acesse: https://render.com
   - Faça login com GitHub

2. **Crie o banco de dados PostgreSQL**
   - Clique em "New +" → "PostgreSQL"
   - Nome: `estoque-engenho-db`
   - Plano: Free
   - Clique em "Create Database"
   - **Importante:** Anote a "Internal Database URL"

3. **Crie o Web Service**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name:** estoque-engenho-api
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Configure variáveis de ambiente**
   - Em "Environment Variables", adicione:
     ```
     DATABASE_URL=${{DATABASE_URL_FROM_POSTGRES}}
     API_HOST=0.0.0.0
     ALLOWED_ORIGINS=*
     ```

5. **Deploy!**
   - Clique em "Create Web Service"
   - Aguarde o deploy (3-5 minutos)
   - Sua URL será: `estoque-engenho-api.onrender.com`

**Custo:** Gratuito (com algumas limitações)

---

## Opção 3: PythonAnywhere (100% Gratuito)

### Passo a Passo:

1. **Crie conta gratuita**
   - Acesse: https://www.pythonanywhere.com
   - Crie conta gratuita

2. **Faça upload do código**
   - Abra o console Bash
   - Clone seu repositório:
     ```bash
     git clone https://github.com/seu-usuario/estoque-engenho.git
     cd estoque-engenho/backend
     ```

3. **Instale dependências**
   ```bash
   pip3 install --user -r requirements.txt
   ```

4. **Configure MySQL**
   - Vá em "Databases"
   - Crie um banco MySQL
   - Execute o script `schema.sql`

5. **Configure Web App**
   - Vá em "Web"
   - Adicione nova web app
   - Configure WSGI file para FastAPI

**Custo:** 100% Gratuito

---

## ✅ Após o Deploy

### Teste sua API:

```bash
# Substitua pela sua URL
curl https://sua-api.railway.app/health

# Ou acesse no navegador:
https://sua-api.railway.app/docs
```

### Atualize o App Mobile:

No arquivo de configuração do app mobile, altere a URL da API:

```javascript
// config.js
export const API_URL = "https://sua-api.railway.app";
```

---

## 🔒 Segurança (Importante!)

Após o deploy, configure:

1. **CORS adequado**
   ```env
   ALLOWED_ORIGINS=https://seu-dominio.com,https://app.seu-dominio.com
   ```

2. **Variáveis de ambiente seguras**
   - Nunca commite senhas no código
   - Use as variáveis de ambiente da plataforma

3. **SSL/HTTPS**
   - Railway e Render já incluem HTTPS automático ✅

---

## 📊 Monitoramento

### Railway:
- Dashboard automático com logs
- Métricas de uso

### Render:
- Logs em tempo real
- Alertas de erro

---

## 💰 Custos Estimados

| Plataforma | Custo Inicial | Custo Mensal |
|------------|---------------|--------------|
| Railway | Grátis | $5-10 (após trial) |
| Render | Grátis | Grátis (com limitações) |
| PythonAnywhere | Grátis | Grátis (básico) |

---

## 🆘 Problemas Comuns

### 1. Erro de conexão com banco
- Verifique se as variáveis de ambiente estão corretas
- Confirme que o banco foi criado

### 2. Timeout no deploy
- Aguarde um pouco mais (pode demorar 5-10 minutos)
- Verifique os logs de build

### 3. Erro 502/503
- Aguarde a aplicação "acordar" (planos gratuitos dormem)
- Verifique o comando de start

---

## 📞 Próximo Passo

Agora que sua API está online:
1. ✅ Anote a URL da API
2. 📱 Configure o app mobile
3. 🎉 Comece a usar!

---

**Dica:** Comece com Railway - é o mais fácil e rápido para testar! 🚀
