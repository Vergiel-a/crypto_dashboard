import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Criptomoedas",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

# ========== FUNÇÕES AUXILIARES ==========

@st.cache_data(ttl=60)  # Cache por 60 segundos
def buscar_dados_criptomoedas(numero_moedas=20):
    """
    Busca dados das principais criptomoedas via API CoinGecko.
    Retorna DataFrame com dados ou DataFrame vazio em caso de erro.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parametros = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': numero_moedas,
        'page': 1,
        'sparkline': 'true',
        'price_change_percentage': '1h,24h,7d,30d'
    }
    
    try:
        resposta = requests.get(url, params=parametros, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        
        if not dados:
            return pd.DataFrame()
        
        df = pd.DataFrame(dados)
        
        # Verificar se colunas essenciais existem
        colunas_necessarias = ['id', 'symbol', 'name', 'current_price', 'market_cap', 
                               'total_volume', 'price_change_percentage_24h']
        
        for col in colunas_necessarias:
            if col not in df.columns:
                st.warning(f"Coluna '{col}' não encontrada nos dados da API")
                return pd.DataFrame()
        
        return df
        
    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout: A API demorou muito para responder. Tente novamente.")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro na requisição: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro inesperado ao buscar dados: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=300)  # Cache por 5 minutos (300 segundos)
def buscar_dados_historicos(cripto_id, dias=30):
    """
    Busca dados históricos de preço de uma criptomoeda específica.
    Retorna DataFrame com timestamp e price ou DataFrame vazio.
    Cache de 5 minutos para evitar excesso de requisições.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{cripto_id}/market_chart"
    parametros = {
        'vs_currency': 'usd',
        'days': dias,
        'interval': 'daily' if dias > 1 else 'hourly'
    }
    
    try:
        # Adicionar delay pequeno para evitar rate limit
        time.sleep(0.5)
        
        resposta = requests.get(url, params=parametros, timeout=15)
        
        # Tratamento específico para erro 429 (Rate Limit)
        if resposta.status_code == 429:
            st.error("⚠️ **Limite de requisições da API atingido.** Os dados históricos estão temporariamente indisponíveis. Aguarde alguns minutos antes de atualizar novamente.")
            return pd.DataFrame()
        
        resposta.raise_for_status()
        dados = resposta.json()
        
        if 'prices' not in dados or not dados['prices']:
            return pd.DataFrame()
        
        # Converter para DataFrame
        precos = dados['prices']
        df = pd.DataFrame(precos, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
        
    except requests.exceptions.Timeout:
        st.warning("⏱️ Timeout ao buscar dados históricos. Tente novamente em alguns instantes.")
        return pd.DataFrame()
    except requests.exceptions.HTTPError as e:
        if '429' in str(e):
            st.error("⚠️ **Limite de requisições atingido.** A API do CoinGecko possui limite gratuito. Aguarde 1-2 minutos e tente novamente.")
        else:
            st.warning(f"⚠️ Erro HTTP ao buscar dados históricos: {e}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ Erro de conexão: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ Erro inesperado: {str(e)}")
        return pd.DataFrame()


def formatar_numero(numero):
    """
    Formata números grandes para notação simplificada (K, M, B, T).
    Retorna string formatada.
    """
    if pd.isna(numero) or numero is None:
        return "N/A"
    
    try:
        numero = float(numero)
        
        if numero >= 1e12:
            return f"${numero/1e12:.2f}T"
        elif numero >= 1e9:
            return f"${numero/1e9:.2f}B"
        elif numero >= 1e6:
            return f"${numero/1e6:.2f}M"
        elif numero >= 1e3:
            return f"${numero/1e3:.2f}K"
        else:
            return f"${numero:.2f}"
    except (ValueError, TypeError):
        return "N/A"


def formatar_preco(preco):
    """
    Formata o preço com a quantidade adequada de casas decimais.
    Retorna string formatada.
    """
    if pd.isna(preco) or preco is None:
        return "N/A"
    
    try:
        preco = float(preco)
        
        if preco >= 1:
            return f"${preco:,.2f}"
        elif preco >= 0.01:
            return f"${preco:.4f}"
        else:
            return f"${preco:.8f}"
    except (ValueError, TypeError):
        return "N/A"


def formatar_percentual(valor):
    """
    Formata valores percentuais com 2 casas decimais.
    Retorna string formatada ou N/A.
    """
    if pd.isna(valor) or valor is None:
        return "N/A"
    
    try:
        valor = float(valor)
        return f"{valor:.2f}%"
    except (ValueError, TypeError):
        return "N/A"


def obter_emoji_variacao(valor):
    """
    Retorna emoji baseado na variação do preço.
    🟢 para positivo, 🔴 para negativo, ⚪ para neutro/N/A.
    """
    if pd.isna(valor) or valor is None:
        return "⚪"
    
    try:
        valor = float(valor)
        return "🟢" if valor > 0 else "🔴" if valor < 0 else "⚪"
    except (ValueError, TypeError):
        return "⚪"


def criar_grafico_historico(df_historico, titulo):
    """
    Cria gráfico de linha com os dados históricos.
    Retorna figure do Plotly.
    """
    if df_historico.empty or 'timestamp' not in df_historico.columns or 'price' not in df_historico.columns:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_historico['timestamp'],
        y=df_historico['price'],
        mode='lines',
        name='Preço',
        line=dict(color='#00d4ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)',
        hovertemplate='<b>Data:</b> %{x|%d/%m/%Y %H:%M}<br><b>Preço:</b> $%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=titulo,
        xaxis_title="Data",
        yaxis_title="Preço (USD)",
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        paper_bgcolor='rgba(0,0,0,0.3)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(color='white')
    )
    
    return fig


def criar_grafico_distribuicao(df):
    """
    Cria gráfico de pizza com distribuição de market cap (Top 10).
    Retorna figure do Plotly.
    """
    if df.empty or 'market_cap' not in df.columns or 'name' not in df.columns:
        return None
    
    # Top 10 para o gráfico
    df_top = df.head(10).copy()
    
    # Remover valores nulos
    df_top = df_top[df_top['market_cap'].notna()]
    
    if df_top.empty:
        return None
    
    fig = px.pie(
        df_top,
        values='market_cap',
        names='name',
        title='Distribuição de Market Cap (Top 10)',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Market Cap: $%{value:,.0f}<br>Percentual: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0.3)',
        height=400,
        font=dict(color='white')
    )
    
    return fig


