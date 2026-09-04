import streamlit as st
import pandas as pd
import joblib
import time
import random

# 1. Configuração da Página
st.set_page_config(page_title="Zeladoria Preditiva", page_icon="🌊", layout="wide")

@st.cache_resource
def carregar_modelo():
    try:
        return joblib.load('modelo_bueiros.pkl')
    except FileNotFoundError:
        st.error("Erro: Arquivo 'modelo_bueiros.pkl' não encontrado. Execute o treinamento primeiro.")
        return None

modelo = carregar_modelo()

st.title("🌊 Sistema Preditivo de Zeladoria Urbana")
st.markdown("Monitoramento IoT e priorização de limpeza de bueiros baseada em IA para prevenção de enchentes.")
st.divider()

if modelo:
    st.sidebar.header("📡 Recepção de Dados (Sensor/Clima)")
    
    # Adicionamos a opção de ligar o Simulador Contínuo
    simulacao_ativa = st.sidebar.checkbox("🔴 Ligar Arduino Virtual (Tempo Real)")
    
    bueiro_id = st.sidebar.text_input("ID do Bueiro Monitorado", "BUE-1042")
    
    # Se o simulador estiver desligado, funciona do jeito manual de antes
    if not simulacao_ativa:
        obstrucao = st.sidebar.slider("Nível de Lixo/Obstrução (%)", 0, 100, 85)
        chuva = st.sidebar.slider("Previsão de Chuva 24h (mm)", 0, 150, 60)
        historico = st.sidebar.slider("Histórico de Alagamento (0-10)", 0, 10, 8)

        if st.sidebar.button("Processar Leitura do Sensor"):
            entrada = pd.DataFrame([[obstrucao, chuva, historico]], columns=['obstrucao_sensor_percentual', 'previsao_chuva_24h_mm', 'historico_alagamento_regiao'])
            risco = modelo.predict(entrada)[0]
            
            if risco == 1:
                st.error(f"⚠️ ALERTA CRÍTICO: O bueiro **{bueiro_id}** tem risco iminente de causar enchente!")
            else:
                st.success(f"✅ O bueiro **{bueiro_id}** está seguro e operando dentro da margem normal.")
    
    # Se o simulador estiver ligado, ele roda um loop contínuo
    else:
        st.sidebar.warning("Simulador rodando! Gerando dados a cada 2 segundos...")
        chuva_fixa = st.sidebar.slider("Fixar Previsão de Chuva (mm)", 0, 150, 80)
        historico_fixo = 8
        
        # Espaço reservado na tela para atualizar os dados sem piscar
        painel_tempo_real = st.empty()
        
        # Loop de simulação
        for _ in range(50): # Vai simular 50 leituras
            # Simula a leitura variando do sensor ultrassônico
            lixo_simulado = random.randint(10, 95) 
            
            entrada = pd.DataFrame([[lixo_simulado, chuva_fixa, historico_fixo]], columns=['obstrucao_sensor_percentual', 'previsao_chuva_24h_mm', 'historico_alagamento_regiao'])
            risco = modelo.predict(entrada)[0]
            
            # Atualiza a interface gráfica em tempo real
            with painel_tempo_real.container():
                st.subheader(f"Leitura ao vivo: {bueiro_id}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Obstrução (Sensor IoT)", f"{lixo_simulado}%")
                col2.metric("Chuva Esperada", f"{chuva_fixa} mm")
                
                if risco == 1:
                    col3.error("🚨 RISCO DE ENCHENTE")
                else:
                    col3.success("🟢 NORMAL")
            
            time.sleep(2) # Espera 2 segundos antes de mandar a próxima leitura