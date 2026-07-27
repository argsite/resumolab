import streamlit as st
import pdfplumber

st.title("Extrator de Laudos para Prontuário Médico")
st.write("Faça o upload do PDF do laboratório para gerar o resumo formatado.")

# Componente para upload do PDF
uploaded_file = st.file_uploader("Escolha o arquivo PDF do exame", type=["pdf"])

if uploaded_file is not None:
    # Extraindo o texto do PDF usando pdfplumber
    texto_extraido = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for pagina in pdf.pages:
            texto_extraido += pagina.extract_text() + "\n"
            
    st.subheader("Texto Bruto Extraído:")
    st.text_area("Original", texto_extraido, height=200)
    
    # Aqui você integraria a lógica de limpeza/IA para estruturar os dados
    st.subheader("Sugestão Pronta para o Prontuário:")
    
    # Exemplo simulado de saída estruturada baseada no documento do paciente Argemiro[span_0](start_span)[span_0](end_span)
    resumo_prontuario = """
    RESUL. LABS (Data: 27/07/2026) - Lab. Cruzeiro[span_1](start_span)[span_1](end_span)
    * Glicose Jejum: 83 mg/dL (Ref: 65 a 99)[span_2](start_span)[span_2](end_span)
    * Urina Tipo I: Densidade 1.030, pH 5.5, Negativo para proteínas/glicose/hemoglobina[span_3](start_span)[span_3](end_span)
    * Hemograma: Hb 14.3 g/dL, Ht 42.9%, Leucócitos 7.300/mm³, Plaquetas 201.000[span_4](start_span)[span_4](end_span)
    * Perfil Lipídico: Colesterol Total 169 | HDL 48 | LDL 102 | Triglicérides 95 mg/dL[span_5](start_span)[span_5](end_span)
    * Função Renal: Ureia 24.8 | Creatinina 1.0 mg/dL (TFGe: 98.79 mL/min)[span_6](start_span)[span_6](end_span)
    """
    
    st.code(resumo_prontuario, language="markdown")
    st.success("Pronto para copiar e colar no prontuário!")
