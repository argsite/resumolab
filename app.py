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

        # Padrões para os exames bioquímicos, hematológicos, hormonais e vitaminas
        glicose = extrair_valor([r"GLICOSE\s*\(Soro\)\s*\|\s*([\d,\.]+)", r"GLICOSE.*?([\d,\.]+)\s*mg/dl"], texto_completo)
        ureia = extrair_valor([r"Uréia\.\s*:\s*([\d,\.]+)", r"Uréia[^\d]*([\d,\.]+)\s*mg/dl"], texto_completo)
        creatinina = extrair_valor([r"CREATININA\s*\(SORO\)[^\d]*([\d,\.]+)", r"Resultado:\s*([\d,\.]+)\s*mg/dL"], texto_completo)
        colesterol_total = extrair_valor([r"COLESTEROL TOTAL:\s*([\d,\.]+)", r"COLESTEROL TOTAL[^\d]*([\d,\.]+)\s*mg"], texto_completo)
        hdl = extrair_valor([r"COLESTEROL HDL\.\s*([\d,\.]+)", r"COLESTEROL\s*HDL[^\d]*([\d,\.]+)", r"HDL-COLESTEROL[^\d]*([\d,\.]+)\s*mg"], texto_completo)
        ldl = extrair_valor([r"COLESTEROL LDL\.\s*:\s*([\d,\.]+)", r"COLESTEROL\s*LDL[^\d]*([\d,\.]+)", r"LDL-COLESTEROL[^\d]*([\d,\.]+)\s*mg"], texto_completo)
        triglicerides = extrair_valor([r"TRIGLICERIDES[^\d]*([\d,\.]+)", r"TRIGLICERIDES[^\d]*:\s*([\d,\.]+)"], texto_completo)
        
        eritrocitos = extrair_valor([r"HEMÁCIAS\.\s*([\d,\.]+)", r"ERITRÓCITOS[^\d]*([\d,\.]+)\s*M"], texto_completo)
        hematocrito = extrair_valor([r"HEMATOCRITO\.\s*([\d,\.]+)", r"HEMATOCRITO[^\d]*([\d,\.]+)\s*%"], texto_completo)
        plaquetas = extrair_valor([r"PLAQUETAS\.\s*([\d,\.]+)", r"PLAQUETAS[^\d]*([\d,\.]+)"], texto_completo)
        leucocitos = extrair_valor([r"LEUCÓCITOS\.\s*([\d,\.]+)", r"LEUCÓCITOS[^\d]*([\d,\.]+)"], texto_completo)
        
        ferro_serico = extrair_valor([r"FERRO SÉRICO\s*([\d,\.]+)", r"FERRO.*?([\d,\.]+)\s*µg/dL"], texto_completo)
        tibc = extrair_valor([r"CAPACIDADE TOTAL DE LIGAÇÃO.*?([\d,\.]+)", r"TIBC.*?([\d,\.]+)\s*µg/dL"], texto_completo)
        sat_transferrina = extrair_valor([r"SATURAÇÃO DE TRANSFERRINA.*?([\d,\.]+)", r"TRANSFERRINA.*?([\d,\.]+)\s*%"], texto_completo)
        
        acido_urico = extrair_valor([r"ÁCIDO ÚRICO.*?([\d,\.]+)\s*mg/dl", r"ÁCIDO ÚRICO\.soro([\d,\.]+)\s*mg/dl"], texto_completo)
        sodio = extrair_valor([r"SÓDIO\.\s*soro\s*([\d,\.]+)", r"SÓDIO.*?([\d,\.]+)\s*mEq/L"], texto_completo)
        potassio = extrair_valor([r"POTÁSSIO\.\s*soro\s*([\d,\.]+)", r"POTÁSSIO.*?([\d,\.]+)\s*mEq/1"], texto_completo)
        
        calcio_total = extrair_valor([r"CÁLCIO TOTAL\s*([\d,\.]+)", r"CÁLCIO.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        calcio_ionizado = extrair_valor([r"CÁLCIO IONIZADO\s*([\d,\.]+)", r"CÁLCIO IONIZADO.*?([\d,\.]+)\s*mmol/L"], texto_completo)
        magnesio = extrair_valor([r"MAGNÉSIO\s*([\d,\.]+)", r"MAGNÉSIO.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        fosforo = extrair_valor([r"FÓSFORO\s*([\d,\.]+)", r"FÓSFORO.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        
        bilirrubina_total = extrair_valor([r"BILIRRUBINA TOTAL\.\s*([\d,\.]+)", r"BILIRRUBINA TOTAL.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        bilirrubina_direta = extrair_valor([r"BILIRRUBINA DIRETA\.\s*([\d,\.]+)", r"BILIRRUBINA DIRETA.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        bilirrubina_indireta = extrair_valor([r"BILIRRUBINA INDIRETA\.\s*([\d,\.]+)", r"BILIRRUBINA INDIRETA.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        
        proteinas_totais = extrair_valor([r"PROTEÍNAS TOTAIS\s*([\d,\.]+)", r"PROTEÍNAS TOTAIS.*?([\d,\.]+)\s*g/dL"], texto_completo)
        albumina = extrair_valor([r"ALBUMINA\s*([\d,\.]+)", r"ALBUMINA.*?([\d,\.]+)\s*g/dL"], texto_completo)
        globulinas = extrair_valor([r"GLOBULINAS\s*([\d,\.]+)", r"GLOBULINAS.*?([\d,\.]+)\s*g/dL"], texto_completo)
        
        pcr = extrair_valor([r"PROTEÍNA C REATIVA.*?([\d,\.]+)", r"PCR.*?([\d,\.]+)\s*mg/L"], texto_completo)
        vhs = extrair_valor([r"VELOCIDADE DE HEMOSSEDIMENTAÇÃO.*?([\d,\.]+)", r"VHS.*?([\d,\.]+)\s*mm/h"], texto_completo)
        
        tgo = extrair_valor([r"TGO\s*\(AST\.\s*([\d,\.]+)", r"TGO.*?([\d,\.]+)\s*U/L"], texto_completo)
        tgp = extrair_valor([r"TGP\s*\(ALT\)\s*([\d,\.]+)", r"TGP.*?([\d,\.]+)\s*U/L"], texto_completo)
        fosfatase = extrair_valor([r"FOSFATASE ALCALINA\.\s*([\d,\./]+)", r"FOSFATASE ALCALINA[^\d]*([\d,\./]+)"], texto_completo)
        gama_gt = extrair_valor([r"GAMA GLUTAMIL TRANSFERASE\s*([\d,\.]+)", r"GAMA GT.*?([\d,\.]+)\s*UI/l"], texto_completo)
        ferritina = extrair_valor([r"FERRITINA\.\s*([\d,\.]+)", r"FERRITINA.*?([\d,\.]+)\s*ng/ml"], texto_completo)

        insulina = extrair_valor([r"INSULINA\s*([\d,\.]+)", r"INSULINA.*?([\d,\.]+)\s*µUI/mL"], texto_completo)
        cortisol = extrair_valor([r"CORTISOL\s*([\d,\.]+)", r"CORTISOL.*?([\d,\.]+)\s*µg/dL"], texto_completo)
        testosterona_total = extrair_valor([r"TESTOSTERONA TOTAL\s*([\d,\.]+)", r"TESTOSTERONA.*?([\d,\.]+)\s*ng/dL"], texto_completo)
        estradiol = extrair_valor([r"ESTRADIOL\s*([\d,\.]+)", r"ESTRADIOL.*?([\d,\.]+)\s*pg/mL"], texto_completo)
        prolactina = extrair_valor([r"PROLACTINA\s*([\d,\.]+)", r"PROLACTINA.*?([\d,\.]+)\s*ng/mL"], texto_completo)
        psa_total = extrair_valor([r"PSA TOTAL\s*([\d,\.]+)", r"PSA.*?([\d,\.]+)\s*ng/mL"], texto_completo)

        vitamina_b12 = extrair_valor([r"VITAMINA B12.*?([\d,\.]+)\s*pg/mL", r"B12.*?([\d,\.]+)\s*pg/mL"], texto_completo)
        vitamina_d = extrair_valor([r"VITAMINA D - 25 HIDROXI.*?([\d,\.]+)\s*ng/mL", r"25 HIDROXI.*?([\d,\.]+)\s*ng/mL"], texto_completo)
        tsh = extrair_valor([r"TSH - HORMÔNIO TIREOESTIMULANTE.*?([\d,\.]+)\s*μUI/mL", r"TSH.*?([\d,\.]+)\s*μUI"], texto_completo)
        t4 = extrair_valor([r"T4- TETRAIODOTIROXINA.*?([\d,\.]+)\s*µg/dL", r"T4.*?([\d,\.]+)\s*µg/dL"], texto_completo)
        hba1c = extrair_valor([r"Hb A1c:\s*([\d,\.]+)\s*%", r"Hemoglobina Glicada.*?([\d,\.]+)\s*%"], texto_completo)

        creatinina_urinaria = extrair_valor([r"CREATININA URINÁRIA.*?([\d,\.]+)", r"CREATININA URINÁRIA.*?([\d,\.]+)\s*mg/dL"], texto_completo)
        microalbuminuria = extrair_valor([r"MICROALBUMINÚRIA.*?([\d,\.]+)", r"MICROALBUMINÚRIA.*?([\d,\.]+)\s*mg/24h"], texto_completo)

        # Padrões ajustados e blindados para a seção de EAS (Urina Tipo I)
        urina_cor = extrair_valor([r"URINA TIPO I.*?Exame Físico.*?Cor\s*[:\|]\s*([A-Za-zÀ-Ú\s]+)(?=\nAspecto)", r"Exame Físico.*?Cor\s*\|\s*([A-Za-zÀ-Ú\s]+)(?=\n)"], texto_completo)
        urina_aspecto = extrair_valor([r"URINA TIPO I.*?Aspecto\s*[:\|]\s*([A-Za-zÀ-Ú\s]+)(?=\nDensidade)", r"Aspecto\s*\|\s*([A-Za-zÀ-Ú\s]+)(?=\n)"], texto_completo)
        urina_densidade = extrair_valor([r"Densidade\s*[:\|]\s*([\d,\.]+)", r"Densidade\s*([0-9\.]+)"], texto_completo)
        urina_ph = extrair_valor([r"PH\s*[:\|]\s*([\d,\.]+)", r"PH\s*([0-9\.]+)"], texto_completo)
        urina_proteinas = extrair_valor([r"Exame Químico.*?Proteínas\s*[:\|]\s*([A-Za-zÀ-Ú]+)", r"Proteínas\s*\|\s*([A-Za-zÀ-Ú]+)"], texto_completo)
        urina_glicose = extrair_valor([r"GLICOSE\.\.\s*[:\|]\s*([A-Za-zÀ-Ú]+)", r"GLICOSE\.\.\s*\|\s*([A-Za-zÀ-Ú]+)"], texto_completo)
        urina_nitrito = extrair_valor([r"Nitrito\s*[:\|]\s*\.*\s*([A-Za-zÀ-Ú]+)", r"Nitrito\s*\|\s*([A-Za-zÀ-Ú]+)"], texto_completo)

        # 3. Monta o texto limpo para o prontuário
        resumo_formatado = f"""RESUL. LABS - LAB. CRUZEIRO
- Glicose (Soro): {glicose} mg/dL
- Ureia (Soro): {ureia} mg/dL
- Creatinina (Soro): {creatinina} mg/dL
- Colesterol Total: {colesterol_total} mg/dL
- Colesterol HDL: {hdl} mg/dL
- Colesterol LDL: {ldl} mg/dL
- Triglicérides: {triglicerides} mg/dL
- Eritrócitos: {eritrocitos} milhões/µL
- Hematócrito: {hematocrito}%
- Plaquetas: {plaquetas} mil/µL
- Leucócitos Totais: {leucocitos} /µL
- Ferro Sérico: {ferro_serico} µg/dL
- TIBC: {tibc} µg/dL
- Saturação de Transferrina: {sat_transferrina}%
- Ácido Úrico (Soro): {acido_urico} mg/dL
- Sódio (Soro): {sodio} mEq/L
- Potássio (Soro): {potassio} mEq/L
- Cálcio Total: {calcio_total} mg/dL
- Cálcio Ionizado: {calcio_ionizado} mmol/L
- Magnésio (Soro): {magnesio} mg/dL
- Fósforo (Soro): {fosforo} mg/dL
- Bilirrubina Total: {bilirrubina_total} mg/dL
- Bilirrubina Direta: {bilirrubina_direta} mg/dL
- Bilirrubina Indireta: {bilirrubina_indireta} mg/dL
- Proteínas Totais: {proteinas_totais} g/dL
- Albumina (Soro): {albumina} g/dL
- Globulinas: {globulinas} g/dL
- Proteína C Reativa (PCR): {pcr} mg/L
- VHS: {vhs} mm/h
- TGO (AST): {tgo} U/L
- TGP (ALT): {tgp} U/L
- Fosfatase Alcalina: {fosfatase} U/L
- Gama GT: {gama_gt} UI/L
- Ferritina: {ferritina} ng/mL
- Insulina (Soro): {insulina} µUI/mL
- Cortisol Basal: {cortisol} µg/dL
- Testosterona Total: {testosterona_total} ng/dL
- Estradiol: {estradiol} pg/mL
- Prolactina: {prolactina} ng/mL
- PSA Total: {psa_total} ng/mL
- Vitamina B12: {vitamina_b12} pg/mL
- Vitamina D: {vitamina_d} ng/mL
- TSH: {tsh} µUI/mL
- T4 Livre: {t4} µg/dL
- Hemoglobina Glicada (HbA1c): {hba1c}%
- Creatinina Urinária: {creatinina_urinaria} mg/dL
- Microalbuminúria: {microalbuminuria} mg/24h
- Urina EAS - Cor: {urina_cor}
- Urina EAS - Aspecto: {urina_aspecto}
- Urina EAS - Densidade: {urina_densidade}
- Urina EAS - pH: {urina_ph}
- Urina EAS - Proteínas: {urina_proteinas}
- Urina EAS - Glicose: {urina_glicose}
- Urina EAS - Nitrito: {urina_nitrito}"""

        st.subheader("Resultado Pronto para o Prontuário:")
        st.text_area("Selecione, copie e cole abaixo:", resumo_formatado, height=350)
        
        # Botão interativo para copiar direto para o clipboard
        text_to_copy = resumo_formatado.replace('\n', '\\n').replace('"', '\\"')
        html_code = f"""
        <button onclick="navigator.clipboard.writeText('{text_to_copy}'); alert('Texto copiado para a área de transferência!');" 
        style="background-color: #ff4b4b; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; font-weight: 600; cursor: pointer; width: 100%;">
            📋 Copiar para o Prontuário
        </button>
        """
        st.components.v1.html(html_code, height=45)
        
        st.success("Extração otimizada concluída com sucesso!")
