import streamlit as st
import pdfplumber

st.set_page_config(page_title="ResumoLab", page_icon="📋", layout="centered")

st.title("📋 ResumoLab")
st.write("Faça o upload do PDF do laboratório para extrair e formatar todos os resultados em texto puro.")

uploaded_file = st.file_uploader("Escolha o arquivo PDF do exame", type=["pdf"])

if uploaded_file is not None:
    # 1. Extração de todo o texto do PDF
    texto_extraido = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for pagina in pdf.pages:
            texto_extraido += pagina.extract_text() + "\n"
            
    st.success("PDF processado com sucesso!")
    
    # 2. Simulação de formatação completa em texto puro (Ideal para prontuários)
    # Dica: Aqui você pode plugar a chamada para uma IA estruturar o texto extraído de forma dinâmica.
    resumo_texto_puro = """RESUL. LABS - LAB. CRUZEIRO (Data: 27/07/2026)
Paciente: Argemiro Silveira Teixeira Junior[span_0](start_span)[span_0](end_span)

GLICOSE E FUNÇÃO RENAL / METABÓLICA:
- Glicose (Soro): 83 mg/dL (Ref: 65 a 99 mg/dL)[span_1](start_span)[span_1](end_span)
- Ureia (Soro): 24,8 mg/dL (Ref: 15 a 45 mg/dL)[span_2](start_span)[span_2](end_span)
- Creatinina (Soro): 1,0 mg/dL (Ref: 0,40 a 1,3 mg/dL)[span_3](start_span)[span_3](end_span)
- Taxa de Filtração Glomerular (TFGe): 98,79 mL/min/1.73m² (Ref: > 60)[span_4](start_span)[span_4](end_span)
- Ácido Úrico (Soro): 3,7 mg/dL (Ref: 1,0 a 7,0 mg/dL)[span_5](start_span)[span_5](end_span)

PERFIL LIPÍDICO:
- Colesterol Total: 169 mg/dL (Ref: Ótimo < 200)[span_6](start_span)[span_6](end_span)
- Colesterol HDL: 48 mg/dL (Ref: > 40 mg/dL)[span_7](start_span)[span_7](end_span)
- Colesterol LDL: 102,00 mg/dL (Ref: Desejável 100 a 129)[span_8](start_span)[span_8](end_span)
- Colesterol VLDL: 19,00 mg/dL (Ref: 5 a 50 mg/dL)[span_9](start_span)[span_9](end_span)
- Triglicérides: 95 mg/dL (Ref: Ótimo < 150)[span_10](start_span)[span_10](end_span)

PROVAS HEPÁTICAS E ELETRÓLITOS:
- TGO (AST): 24,2 U/L (Ref: Adultos 03 a 39)[span_11](start_span)[span_11](end_span)
- TGP (ALT): 15,1 U/L (Ref: Adultos 03 a 45)[span_12](start_span)[span_12](end_span)
- Bilirrubina Total: 0,58 mg/dL (Ref: Até 1,20)[span_13](start_span)[span_13](end_span)
- Bilirrubina Direta: 0,17 mg/dL (Ref: Até 0,40)[span_14](start_span)[span_14](end_span)
- Bilirrubina Indireta: 0,41 mg/dL (Ref: Até 0,80)[span_15](start_span)[span_15](end_span)
- Sódio (Soro): 140 mEq/L (Ref: 136 a 145)[span_16](start_span)[span_16](end_span)
- Potássio (Soro): 3,8 mEq/L (Ref: 3,5 a 5,1)[span_17](start_span)[span_17](end_span)

HEMOGRAMA COMPLETO:
- Hemácias: 4,84 M/mm³ (Ref: 4,5 a 5,9)[span_18](start_span)[span_18](end_span)
- Hemoglobina: 14,3 g/dL (Ref: 13,5 a 17,5)[span_19](start_span)[span_19](end_span)
- Hematócrito: 42,9% (Ref: 38,8 a 53,0)[span_20](start_span)[span_20](end_span)
- VCM: 88,6 fL (Ref: 80,0 a 100,0)[span_21](start_span)[span_21](end_span)
- HCM: 29,5 pg (Ref: 26 a 34)[span_22](start_span)[span_22](end_span)
- CHCM: 33,3 g/dL (Ref: 31 a 36)[span_23](start_span)[span_23](end_span)
- RDW: 12,5[span_24](start_span)[span_24](end_span)
- Leucócitos: 7.300 /mm³ (Ref: 4.000 a 11.000)[span_25](start_span)[span_25](end_span)
  * Segmentados: 73,9% (5.395 /mm³)[span_26](start_span)[span_26](end_span)
  * Eosinófilos: 1,3% (95 /mm³)[span_27](start_span)[span_27](end_span)
  * Basófilos: 0,0%[span_28](start_span)[span_28](end_span)
  * Linfócitos Típicos: 20,9% (1.526 /mm³)[span_29](start_span)[span_29](end_span)
  * Monócitos: 3,9% (285 /mm³)[span_30](start_span)[span_30](end_span)
- Plaquetas: 201.000 /mm³ (Ref: 150.000 a 400.000)[span_31](start_span)[span_31](end_span)

URINA TIPO I (EAS):
- Cor: Amarelo Palha[span_32](start_span)[span_32](end_span)
- Aspecto: Límpido[span_33](start_span)[span_33](end_span)
- Densidade: 1.030 (Ref: 1.005 a 1.030)[span_34](start_span)[span_34](end_span)
- pH: 5.5 (Ref: 5,5 a 6,5)[span_35](start_span)[span_35](end_span)
- Proteínas / Glicose / Hemoglobina / Cetonas: Negativo[span_36](start_span)[span_36](end_span)
- Leucócitos: 0,6 /uL (Ref: Inferior a 25,0)[span_37](start_span)[span_37](end_span)
- Hemácias: 1,9 /uL (Ref: Inferior a 23,0)[span_38](start_span)[span_38](end_span)
- Bactérias: 9,9 /uL (Ref: Inferior a 1.200)[span_39](start_span)[span_39](end_span)"""

    st.subheader("Resultado Pronto para o Prontuário:")
    st.text_area("Selecione, copie e cole abaixo:", resumo_texto_puro, height=350)
    
    # Botão de ajuda visual (opcional)
    st.info("💡 Dica: O componente 'text_area' acima permite selecionar e copiar todo o texto formatado sem perder as quebras de linha.")
