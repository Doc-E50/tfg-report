# -*- coding: utf-8 -*-

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Relatório de TFG", layout="centered")
st.title("📉 Gerador de Relatório de TFG")

st.markdown("Preencha os dados do paciente e os valores de TFG para gerar o gráfico e o PDF.")

# -------------------------
# CAMPOS DO PACIENTE
# -------------------------
st.header("🧑 Dados do Paciente")

nome = st.text_input("Nome completo")
idade = st.number_input("Idade", min_value=0, max_value=120, value=60)
doenca_base = st.text_input("Doença de Base (ex: Diabetes Mellitus, HAS, DRC...)")

# -------------------------
# ENTRADA DE TFG
# -------------------------
st.header("📅 Valores de TFG")

n = st.number_input("Quantas medidas deseja inserir?", min_value=2, max_value=20, value=5)
dados = []

with st.form("dados_form"):
    for i in range(n):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input(f"Data {i+1}", key=f"data_{i}")
        with col2:
            tfg = st.number_input(f"TFG estimada {i+1} (mL/min)", min_value=0.0, max_value=150.0, key=f"tfg_{i}")
        dados.append((data, tfg))
    gerar = st.form_submit_button("Gerar Relatório")

# -------------------------
# GERAÇÃO DO GRÁFICO
# -------------------------
if gerar:

    # Organizar dados
    dados.sort()
    datas = [datetime.datetime.combine(d, datetime.time()) for d, _ in dados]
    tfgs = [v for _, v in dados]
    data_inicio = datas[0]
    meses = [(d - data_inicio).days / 30.44 for d in datas]

    # Curvas modelo
    x_modelo = np.arange(0, 61, 1)
    declinio_lento = 90 - 0.33 * x_modelo
    declinio_moderado = 90 - 0.83 * x_modelo
    declinio_rapido = 90 - 1.25 * x_modelo

    # Plot do gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x_modelo, declinio_lento, '--', label='Lento (~4 mL/ano)', color='blue')
    ax.plot(x_modelo, declinio_moderado, '-', label='Moderado (~10 mL/ano)', color='green')
    ax.plot(x_modelo, declinio_rapido, ':', label='Rápido (~15 mL/ano)', color='orange')
    ax.plot(meses, tfgs, 'o-r', label='Paciente', linewidth=2.5)
    ax.axhline(60, color='gray', linestyle='--', lw=0.5)
    ax.axhline(30, color='gray', linestyle='--', lw=0.5)
    ax.set_title('Evolução da TFG estimada')
    ax.set_xlabel('Meses desde o primeiro exame')
    ax.set_ylabel('TFG (mL/min/1.73m²)')
    ax.set_ylim(0, 100)
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.success("✅ Gráfico gerado com sucesso!")

# -------------------------
# GERAÇÃO DO PDF
# -------------------------
from reportlab.lib.utils import ImageReader
st.header("📄 Download do Relatório em PDF")

buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=A4)

# Cabeçalho
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 800, "Relatório de Evolução da TFG")

# Dados do paciente
c.setFont("Helvetica", 12)
c.drawString(50, 770, f"Nome: {nome}")
c.drawString(50, 750, f"Idade: {idade}")
c.drawString(50, 730, f"Doença de Base: {doenca_base}")

# Inserir o gráfico
img_buffer = BytesIO()
fig.savefig(img_buffer, format="png", dpi=150, bbox_inches="tight")
img_buffer.seek(0)

# CONVERSÃO CORRETA PARA IMAGE READER
img_reader = ImageReader(img_buffer)

c.drawImage(img_reader, 40, 380, width=520, height=300)

c.showPage()
c.save()

buffer.seek(0)

st.download_button(
    label="📥 Baixar PDF",
    data=buffer,
    file_name="relatorio_tfg.pdf",
    mime="application/pdf"
)
