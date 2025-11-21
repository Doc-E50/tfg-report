# App interativo com Streamlit para visualização de TFG
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="Curva de TFG do Paciente", layout="centered")
st.title("?? Curva de Declínio da TFG")
st.markdown("Insira as estimativas de TFG com datas para visualizar a progressão renal do paciente comparada com cenários modelo.")

# Entrada de dados
with st.form("dados_tfg"):
    n = st.number_input("Quantas medidas de TFG deseja inserir?", min_value=2, max_value=20, value=5)
    dados = []
    for i in range(n):
        col1, col2 = st.columns([2, 1])
        with col1:
            data = st.date_input(f"Data {i+1}", key=f"data_{i}")
        with col2:
            tfg = st.number_input(f"TFG (mL/min) {i+1}", min_value=0.0, max_value=150.0, value=90.0, step=0.1, key=f"tfg_{i}")
        dados.append((data, tfg))
    submitted = st.form_submit_button("Gerar Gráfico")

if submitted:
    dados.sort()  # garantir ordem cronológica
    datas = [datetime.datetime.combine(d, datetime.time()) for d, _ in dados]
    tfgs = [v for _, v in dados]
    data_inicial = datas[0]
    meses_paciente = [(d - data_inicial).days / 30.44 for d in datas]

    # Modelos
    tfg_inicial = 90
    meses_modelo = np.arange(0, 61, 1)
    def declinio_lento(m): return tfg_inicial - (0.33 * m)
    def declinio_moderado(m): return tfg_inicial - (0.83 * m)
    def declinio_rapido(m): return tfg_inicial - (1.25 * m)

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(meses_modelo, declinio_lento(meses_modelo), '--', label='Declínio lento (~4 mL/ano)')
    ax.plot(meses_modelo, declinio_moderado(meses_modelo), '-', label='Declínio moderado (~10 mL/ano)')
    ax.plot(meses_modelo, declinio_rapido(meses_modelo), ':', label='Declínio rápido (~15 mL/ano)')
    ax.plot(meses_paciente, tfgs, 'o-r', linewidth=2.5, label='Paciente')

    ax.axhline(60, color='gray', linestyle='--', lw=0.5)
    ax.axhline(30, color='gray', linestyle='--', lw=0.5)
    ax.text(1, 61, "Estágio 2", fontsize=8, color='gray')
    ax.text(1, 31, "Estágio 3b", fontsize=8, color='gray')

    ax.set_title('Declínio da TFG estimada ao longo do tempo')
    ax.set_xlabel('Meses desde o primeiro exame')
    ax.set_ylabel('TFG (mL/min/1.73m²)')
    ax.set_ylim(0, 100)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.success("? Gráfico gerado com sucesso!")