def criar_grafico_barras(df):
    """
    Cria gráfico de barras com Top 10 por Market Cap.
    Retorna figure do Plotly.
    """
    if df.empty or 'market_cap' not in df.columns or 'name' not in df.columns:
        return None
    
    df_top10 = df.head(10).copy()
    df_top10 = df_top10[df_top10['market_cap'].notna()]
    
    if df_top10.empty:
        return None
    
    # Verificar se a coluna de variação existe
    color_col = 'price_change_percentage_24h' if 'price_change_percentage_24h' in df_top10.columns else None
    
    fig = px.bar(
        df_top10,
        x='name',
        y='market_cap',
        title='Top 10 Criptomoedas por Market Cap',
        labels={'market_cap': 'Market Cap (USD)', 'name': 'Criptomoeda'},
        color=color_col,
        color_continuous_scale=['red', 'yellow', 'green'],
        hover_data={'market_cap': ':,.0f'}
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0.3)',
        height=400,
        xaxis_tickangle=-45,
        font=dict(color='white')
    )
    
    return fig


# ========== INTERFACE PRINCIPAL ==========

# Título e descrição
st.title("📈 Dashboard de Criptomoedas")

# Aviso sobre limites da API
with st.expander("ℹ️ Informações Importantes sobre a API", expanded=False):
    st.markdown("""
    **Sobre os dados:**
    - Este dashboard utiliza a **API gratuita do CoinGecko**
    - A API possui **limites de requisições** (rate limits)
    - Dados principais são atualizados a cada 60 segundos (configurável)
    - Gráficos históricos têm cache de 5 minutos para economizar requisições
    
    **Se encontrar erros:**
    - ⚠️ **Erro 429**: Aguarde 1-2 minutos antes de atualizar
    - 🔄 Use o botão "Atualizar Agora" ao invés de recarregar a página
    - 📊 Os gráficos de 7 dias usam dados "sparkline" quando possível (sem requisições extras)
    """)

st.markdown("---")

