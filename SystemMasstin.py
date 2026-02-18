import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Apontamentos Masstin",
    layout="wide",
    page_icon="❄️"
)

# ==============================
# ESTRUTURA DE DADOS
# ==============================
COLUNAS = [
    "Data", "Técnico", "Cliente", "Equipamento", "Tipo", "Status", "Horas",
    "Frequencia",

    # Mensal
    "Temp_Ambiente", "Temp_Externo", "Bandeja_Dreno", "Limpeza_Componentes",
    "Controle_Remoto", "Filtro_Retorno", "Filtro_TAE",

    # Semestral
    "Reaperto_Terminais", "Isolamento_Termoacustico", "Vibracoes_Vazamentos",
    "Tubulacao_Isolamento", "Serpentina_Bandeja", "Ferrugem",
    "Suporte_Equip", "Condensador",

    # Campos finais
    "Atividade_Executada", "Pecas_Utilizadas", "Orcar",
    "Recomendacoes", "Fluido", "Qtd_Fluido", "OBS"
]

DB_FILE = "log_atividades_masstin.csv"

# ==============================
# FUNÇÕES
# ==============================
def carregar_dados():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE, sep=";", encoding="utf-8-sig")
            if list(df.columns) == COLUNAS:
                return df
        except:
            pass
    return pd.DataFrame(columns=COLUNAS)

def salvar_dados(df):
    df.to_csv(DB_FILE, index=False, sep=";", encoding="utf-8-sig")

def gerar_pdf(row):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "ORDEM DE SERVIÇO - MASSTIN", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=8)
    for col in COLUNAS:
        valor = "-" if pd.isna(row[col]) or row[col] == "" else str(row[col])
        pdf.set_font("Arial", "B", 8)
        pdf.cell(65, 6, col.replace("_", " "), border=1)
        pdf.set_font("Arial", size=8)
        pdf.cell(125, 6, valor, border=1, ln=True)

    return pdf.output(dest="S").encode("latin-1")

# ==============================
# CARGA INICIAL
# ==============================
df = carregar_dados()

# ==============================
# SIDEBAR – DADOS BÁSICOS
# ==============================
st.sidebar.title("Apontamentos Masstin")

data_servico = st.sidebar.date_input("Data", datetime.now())
tecnico = st.sidebar.selectbox("Técnico", ["João Silva", "Maria Souza", "Carlos Tech", "Equipe A"])
cliente = st.sidebar.selectbox("Cliente", [
    "PREVENT SENIOR", "DOW GUARUJA", "KLABIN SAS", "EKURITO", "OXITENO MAUA",
    "PETROCOQUE", "KRONES", "CROMUS", "UNIMED FESP", "WESTPHARMA",
    "HOSPITAL ALBERT EINSTEIN", "HOSPITAL SAO CAMILO"
])
equip = st.sidebar.selectbox("Equipamento", ["Split", "Chiller", "FanCoil", "Self", "Câmara Fria"])
tipo = st.sidebar.radio("Tipo de Serviço", ["Preventiva", "Corretiva", "Instalação"])
status = st.sidebar.selectbox("Status", ["Concluído", "Pendente (Peça)", "Em Aberto"])
horas = st.sidebar.number_input("Horas", min_value=0.5, step=0.5)

# ==============================
# ÁREA CENTRAL – PREVENTIVA SPLIT
# ==============================
st.title("📊 Painel Operacional HVAC")

dados_tecnicos = {c: "" for c in COLUNAS[7:]}

