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
        
        # 2. Função de busca flexível por Regex
        def extrair_valor(padroes, texto):
            for padrao in padroes:
                match = re.search(padrao, texto, re.IGNORECASE | re.DOTALL)
                if match:
                    val = match.group(1).strip()
                    if val and not val.startswith('.'):
                        return val
            return "Não encontrado"

        # Padrões para os exames já existentes e os novos adicionados
        glicose = extrair_valor([r"GLICOSE\s*\(Soro\)\s*[:\.]*[\s\|]*([\d,\.]+)", r"GLICOSE.*?([\d,\.]+)\s*mg/dl"], texto_completo)
        ureia = extrair_valor([r"Uréia\.\s*:\s*([\d,\.]+)", r"Uréia[^\d]*([\d,\.]+)\s*mg/dl"], texto_completo)
        creatinina = extrair_valor([r"CREATININA\s*\(SORO\)[^\d]*([\d,\.]+)", r"Resultado:\s*([\d,\.]+)\s*mg/dL"], texto_completo)
        colesterol_total = extrair_valor([r"COLESTEROL TOTAL:\s*([\d,\.]+)", r"COLESTEROL TOTAL[^\d]*([\d,\.]+)\s*mg"], texto_completo)
        hdl = extrair_valor([r"COLESTEROL HDL\.\s*[\.:]*\s*([\d,\.]+)", r"COLESTEROL\s*HDL[^\d]*([\d,\.]+)", r"HDL-COLESTEROL[^\d]*([\d,\.]+)\s*mg"], texto_completo)
        ldl = extrair_valor([r"COLESTEROL LDL\.\s*:\s*([\d,\.]+)", r"COLESTEROL\s*LDL[^\d]*([\d,\.]+)", r"LDL-COLESTEROL[^\d]*([\d,\.]+)\s*mg"], texto_completo)
        triglicerides = extrair_valor([r"TRIGLICERIDES[^\d]*([\d,\.]+)", r"TRIGLICERIDES[^\d]*:\s*([\d,\.]+)"], texto_completo)
        
        # Novos exames adicionados deste arquivo:
        tgo = extrair_valor([r"TGO\s*\(AST\.\s*([\d,\.]+)", r"TGO.*?([\d,\.]+)\s*U/L"], texto_completo)
        tgp = extrair_valor([r"TGP\s*\(ALT\)\s*([\d,\.]+)", r"TGP.*?([\d,\.]+)\s*U/L"], texto_completo)
        fosfatase = extrair_valor([r"FOSFATASE ALCALINA\.\s*([\d,\./]+)", r"FOSFATASE ALCALINA[^\d]*([\d,\./]+)"], texto_completo)
        gama_gt = extrair_valor([r"GAMA GLUTAMIL TRANSFERASE\s*([\d,\.]+)", r"GAMA GT.*?([\d,\.]+)\s*UI/l"], texto_completo)
        ferritina = extrair_valor([r"FERRITINA\.\s*([\d,\.]+)", r"FERRITINA.*?([\d,\.]+)\s*ng/ml"], texto_completo)

        # 3. Monta o texto limpo para o prontuário com todos os parâmetros
        resumo_formatado = f"""RESUL. LABS - LAB. CRUZEIRO
- Glicose (Soro): {glicose} mg/dL
- Ureia (Soro): {ureia} mg/dL
- Creatinina (Soro): {creatinina} mg/dL
- Colesterol Total: {colesterol_total} mg/dL
- Colesterol HDL: {hdl} mg/dL
- Colesterol LDL: {ldl} mg/dL
- Triglicérides: {triglicerides} mg/dL
- TGO (AST): {tgo} U/L
- TGP (ALT): {tgp} U/L
- Fosfatase Alcalina: {fosfatase} U/L
- Gama GT: {gama_gt} UI/L
- Ferritina: {ferritina} ng/mL"""

        st.subheader("Resultado Pronto para o Prontuário:")
        st.text_area("Selecione, copie e cole abaixo:", resumo_formatado, height=300)
        st.success("Extração expandida concluída com sucesso!")