# Sidebar - Configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    numero_moedas = st.slider(
        "Número de criptomoedas",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )
    
    auto_atualizar = st.checkbox("Atualização automática", value=True)
    
    if auto_atualizar:
        intervalo = st.slider(
            "Intervalo de atualização (segundos)",
            min_value=600,
            max_value=1800,
            value=600,
            step=300
        )
    
    st.markdown("---")
    st.info("💡 **Dica:** Selecione uma criptomoeda abaixo para ver gráficos históricos!")
    
    st.warning("⚠️ **Importante:** A API gratuita do CoinGecko tem limites de requisições. Se os gráficos não carregarem, aguarde 1-2 minutos.")
    
    # Botão de atualização manual
    if st.button("🔄 Atualizar Agora", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Buscar dados
with st.spinner("🔍 Buscando dados das criptomoedas..."):
    df = buscar_dados_criptomoedas(numero_moedas)

if df.empty:
    st.error("❌ Não foi possível carregar os dados. Verifique sua conexão e tente novamente.")
    st.stop()

# Última atualização
col_update1, col_update2 = st.columns([3, 1])
with col_update1:
    st.caption(f"🕐 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
with col_update2:
    if auto_atualizar:
        st.caption(f"⏱️ Próxima em: {intervalo}s")

# ========== MÉTRICAS PRINCIPAIS ==========
st.subheader("📊 Visão Geral do Mercado")

col1, col2, col3, col4 = st.columns(4)

with col1:
    market_cap_total = df['market_cap'].sum() if 'market_cap' in df.columns else 0
    st.metric(
        label="Market Cap Total",
        value=formatar_numero(market_cap_total)
    )

with col2:
    volume_total = df['total_volume'].sum() if 'total_volume' in df.columns else 0
    st.metric(
        label="Volume 24h Total",
        value=formatar_numero(volume_total)
    )

with col3:
    # Dominância do Bitcoin
    if 'symbol' in df.columns and 'market_cap' in df.columns:
        btc_row = df[df['symbol'].str.lower() == 'btc']
        if not btc_row.empty and market_cap_total > 0:
            btc_dominance = (btc_row.iloc[0]['market_cap'] / market_cap_total * 100)
            st.metric(
                label="Dominância BTC",
                value=f"{btc_dominance:.2f}%"
            )
        else:
            st.metric(label="Dominância BTC", value="N/A")
    else:
        st.metric(label="Dominância BTC", value="N/A")

with col4:
    # Média de variação 24h
    if 'price_change_percentage_24h' in df.columns:
        media_variacao = df['price_change_percentage_24h'].mean()
        st.metric(
            label="Variação Média 24h",
            value=formatar_percentual(media_variacao),
            delta=formatar_percentual(media_variacao)
        )
    else:
        st.metric(label="Variação Média 24h", value="N/A")

st.markdown("---")

# ========== GRÁFICOS DE ANÁLISE ==========
st.subheader("📈 Análise Visual")

col_g1, col_g2 = st.columns(2)

with col_g1:
    # Gráfico de barras - Top 10 por Market Cap
    fig_bar = criar_grafico_barras(df)
    if fig_bar:
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Não foi possível criar o gráfico de barras.")

with col_g2:
    # Gráfico de pizza - Distribuição
    fig_pie = criar_grafico_distribuicao(df)
    if fig_pie:
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Não foi possível criar o gráfico de distribuição.")

st.markdown("---")

# ========== TABELA DE CRIPTOMOEDAS ==========
st.subheader("💰 Ranking de Criptomoedas")

# Preparar DataFrame para exibição
df_tabela = pd.DataFrame()

if not df.empty:
    df_tabela['#'] = df['market_cap_rank'].fillna(0).astype(int)
    df_tabela['Nome'] = df['name'] + ' (' + df['symbol'].str.upper() + ')'
    df_tabela['Preço'] = df['current_price'].apply(formatar_preco)
    
    # Variações com emojis
    if 'price_change_percentage_1h_in_currency' in df.columns:
        df_tabela['1h'] = df.apply(
            lambda x: f"{obter_emoji_variacao(x['price_change_percentage_1h_in_currency'])} {formatar_percentual(x['price_change_percentage_1h_in_currency'])}", 
            axis=1
        )
    
    if 'price_change_percentage_24h' in df.columns:
        df_tabela['24h'] = df.apply(
            lambda x: f"{obter_emoji_variacao(x['price_change_percentage_24h'])} {formatar_percentual(x['price_change_percentage_24h'])}", 
            axis=1
        )
    
    if 'price_change_percentage_7d_in_currency' in df.columns:
        df_tabela['7d'] = df.apply(
            lambda x: f"{obter_emoji_variacao(x['price_change_percentage_7d_in_currency'])} {formatar_percentual(x['price_change_percentage_7d_in_currency'])}", 
            axis=1
        )
    
    df_tabela['Volume 24h'] = df['total_volume'].apply(formatar_numero)
    df_tabela['Market Cap'] = df['market_cap'].apply(formatar_numero)

# Exibir tabela
st.dataframe(
    df_tabela,
    use_container_width=True,
    height=600,
    hide_index=True
)

st.markdown("---")

# ========== DETALHES DA CRIPTOMOEDA SELECIONADA ==========
st.subheader("🔍 Análise Detalhada")

# Seletor de criptomoeda
if 'name' in df.columns and not df.empty:
    cripto_selecionada = st.selectbox(
        "Selecione uma criptomoeda para ver detalhes:",
        options=df['name'].tolist(),
        index=0
    )
    
    # Buscar linha da criptomoeda selecionada
    info_row = df[df['name'] == cripto_selecionada].iloc[0]
    cripto_id = info_row['id']
    
    # Informações em cards
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Preço Atual", formatar_preco(info_row.get('current_price')))
        st.metric("Preço Máximo 24h", formatar_preco(info_row.get('high_24h')))
        st.metric("Preço Mínimo 24h", formatar_preco(info_row.get('low_24h')))
    
    with col_info2:
        st.metric("Market Cap", formatar_numero(info_row.get('market_cap')))
        st.metric("Volume 24h", formatar_numero(info_row.get('total_volume')))
        rank = info_row.get('market_cap_rank')
        st.metric("Market Cap Rank", f"#{int(rank)}" if pd.notna(rank) else "N/A")
    
    with col_info3:
        var_1h = info_row.get('price_change_percentage_1h_in_currency')
        st.metric("Variação 1h", formatar_percentual(var_1h), delta=formatar_percentual(var_1h))
        
        var_24h = info_row.get('price_change_percentage_24h')
        st.metric("Variação 24h", formatar_percentual(var_24h), delta=formatar_percentual(var_24h))
        
        var_7d = info_row.get('price_change_percentage_7d_in_currency')
        st.metric("Variação 7d", formatar_percentual(var_7d), delta=formatar_percentual(var_7d))
    
    st.markdown("---")
    
    # Gráficos históricos em tabs
    tab1, tab2 = st.tabs(["📅 Últimos 7 Dias", "📅 Últimos 30 Dias"])
    
    with tab1:
        # Tentar usar dados de sparkline primeiro (já disponíveis, sem nova requisição)
        if 'sparkline_in_7d' in info_row and info_row['sparkline_in_7d'] and isinstance(info_row['sparkline_in_7d'], dict):
            sparkline_prices = info_row['sparkline_in_7d'].get('price', [])
            if sparkline_prices and len(sparkline_prices) > 0:
                # Criar DataFrame a partir do sparkline
                df_sparkline = pd.DataFrame({
                    'timestamp': pd.date_range(end=datetime.now(), periods=len(sparkline_prices), freq='H'),
                    'price': sparkline_prices
                })
                fig_7d_spark = criar_grafico_historico(df_sparkline, f"{cripto_selecionada} - Últimos 7 Dias (Sparkline)")
                if fig_7d_spark:
                    st.plotly_chart(fig_7d_spark, use_container_width=True)
                    st.caption("📌 Dados do gráfico sparkline (168 pontos horários)")
            else:
                st.info("📊 Dados de sparkline não disponíveis. Tente selecionar outra criptomoeda.")
        else:
            # Se não houver sparkline, tentar buscar dados históricos
            with st.spinner("Carregando dados de 7 dias..."):
                df_hist_7 = buscar_dados_historicos(cripto_id, 7)
                if not df_hist_7.empty:
                    fig_7d = criar_grafico_historico(df_hist_7, f"{cripto_selecionada} - Últimos 7 Dias")
                    if fig_7d:
                        st.plotly_chart(fig_7d, use_container_width=True)
                    else:
                        st.warning("Não foi possível criar o gráfico.")
                else:
                    st.info("📊 Dados históricos não disponíveis no momento. A API pode ter atingido o limite de requisições. Aguarde 1-2 minutos e clique em 'Atualizar Agora' na sidebar.")
    
    with tab2:
        with st.spinner("Carregando dados de 30 dias..."):
            df_hist_30 = buscar_dados_historicos(cripto_id, 30)
            if not df_hist_30.empty:
                fig_30d = criar_grafico_historico(df_hist_30, f"{cripto_selecionada} - Últimos 30 Dias")
                if fig_30d:
                    st.plotly_chart(fig_30d, use_container_width=True)
                else:
                    st.warning("Não foi possível criar o gráfico.")
            else:
                st.info("📊 Dados históricos não disponíveis no momento. A API pode ter atingido o limite de requisições. Aguarde 1-2 minutos e clique em 'Atualizar Agora' na sidebar.")

else:
    st.warning("Nenhuma criptomoeda disponível para seleção.")

# ========== ATUALIZAÇÃO AUTOMÁTICA ==========
if auto_atualizar:
    # Usar placeholder para contagem regressiva
    placeholder = st.empty()
    
    for segundos_restantes in range(intervalo, 0, -1):
        placeholder.caption(f"🔄 Próxima atualização em: {segundos_restantes}s")
        time.sleep(1)
    
    placeholder.empty()
    st.cache_data.clear()
    st.rerun()