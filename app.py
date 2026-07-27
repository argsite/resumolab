import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="ResumoLab", page_icon="📋", layout="centered")

st.title("📋 ResumoLab (Modo Local / Sem IA)")
st.write("Faça o upload do PDF do laboratório para extrair os resultados de forma automática.")

uploaded_file = st.file_uploader("Escolha o arquivo PDF do exame", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extraindo dados do PDF..."):
        # 1. Extrai todo o texto do PDF
        texto_completo = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for pagina in pdf.pages:
                texto_completo += pagina.extract_text() + "\n"
        
        # 2. Função de busca por Regex corrigida com 'if' em inglês
        def extrair_valor(padrao, texto):
            match = re.search(padrao, texto, re.IGNORECASE)
            return match.group(1).strip() if match else "Não encontrado"

        # Extração baseada nos padrões do laudo do Lab. Cruzeiro
        glicose = extrair_valor(r"GLICOSE\s*\(Soro\)\s*\|\s*([\d,\.]+)", texto_completo)
        ureia = extrair_valor(r"Uréia\.\s*:\s*([\d,\.]+)", texto_completo)
        creatinina = extrair_valor(r"CREATININA\s*\(SORO\)[^\d]*([\d,\.]+)\s*mg/dL", texto_completo)
        colesterol_total = extrair_valor(r"COLESTEROL TOTAL:\s*([\d,\.]+)", texto_completo)
        hdl = extrair_valor(r"COLESTEROL HDL\.\s*([\d,\.]+)", texto_completo)
        ldl = extrair_valor(r"COLESTEROL LDL\.\s*:\s*([\d,\.]+)", texto_completo)
        triglicerides = extrair_valor(r"TRIGLICERIDES[^\d]*([\d,\.]+)", texto_completo)
        
        # 3. Monta o texto limpo em formato de texto puro para o prontuário
        resumo_formatado = f"""RESUL. LABS - LAB. CRUZEIRO
- Glicose (Soro): {glicose} mg/dL
- Ureia (Soro): {ureia} mg/dL
- Creatinina (Soro): {creatinina} mg/dL
- Colesterol Total: {colesterol_total} mg/dL
- Colesterol HDL: {hdl} mg/dL
- Colesterol LDL: {ldl} mg/dL
- Triglicérides: {triglicerides} mg/dL"""

        st.subheader("Resultado Pronto para o Prontuário:")
        st.text_area("Selecione, copie e cole abaixo:", resumo_formatado, height=250)
        st.success("Extração concluída com sucesso e sem uso de IA!")
