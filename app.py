import streamlit as st
import pdfplumber
from google import genai

st.set_page_config(page_title="ResumoLab", page_icon="📋", layout="centered")

st.title("📋 ResumoLab")
st.write("Faça o upload do PDF do laboratório para gerar o resumo limpo para o prontuário.")

# Configuração da chave de API do Gemini (pode ser colocada nos Secrets do Streamlit Cloud)
# O usuário configura a chave de segurança nas configurações do Streamlit Cloud
api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Insira sua Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Escolha o arquivo PDF do exame", type=["pdf"])

if uploaded_file is not None and api_key:
    with st.spinner("Lendo e formatando o laudo..."):
        # 1. Extrai o texto cru do PDF enviado
        texto_extraido = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for pagina in pdf.pages:
                texto_extraido += pagina.extract_text() + "\n"
        
        # 2. Configura o cliente da API do Gemini
        client = genai.Client(api_key=api_key)
        
        # 3. Prompt estrito para garantir texto puro sem formatações HTML ou marcações estranhas
        prompt = f"""
        Você é um assistente médico especialista em estruturação de prontuários.
        Analise o texto do laudo de laboratório abaixo e crie um resumo limpo, em TEXTO PURO (sem markdown complexo, sem negritos com asteriscos, sem tags HTML, sem códigos de marcação).
        Organize todos os exames em linhas separadas, agrupados por categorias, contendo o nome do exame, o resultado e o valor de referência entre parênteses.
        
        Texto do laudo:
        {texto_extraido}
        """
        
        # 4. Chamada ao modelo Gemini
                # Chamada ao modelo Gemini corrigida
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        
        resumo_limpo = response.text
        
        st.subheader("Resultado Pronto para o Prontuário:")
        st.text_area("Selecione, copie e cole abaixo:", resumo_limpo, height=400)
        st.success("Pronto! Nenhum código de marcação foi incluído.")

elif uploaded_file is not None and not api_key:
    st.warning("Por favor, informe a chave da API do Gemini para processar o documento.")
