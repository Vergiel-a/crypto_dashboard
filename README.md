# 📈 Dashboard de Criptomoedas - Documentação Completa

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Requisitos](#requisitos)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Instalação Local](#instalação-local)
5. [Deploy no Streamlit Cloud](#deploy-no-streamlit-cloud)
6. [Uso do Dashboard](#uso-do-dashboard)
---

## 🎯 Visão Geral

Dashboard interativo em Python que exibe dados em tempo real das principais criptomoedas usando a API gratuita do CoinGecko.

**Funcionalidades:**
- ✅ Dados em tempo real de até 50 criptomoedas
- ✅ Atualização automática configurável (10-30 minutos)
- ✅ Gráficos interativos (7 e 30 dias)
- ✅ Métricas de mercado (Market Cap, Volume, Dominância BTC)
- ✅ Tabela com ranking e variações de preço
- ✅ Interface moderna e responsiva

---

## 📦 Requisitos

- Python 3.8 ou superior
- Conta no GitHub (gratuita)
- Conta no Streamlit Cloud (gratuita)

---

## 📁 Estrutura do Projeto

Seu repositório GitHub deve ter a seguinte estrutura:

```
crypto-dashboard/
│
├── app.py                  # Arquivo principal do dashboard
├── requirements.txt        # Dependências do projeto
├── README.md              # Documentação do projeto
└── .gitignore            # Arquivos a serem ignorados (opcional)
```

---

## 🛠️ Instalação Local

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/crypto-dashboard.git
cd crypto-dashboard
```

### 2️⃣ Criar Ambiente Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar Localmente

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

---

## 📝 Arquivos Necessários

### **1. app.py**

Copie o código completo do dashboard Python fornecido anteriormente.

### **2. requirements.txt**

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```txt
streamlit==1.29.0
pandas==2.3.3
requests==2.31.0
plotly==5.18.0
```

### **3. README.md** (Opcional mas recomendado)

```markdown
# 📈 Dashboard de Criptomoedas

Dashboard interativo para análise de criptomoedas em tempo real.

## 🚀 Acesso Online
[Link do Dashboard](https://cryptodashboard-s9to9g4ywatqk7wy5euqxe.streamlit.app/)

## 🛠️ Tecnologias
- Python 3.8+
- Streamlit
- Plotly
- Pandas
- CoinGecko API

## 📊 Funcionalidades
- Dados em tempo real de 50+ criptomoedas
- Gráficos históricos interativos
- Métricas de mercado
- Atualização automática

## 💻 Executar Localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📄 Licença
MIT License
```

### **4. .gitignore** (Opcional)

```txt
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Streamlit
.streamlit/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 🚀 Deploy no Streamlit Cloud

### **Passo 1: Preparar o Repositório GitHub**

1. **Crie um repositório no GitHub:**
   - Acesse [github.com](https://github.com)
   - Clique em **"New repository"**
   - Nome sugerido: `crypto-dashboard`
   - Selecione **"Public"** (necessário para Streamlit Cloud gratuito)
   - Clique em **"Create repository"**

2. **Faça upload dos arquivos:**

   **Opção A - Via interface web:**
   - Clique em **"uploading an existing file"**
   - Arraste os arquivos: `app.py`, `requirements.txt`, `README.md`
   - Commit com mensagem: "Initial commit"

   **Opção B - Via Git (linha de comando):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/crypto-dashboard.git
   git push -u origin main
   ```

3. **Verifique se os arquivos estão no repositório:**
   - ✅ `app.py`
   - ✅ `requirements.txt`
   - ✅ `README.md` (opcional)

---

### **Passo 2: Criar Conta no Streamlit Cloud**

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"Sign up"** ou **"Continue with GitHub"**
3. Autorize o Streamlit a acessar sua conta GitHub
4. Complete o cadastro

---

### **Passo 3: Deploy do Aplicativo**

1. **No Streamlit Cloud, clique em "New app"**

2. **Configure o deploy:**
   - **Repository:** Selecione `seu-usuario/crypto-dashboard`
   - **Branch:** `main` (ou `master`)
   - **Main file path:** `app.py`
   - **App URL (optional):** Escolha uma URL personalizada (ex: `crypto-dashboard-seu-nome`)

3. **Clique em "Deploy!"**

4. **Aguarde o deploy (2-5 minutos):**
   - O Streamlit irá:
     - ✅ Clonar seu repositório
     - ✅ Instalar dependências do `requirements.txt`
     - ✅ Executar o `app.py`
     - ✅ Gerar URL pública

5. **Acesse seu dashboard:**
   - URL será algo como: `https://crypto-dashboard-seu-nome.streamlit.app`
   - Compartilhe com qualquer pessoa! 🎉

---

### **Passo 4: Verificar o Deploy**

Após o deploy, você verá:

✅ **Status: Running** (verde)
- Seu app está online e funcionando

❌ **Status: Error** (vermelho)
- Verifique os logs clicando em "Manage app" → "Logs"
- Erros comuns e soluções na seção abaixo

---

## 🔄 Atualizar o Dashboard

Sempre que você fizer alterações no código:

1. **Atualize o repositório GitHub:**
   ```bash
   git add .
   git commit -m "Descrição das alterações"
   git push
   ```

2. **O Streamlit Cloud atualiza automaticamente!**
   - Detecta mudanças no GitHub
   - Redeploy automático
   - Sem necessidade de ação manual

Ou clique em **"Reboot app"** no painel do Streamlit Cloud.

---

## 🎮 Uso do Dashboard

### **Configurações (Sidebar)**

1. **Número de criptomoedas:** 
   - Slider de 5 a 50 moedas
   - Padrão: 20 moedas

2. **Atualização automática:**
   - ☑️ Ativar/desativar
   - Intervalo: 10-30 minutos
   - Padrão: 10 minutos

3. **Botão "Atualizar Agora":**
   - Força atualização imediata
   - Limpa cache

### **Funcionalidades Principais**

1. **Métricas Gerais:**
   - Market Cap Total
   - Volume 24h
   - Dominância Bitcoin
   - Variação Média 24h

2. **Gráficos:**
   - Barras: Top 10 por Market Cap
   - Pizza: Distribuição de Market Cap

3. **Tabela de Rankings:**
   - Ordenada por Market Cap
   - Colunas: Rank, Nome, Preço, Variações (1h/24h/7d), Volume, Market Cap
   - Emojis: 🟢 (alta) / 🔴 (baixa)

4. **Análise Detalhada:**
   - Selecione uma criptomoeda
   - Informações: Preços (atual/máx/mín), métricas, variações
   - Abas: Gráficos de 7 e 30 dias

---

## ⚠️ Solução de Problemas

### **Erro 429 - Too Many Requests**

**Causa:** Limite da API CoinGecko atingido

**Solução:**
- ✅ Aguarde 1-2 minutos
- ✅ Use intervalos maiores de atualização (15-30 min)
- ✅ Gráfico de 7 dias usa dados "sparkline" (sem requisições extras)
- ✅ Cache de 5 minutos nos dados históricos

---

### **App não inicia no Streamlit Cloud**

**Erro:** `ModuleNotFoundError`

**Solução:**
1. Verifique se `requirements.txt` está no repositório
2. Confirme se todas as bibliotecas estão listadas
3. Reboot do app: "Manage app" → "Reboot app"

---

### **Gráficos não aparecem**

**Solução:**
1. Verifique conexão com a internet
2. API pode estar temporariamente indisponível
3. Aguarde 1-2 minutos e clique "Atualizar Agora"
4. Gráfico de 7 dias usa sparkline (sempre disponível)

---

### **Deploy falha com erro de Python**

**Erro:** `Python version not supported`

**Solução:**
Crie arquivo `.streamlit/config.toml` no repositório:

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

E especifique versão Python em `runtime.txt`:
```txt
python-3.11
```

---

### **App muito lento**

**Solução:**
- ✅ Reduza número de criptomoedas (slider)
- ✅ Aumente intervalo de atualização
- ✅ Cache otimiza requisições (já implementado)

---

## 📊 Limites da API Gratuita

**CoinGecko API (Free Tier):**
- ✅ 10-30 requisições/minuto
- ✅ Sem necessidade de API Key
- ✅ Dados em tempo real
- ⚠️ Rate limit: 429 error

**Otimizações implementadas:**
- Cache de 60s para dados principais
- Cache de 5 minutos para históricos
- Sparkline de 7 dias (sem requisição extra)
- Delay entre requisições

---

## 🔧 Configurações Avançadas

### **Alterar tema do Streamlit**

Crie `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#8B5CF6"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#F1F5F9"
font = "sans serif"
```

### **Configurar domínio customizado**

1. No Streamlit Cloud: "Settings" → "Custom domain"
2. Configure DNS do seu domínio
3. Documentação: [docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/custom-domains](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/custom-domains)

---

## 📚 Recursos Adicionais

- **Documentação Streamlit:** [docs.streamlit.io](https://docs.streamlit.io)
- **API CoinGecko:** [coingecko.com/en/api/documentation](https://www.coingecko.com/en/api/documentation)
- **Plotly Docs:** [plotly.com/python](https://plotly.com/python/)
- **Pandas Docs:** [pandas.pydata.org](https://pandas.pydata.org/docs/)

---

## 🎯 Checklist de Deploy

Antes de fazer deploy, verifique:

- [ ] Código testado localmente (`streamlit run app.py`)
- [ ] `requirements.txt` criado e atualizado
- [ ] `README.md` criado
- [ ] Repositório GitHub criado (público)
- [ ] Arquivos commitados no GitHub
- [ ] Conta Streamlit Cloud criada
- [ ] App deployado com sucesso
- [ ] URL funcionando corretamente
- [ ] Gráficos carregando
- [ ] Dados atualizando

---

## ✨ Melhorias Futuras

Sugestões de expansão:
- [ ] Adicionar mais exchanges (Binance, Coinbase)
- [ ] Alertas de preço por email
- [ ] Comparação entre criptomoedas
- [ ] Análise técnica (RSI, MACD)
- [ ] Portfolio tracker
- [ ] Modo escuro/claro
- [ ] Exportar dados (CSV, Excel)
- [ ] Integração com APIs de carteiras

---

**🎉 Parabéns! Seu dashboard está no ar!**

Compartilhe a URL do seu app e mostre suas habilidades em análise de dados! 📊🚀