if tipo == "Preventiva" and equip == "Split":
    st.subheader("🛠️ Checklist Técnico – Preventiva (Split)")

    dados_tecnicos["Frequencia"] = st.selectbox(
        "Frequência",
        ["Mensal", "Trimestral", "Semestral"]
    )

    # ---------------- MENSAL ----------------
    st.markdown("### 📆 Atividades Mensais")

    dados_tecnicos["Temp_Ambiente"] = st.text_input("[27] Medir temperatura ambiente (°C)")
    dados_tecnicos["Temp_Externo"] = st.text_input("[29] Medir temperatura ar externo (°C)")
    dados_tecnicos["Bandeja_Dreno"] = st.selectbox("[76] Bandejas e dreno", ["OK", "Limpeza Realizada", "Obstruído"])
    dados_tecnicos["Limpeza_Componentes"] = st.selectbox("[26] Limpeza do equipamento", ["OK", "Realizada"])
    dados_tecnicos["Controle_Remoto"] = st.selectbox("[65] Testar controle remoto", ["OK", "Defeito"])
    dados_tecnicos["Filtro_Retorno"] = st.selectbox("[53] Limpar filtro retorno", ["Limpo", "Trocado"])
    dados_tecnicos["Filtro_TAE"] = st.selectbox("[53] Limpar filtro TAE", ["Limpo", "Trocado", "N/A"])

    # ---------------- SEMESTRAL ----------------
    if dados_tecnicos["Frequencia"] == "Semestral":
        st.markdown("### 📆 Atividades Semestrais")

        dados_tecnicos["Reaperto_Terminais"] = st.selectbox("[13] Reaperto dos terminais", ["OK", "Ajustado"])
        dados_tecnicos["Isolamento_Termoacustico"] = st.selectbox("[95] Isolamento termo-acústico", ["Bom", "Danificado"])
        dados_tecnicos["Vibracoes_Vazamentos"] = st.selectbox("[5] Vibrações / vazamentos", ["Normal", "Corrigido"])
        dados_tecnicos["Tubulacao_Isolamento"] = st.selectbox("[7] Tubulação / isolamento térmico", ["Bom", "Regular", "Ruim"])
        dados_tecnicos["Serpentina_Bandeja"] = st.selectbox("[24] Limpeza serpentina e bandeja", ["OK", "Realizada"])
        dados_tecnicos["Ferrugem"] = st.selectbox("[25] Pontos de ferrugem", ["Não possui", "Tratado"])
        dados_tecnicos["Suporte_Equip"] = st.selectbox("[103] Suporte do equipamento", ["OK", "Ajustado"])
        dados_tecnicos["Condensador"] = st.selectbox("[23] Lavar conjunto condensador", ["OK", "Lavado"])

    # ---------------- CAMPOS FINAIS ----------------
    st.markdown("### 📝 Informações Complementares")

    dados_tecnicos["Atividade_Executada"] = st.text_area("Atividade executada")
    dados_tecnicos["Pecas_Utilizadas"] = st.text_input("Peças utilizadas")
    dados_tecnicos["Orcar"] = st.selectbox("Precisa orçar alguma atividade ou peça?", ["Não", "Sim"])
    dados_tecnicos["Recomendacoes"] = st.text_area("Recomendações")
    dados_tecnicos["Fluido"] = st.text_input("Fluido utilizado")
    dados_tecnicos["Qtd_Fluido"] = st.text_input("Quantidade de fluido (g)")
    dados_tecnicos["OBS"] = st.text_area("Observações")

    st.divider()

# ==============================
# SALVAR
# ==============================
if st.sidebar.button("💾 SALVAR REGISTRO"):
    nova_linha = [
        data_servico.strftime("%d/%m/%Y"), tecnico, cliente, equip, tipo, status, horas,
        dados_tecnicos["Frequencia"],

        dados_tecnicos["Temp_Ambiente"], dados_tecnicos["Temp_Externo"],
        dados_tecnicos["Bandeja_Dreno"], dados_tecnicos["Limpeza_Componentes"],
        dados_tecnicos["Controle_Remoto"], dados_tecnicos["Filtro_Retorno"],
        dados_tecnicos["Filtro_TAE"],

        dados_tecnicos["Reaperto_Terminais"], dados_tecnicos["Isolamento_Termoacustico"],
        dados_tecnicos["Vibracoes_Vazamentos"], dados_tecnicos["Tubulacao_Isolamento"],
        dados_tecnicos["Serpentina_Bandeja"], dados_tecnicos["Ferrugem"],
        dados_tecnicos["Suporte_Equip"], dados_tecnicos["Condensador"],

        dados_tecnicos["Atividade_Executada"], dados_tecnicos["Pecas_Utilizadas"],
        dados_tecnicos["Orcar"], dados_tecnicos["Recomendacoes"],
        dados_tecnicos["Fluido"], dados_tecnicos["Qtd_Fluido"],
        dados_tecnicos["OBS"]
    ]

    df = pd.concat([df, pd.DataFrame([nova_linha], columns=COLUNAS)], ignore_index=True)
    salvar_dados(df)
    st.success("✅ Registro salvo com sucesso")
    st.rerun()

# ==============================
# HISTÓRICO
# ==============================
if not df.empty:
    for i, row in df.iterrows():
        with st.expander(f"{row['Data']} | {row['Cliente']} | {row['Equipamento']}"):
            st.write(row)
            st.download_button(
                "📄 PDF OS",
                gerar_pdf(row),
                f"OS_{i}.pdf",
                "application/pdf",
                key=f"pdf_{i}"
            )
else:
    st.info("Nenhum registro cadastrado.")
