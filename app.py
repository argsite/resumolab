import re
import unicodedata
from collections import OrderedDict

import pdfplumber
import streamlit as st


def aplicar_estilo():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(1, 105, 111, 0.08), transparent 28%),
                linear-gradient(180deg, #f7f6f2 0%, #f2f0ea 100%);
            color: #28251d;
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            max-width: 980px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
        .hero-card {
            background: rgba(249, 248, 245, 0.92);
            border: 1px solid rgba(40, 37, 29, 0.08);
            border-radius: 20px;
            padding: 1.4rem 1.4rem 1.1rem 1.4rem;
            box-shadow: 0 10px 30px rgba(40, 37, 29, 0.06);
            margin-bottom: 1rem;
        }
        .hero-badge {
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 600;
            color: #0c4e54;
            background: rgba(1, 105, 111, 0.10);
            border: 1px solid rgba(1, 105, 111, 0.12);
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            margin-bottom: 0.85rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
            color: #28251d;
        }
        .hero-subtitle {
            font-size: 1rem;
            color: #6f6c64;
            margin: 0;
            max-width: 62ch;
        }
        .section-card {
            background: rgba(251, 251, 249, 0.95);
            border: 1px solid rgba(40, 37, 29, 0.08);
            border-radius: 18px;
            padding: 1rem 1rem 0.75rem 1rem;
            box-shadow: 0 6px 20px rgba(40, 37, 29, 0.05);
            margin-top: 0.75rem;
        }
        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.65rem;
            flex-wrap: wrap;
        }
        .result-title {
            font-size: 1rem;
            font-weight: 700;
            color: #28251d;
            margin: 0;
        }
        .result-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.8rem;
            color: #0c4e54;
            background: rgba(1, 105, 111, 0.08);
            border: 1px solid rgba(1, 105, 111, 0.1);
            border-radius: 999px;
            padding: 0.3rem 0.65rem;
        }
        .stTextArea textarea {
            border-radius: 14px !important;
            border: 1px solid rgba(40, 37, 29, 0.12) !important;
            background: #fffdfa !important;
            color: #28251d !important;
            box-shadow: inset 0 1px 2px rgba(40, 37, 29, 0.03);
            font-size: 0.96rem !important;
            line-height: 1.5 !important;
        }
        .stFileUploader, .stCheckbox, .stExpander {
            background: transparent;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(40, 37, 29, 0.08);
            background: #fbfbf9;
        }
        div.stButton > button, .copy-btn {
            border-radius: 12px !important;
        }
        .footer-note {
            color: #7a7974;
            font-size: 0.84rem;
            margin-top: 0.45rem;
        }
        @media (max-width: 640px) {
            .hero-card { padding: 1rem; border-radius: 16px; }
            .hero-title { font-size: 1.55rem; }
            .section-card { padding: 0.85rem; border-radius: 15px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="ResumoLab", page_icon="📋", layout="centered")

LAB_CONFIGS = {
    "LABORATORIO CRUZEIRO": {
        "nome_resumo": "LAB. CRUZEIRO",
        "titulos_exames": [
            "GLICOSE JEJUM",
            "URINA TIPO I (EAS)",
            "HEMOGRAMA COMPLETO",
            "COLESTEROL TOTAL",
            "HDL - COLESTEROL",
            "LDL - COLESTEROL",
            "VLDL - COLESTEROL",
            "TRIGLICÉRIDES",
            "UREIA ( SORO )",
            "CREATININA ( SORO )",
            "ACIDO URICO SERICO",
            "TGO (AST)",
            "TGP (ALT)",
            "BILIRRUBINAS TOTAL E FRAÇÕES",
            "SÓDIO",
            "POTÁSSIO",
            "VITAMINA B12",
            "VITAMINA D - 25 HIDROXI",
            "TSH - HORMÔNIO TIREOESTIMULANTE",
            "T4- TETRAIODOTIROXINA",
            "HEMOGLOBINA GLICADA",
        ],
    }
}

EXAMES_MAP = OrderedDict([
    ("glicose", {"label": "Glicose jejum", "secao": "Bioquímica", "unidade": "mg/dL"}),
    ("ureia", {"label": "Ureia", "secao": "Bioquímica", "unidade": "mg/dL"}),
    ("creatinina", {"label": "Creatinina", "secao": "Bioquímica", "unidade": "mg/dL"}),
    ("tfge", {"label": "TFGe", "secao": "Bioquímica", "unidade": "mL/min/1,73m²"}),
    ("colesterol_total", {"label": "Colesterol total", "secao": "Lipidograma", "unidade": "mg/dL"}),
    ("hdl", {"label": "HDL", "secao": "Lipidograma", "unidade": "mg/dL"}),
    ("ldl", {"label": "LDL", "secao": "Lipidograma", "unidade": "mg/dL"}),
    ("vldl", {"label": "VLDL", "secao": "Lipidograma", "unidade": "mg/dL"}),
    ("triglicerides", {"label": "Triglicérides", "secao": "Lipidograma", "unidade": "mg/dL"}),
    ("hemacias", {"label": "Hemácias", "secao": "Hemograma", "unidade": "M/mm3"}),
    ("hemoglobina", {"label": "Hemoglobina", "secao": "Hemograma", "unidade": "g/dL"}),
    ("hematocrito", {"label": "Hematócrito", "secao": "Hemograma", "unidade": "%"}),
    ("leucocitos", {"label": "Leucócitos", "secao": "Hemograma", "unidade": ""}),
    ("plaquetas", {"label": "Plaquetas", "secao": "Hemograma", "unidade": ""}),
    ("segmentados_perc", {"label": "Segmentados", "secao": "Hemograma", "unidade": "%"}),
    ("segmentados_abs", {"label": "Segmentados absolutos", "secao": "Hemograma", "unidade": "/mm3"}),
    ("linfocitos_perc", {"label": "Linfócitos típicos", "secao": "Hemograma", "unidade": "%"}),
    ("linfocitos_abs", {"label": "Linfócitos típicos absolutos", "secao": "Hemograma", "unidade": "/mm3"}),
    ("monocitos_perc", {"label": "Monócitos", "secao": "Hemograma", "unidade": "%"}),
    ("monocitos_abs", {"label": "Monócitos absolutos", "secao": "Hemograma", "unidade": "/mm3"}),
    ("eosinofilos_perc", {"label": "Eosinófilos", "secao": "Hemograma", "unidade": "%"}),
    ("eosinofilos_abs", {"label": "Eosinófilos absolutos", "secao": "Hemograma", "unidade": "/mm3"}),
    ("basofilos_perc", {"label": "Basófilos", "secao": "Hemograma", "unidade": "%"}),
    ("basofilos_abs", {"label": "Basófilos absolutos", "secao": "Hemograma", "unidade": "/mm3"}),
    ("acido_urico", {"label": "Ácido úrico", "secao": "Bioquímica", "unidade": "mg/dL"}),
    ("tgo", {"label": "TGO (AST)", "secao": "Função hepática", "unidade": "U/L"}),
    ("tgp", {"label": "TGP (ALT)", "secao": "Função hepática", "unidade": "U/L"}),
    ("bilirrubina_total", {"label": "Bilirrubina total", "secao": "Função hepática", "unidade": "mg/dL"}),
    ("bilirrubina_direta", {"label": "Bilirrubina direta", "secao": "Função hepática", "unidade": "mg/dL"}),
    ("bilirrubina_indireta", {"label": "Bilirrubina indireta", "secao": "Função hepática", "unidade": "mg/dL"}),
    ("sodio", {"label": "Sódio", "secao": "Eletrólitos", "unidade": "mEq/L"}),
    ("potassio", {"label": "Potássio", "secao": "Eletrólitos", "unidade": "mEq/L"}),
    ("vitamina_b12", {"label": "Vitamina B12", "secao": "Vitaminas e hormônios", "unidade": "pg/mL"}),
    ("vitamina_d", {"label": "Vitamina D", "secao": "Vitaminas e hormônios", "unidade": "ng/mL"}),
    ("tsh", {"label": "TSH", "secao": "Vitaminas e hormônios", "unidade": "µUI/mL"}),
    ("t4", {"label": "T4", "secao": "Vitaminas e hormônios", "unidade": "µg/dL"}),
    ("hba1c", {"label": "Hemoglobina glicada (HbA1c)", "secao": "Glicemia", "unidade": "%"}),
    ("glicemia_media", {"label": "Glicemia estimada média", "secao": "Glicemia", "unidade": "mg/dL"}),
])

URINA_MAP = OrderedDict([
    ("cor", "Cor"),
    ("aspecto", "Aspecto"),
    ("densidade", "Densidade"),
    ("ph", "pH"),
    ("proteinas", "Proteínas"),
    ("corpos_cetonicos", "Corpos cetônicos"),
    ("glicose", "Glicose"),
    ("hemoglobina", "Hemoglobina"),
    ("pigmentos_biliares", "Pigmentos biliares"),
    ("urobilinogenio", "Urobilinogênio"),
    ("nitrito", "Nitrito"),
    ("leucocitos", "Leucócitos"),
    ("hemacias", "Hemácias"),
    ("bacterias", "Bactérias"),
    ("cristais", "Cristais"),
    ("celulas_epiteliais", "Células epiteliais"),
    ("filamento_muco", "Filamento de muco"),
    ("leveduras", "Leveduras"),
    ("cilindros", "Cilindros"),
])

IGNORE_VALUES = {"", "NAO ENCONTRADO", "NÃO ENCONTRADO", "NÃO INFORMADO", "NAO INFORMADO", "NONE"}

EXCLUDED_LINE_STARTS = [
    "WWW.", "MATRIZ ", "TATUI", "BOITUVA", "CAPELA DO ALTO", "IPERO", "PORTO FELIZ",
    "PAGINA ", "#ASSINATURA#", "PACIENTE :", "DATA NASC:", "CONVENIO :", "MÉDICO(A):",
    "MEDICO(A):", "O VALOR PREDITIVO", "CONFERIDO:", "LIBERADO POR:",
    "EXAME REALIZADO NO LABORATORIO", "EXAME REALIZADO NO LABORATÓRIO",
]

aplicar_estilo()
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-badge">Resumo clínico automatizado</div>
        <h1 class="hero-title">📋 ResumoLab</h1>
        <p class="hero-subtitle">Envie o PDF do laboratório para identificar os exames, montar um resumo objetivo e facilitar a cópia para o prontuário.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def normalizar_texto(txt: str) -> str:
    if not txt:
        return ""
    txt = txt.replace("\xa0", " ")
    txt = txt.replace("µ", "u").replace("μ", "u")
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n{2,}", "\n", txt)
    return txt.strip()


def remover_acentos(txt: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", txt) if unicodedata.category(c) != "Mn")


def canonical(txt: str) -> str:
    txt = remover_acentos(txt.upper().strip())
    txt = re.sub(r"\s+", " ", txt)
    return txt


def detectar_laboratorio(texto: str) -> str:
    texto_can = canonical(texto)
    for chave in LAB_CONFIGS:
        if chave in texto_can:
            return chave
    return "LABORATORIO CRUZEIRO"


def extrair_texto_pdf(uploaded_file):
    paginas = []
    texto_total = []
    with pdfplumber.open(uploaded_file) as pdf:
        for i, pagina in enumerate(pdf.pages, start=1):
            txt = pagina.extract_text() or ""
            txt = normalizar_texto(txt)
            paginas.append((i, txt))
            texto_total.append(txt)
    return paginas, "\n".join(texto_total)


def linha_util(linha: str) -> bool:
    l = canonical(linha)
    if not l:
        return False
    if set(l.replace(" ", "")) <= {"_", "-", ".", ":", "/"}:
        return False
    return not any(l.startswith(canonical(prefixo)) for prefixo in EXCLUDED_LINE_STARTS)


def extrair_blocos_por_titulos(texto: str, titulos: list[str]) -> dict:
    linhas = [ln.rstrip() for ln in texto.splitlines() if linha_util(ln)]
    linhas_can = [canonical(ln) for ln in linhas]
    titulos_can = {canonical(t): t for t in titulos}

    posicoes = []
    for i, linha in enumerate(linhas_can):
        if linha in titulos_can:
            posicoes.append((i, titulos_can[linha]))

    blocos = {}
    for idx, (inicio, titulo) in enumerate(posicoes):
        fim = posicoes[idx + 1][0] if idx + 1 < len(posicoes) else len(linhas)
        bloco = "\n".join(linhas[inicio:fim]).strip()
        blocos[titulo] = bloco
    return blocos


def buscar_padrao(texto: str, padroes: list[str], flags=re.IGNORECASE):
    for padrao in padroes:
        m = re.search(padrao, texto, flags)
        if m:
            if not m.groups():
                continue
            valor = m.group(1).strip(" .:-")
            if valor:
                return valor
    return None


def limpar_valor(valor: str | None) -> str | None:
    if valor is None:
        return None
    valor = re.sub(r"\s+", " ", valor).strip(" .:-")
    valor_can = canonical(valor)
    if valor_can in IGNORE_VALUES:
        return None
    return valor


def buscar_linha_campo(bloco: str, nome_campo: str) -> str | None:
    linhas = bloco.splitlines()
    campo_can = canonical(nome_campo)
    for linha in linhas:
        linha_can = canonical(linha)
        if campo_can in linha_can:
            if ":" in linha:
                valor = linha.split(":", 1)[1].strip()
            else:
                m = re.search(rf"{re.escape(nome_campo)}\s*[\. ]+(.+)", linha, re.IGNORECASE)
                valor = m.group(1).strip() if m else None
            if valor:
                valor = re.split(r"\s{2,}", valor)[0].strip()
                return limpar_valor(valor)
    return None


def extrair_hemograma_detalhado(bloco: str) -> dict:
    retorno = {}

    def extrair_duplo(nome_base: str, aliases: list[str]):
        for alias in aliases:
            padrao = rf"{alias}\s*[\. :]+([\d,]+)\s*%\s*([\d\.]+)"
            m = re.search(padrao, bloco, re.IGNORECASE)
            if m:
                retorno[f"{nome_base}_perc"] = limpar_valor(m.group(1))
                retorno[f"{nome_base}_abs"] = limpar_valor(m.group(2))
                return

        linha_match = None
        for linha in bloco.splitlines():
            linha_can = canonical(linha)
            if any(canonical(alias) in linha_can for alias in aliases):
                linha_match = linha
                break
        if linha_match:
            nums = re.findall(r"\d+[\d\.,]*", linha_match)
            if len(nums) >= 2:
                retorno[f"{nome_base}_perc"] = limpar_valor(nums[0])
                retorno[f"{nome_base}_abs"] = limpar_valor(nums[1])

    extrair_duplo("segmentados", ["SEGMENTADOS"])
    extrair_duplo("linfocitos", ["LINFÓCITOS TÍPICOS", "LINFOCITOS TIPICOS"])
    extrair_duplo("monocitos", ["MONÓCITOS", "MONOCITOS"])
    extrair_duplo("eosinofilos", ["EOSINÓFILOS", "EOSINOFILOS"])
    extrair_duplo("basofilos", ["BASÓFILOS", "BASOFILOS"])
    return retorno


def extrair_urina(bloco: str) -> dict:
    retorno = {}
    aliases = {
        "Cor": ["Cor"],
        "Aspecto": ["Aspecto"],
        "Densidade": ["Densidade"],
        "pH": ["pH", "PH"],
        "Proteínas": ["Proteínas", "Proteinas"],
        "Corpos cetônicos": ["Corpos Cetônicos", "Corpos Cetonicos"],
        "Glicose": ["GLICOSE", "Glicose"],
        "Hemoglobina": ["Hemoglobina"],
        "Pigmentos biliares": ["Pigmentos Biliares"],
        "Urobilinogênio": ["Urobilinogênio", "Urobilinogenio"],
        "Nitrito": ["Nitrito"],
        "Leucócitos": ["Leucócitos", "Leucocitos"],
        "Hemácias": ["Hemácias", "Hemacias"],
        "Bactérias": ["Bactérias", "Bacterias"],
        "Cristais": ["Cristais"],
        "Células epiteliais": ["Células Epiteliais", "Celulas Epiteliais"],
        "Filamento de muco": ["Filamento de Muco"],
        "Leveduras": ["Leveduras"],
        "Cilindros": ["Cilindros"],
    }
    for chave, label in URINA_MAP.items():
        valor = None
        for alias in aliases[label]:
            valor = buscar_linha_campo(bloco, alias)
            if valor:
                break
        retorno[chave] = valor
    return retorno


def extrair_resultados(blocos: dict) -> dict:
    resultados = {}

    resultados["glicose"] = limpar_valor(buscar_padrao(blocos.get("GLICOSE JEJUM", ""), [r"GLICOSE\s*\(Soro\)\s*[\. :]+([\d,\.]+)"]))
    resultados["ureia"] = limpar_valor(buscar_padrao(blocos.get("UREIA ( SORO )", ""), [r"Ureia\s*[\. :]+([\d,\.]+)", r"Uréia\s*[\. :]+([\d,\.]+)"]))
    resultados["creatinina"] = limpar_valor(buscar_padrao(blocos.get("CREATININA ( SORO )", ""), [r"Resultado:?\s*([\d,\.]+)\s*mg/dL"]))
    resultados["tfge"] = limpar_valor(buscar_padrao(blocos.get("CREATININA ( SORO )", ""), [r"TFGe\).*?([\d,\.]+)\s*ml/min/1,73m", r"estimada\(TFGe\).*?([\d,\.]+)\s*ml/min/1,73m"], flags=re.IGNORECASE | re.DOTALL))
    resultados["colesterol_total"] = limpar_valor(buscar_padrao(blocos.get("COLESTEROL TOTAL", ""), [r"COLESTEROL TOTAL\s*[\. :]+([\d,\.]+)\s*mg/dL"]))
    resultados["hdl"] = limpar_valor(buscar_padrao(blocos.get("HDL - COLESTEROL", ""), [r"COLESTEROL HDL\s*[\. :]+([\d,\.]+)\s*mg/dl"]))
    resultados["ldl"] = limpar_valor(buscar_padrao(blocos.get("LDL - COLESTEROL", ""), [r"COLESTEROL LDL\s*[\. :]+([\d,\.]+)\s*mg/dl"]))
    resultados["vldl"] = limpar_valor(buscar_padrao(blocos.get("VLDL - COLESTEROL", ""), [r"COLESTEROL\s+VLDL\s*[\. :]+([\d,\.]+)\s*mg/dl"]))
    resultados["triglicerides"] = limpar_valor(buscar_padrao(blocos.get("TRIGLICÉRIDES", ""), [r"TRIGLICERIDES\s*[\. :]+([\d,\.]+)\s*mg/dl"]))

    hemograma = blocos.get("HEMOGRAMA COMPLETO", "")
    resultados["hemacias"] = limpar_valor(buscar_padrao(hemograma, [r"HEMÁCIAS\s*[\. :]+([\d,\.]+)\s*M/mm3"]))
    resultados["hemoglobina"] = limpar_valor(buscar_padrao(hemograma, [r"HEMOGLOBINA\s*[\. :]+([\d,\.]+)\s*g/dL"]))
    resultados["hematocrito"] = limpar_valor(buscar_padrao(hemograma, [r"HEMATÓCRITO\s*[\. :]+([\d,\.]+)\s*%"]))
    resultados["leucocitos"] = limpar_valor(buscar_padrao(hemograma, [r"LEUCÓCITOS\s*[\. :]+([\d\.]+)"]))
    resultados["plaquetas"] = limpar_valor(buscar_padrao(hemograma, [r"PLAQUETAS\s*[\. :]+([\d\.]+)"]))
    resultados.update(extrair_hemograma_detalhado(hemograma))

    resultados["acido_urico"] = limpar_valor(buscar_padrao(blocos.get("ACIDO URICO SERICO", ""), [r"ÁCIDO ÚRICO.*?([\d,\.]+)\s*mg/dl", r"ACIDO URICO.*?([\d,\.]+)\s*mg/dl"], flags=re.IGNORECASE | re.DOTALL))
    resultados["tgo"] = limpar_valor(buscar_padrao(blocos.get("TGO (AST)", ""), [r"([\d,\.]+)\s*U/L"]))
    resultados["tgp"] = limpar_valor(buscar_padrao(blocos.get("TGP (ALT)", ""), [r"([\d,\.]+)\s*U/L"]))

    bil = blocos.get("BILIRRUBINAS TOTAL E FRAÇÕES", "")
    resultados["bilirrubina_total"] = limpar_valor(buscar_padrao(bil, [r"BILIRRUBINA TOTAL[\. :]+([\d,\.]+)\s*mg/dL"]))
    resultados["bilirrubina_direta"] = limpar_valor(buscar_padrao(bil, [r"BILIRRUBINA DIRETA[\. :]+([\d,\.]+)\s*mg/dL"]))
    resultados["bilirrubina_indireta"] = limpar_valor(buscar_padrao(bil, [r"BILIRRUBINA INDIRETA[\. :]+([\d,\.]+)\s*mg/dL"]))

    resultados["sodio"] = limpar_valor(buscar_padrao(blocos.get("SÓDIO", ""), [r"([\d,\.]+)\s*mEq/L"], flags=re.IGNORECASE | re.DOTALL))
    resultados["potassio"] = limpar_valor(buscar_padrao(blocos.get("POTÁSSIO", ""), [r"([\d,\.]+)\s*mEq/l"], flags=re.IGNORECASE | re.DOTALL))
    resultados["vitamina_b12"] = limpar_valor(buscar_padrao(blocos.get("VITAMINA B12", ""), [r"Resultado\s*([\d,\.]+)\s*pg/mL"]))
    resultados["vitamina_d"] = limpar_valor(buscar_padrao(blocos.get("VITAMINA D - 25 HIDROXI", ""), [r"Resultado.*?([\d,\.]+)\s*ng/mL", r"\n([\d,\.]+)\s*ng/mL"], flags=re.IGNORECASE | re.DOTALL))
    resultados["tsh"] = limpar_valor(buscar_padrao(blocos.get("TSH - HORMÔNIO TIREOESTIMULANTE", ""), [r"Resultado\s*([\d,\.]+)\s*uUI/mL"]))
    resultados["t4"] = limpar_valor(buscar_padrao(blocos.get("T4- TETRAIODOTIROXINA", ""), [r"Resultado\s*([\d,\.]+)\s*ug/dL"]))

    hba1c_bloco = blocos.get("HEMOGLOBINA GLICADA", "")
    resultados["hba1c"] = limpar_valor(buscar_padrao(hba1c_bloco, [r"Hb A1c:\s*([\d,\.]+)\s*%"]))
    resultados["glicemia_media"] = limpar_valor(buscar_padrao(hba1c_bloco, [r"Glicemia estimada\s*m[eé]dia:\s*([\d,\.]+)\s*mg/dL"], flags=re.IGNORECASE | re.DOTALL))

    return resultados


def montar_resumo(nome_lab: str, resultados: dict, urina: dict) -> str:
    secoes = OrderedDict()
    for chave, meta in EXAMES_MAP.items():
        valor = resultados.get(chave)
        if not valor:
            continue
        secoes.setdefault(meta["secao"], []).append((meta["label"], valor, meta["unidade"]))

    linhas = [f"RESUL. LABS - {nome_lab}"]
    for secao, itens in secoes.items():
        linhas.append(f"\n{secao}:")
        for label, valor, unidade in itens:
            sufixo = f" {unidade}" if unidade else ""
            linhas.append(f"- {label}: {valor}{sufixo}")

    urina_validos = [(label, urina[chave]) for chave, label in URINA_MAP.items() if urina.get(chave)]
    if urina_validos:
        linhas.append("\nEAS:")
        for label, valor in urina_validos:
            linhas.append(f"- {label}: {valor}")

    return "\n".join(linhas)


def montar_debug(blocos: dict, resultados: dict, urina: dict) -> dict:
    exames_detectados = []
    for titulo in blocos:
        exames_detectados.append({
            "exame": titulo,
            "detectado": True,
            "linhas_bloco": len(blocos[titulo].splitlines())
        })

    itens_resultado = []
    for chave, meta in EXAMES_MAP.items():
        valor = resultados.get(chave)
        itens_resultado.append({
            "secao": meta["secao"],
            "campo": meta["label"],
            "status": "Encontrado" if valor else "Não encontrado",
            "valor": valor or "",
        })

    itens_urina = []
    for chave, label in URINA_MAP.items():
        valor = urina.get(chave)
        itens_urina.append({
            "secao": "EAS",
            "campo": label,
            "status": "Encontrado" if valor else "Não encontrado",
            "valor": valor or "",
        })

    return {
        "exames_detectados": exames_detectados,
        "itens_resultado": itens_resultado,
        "itens_urina": itens_urina,
    }


st.markdown('<div class="section-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Escolha o arquivo PDF do exame", type=["pdf"])
mostrar_debug = st.checkbox("Mostrar painel de depuração", value=True)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    with st.spinner("Extraindo dados do PDF..."):
        paginas, texto_completo = extrair_texto_pdf(uploaded_file)
        laboratorio = detectar_laboratorio(texto_completo)
        config_lab = LAB_CONFIGS[laboratorio]
        blocos = extrair_blocos_por_titulos(texto_completo, config_lab["titulos_exames"])
        resultados = extrair_resultados(blocos)
        urina = extrair_urina(blocos.get("URINA TIPO I (EAS)", ""))
        resumo_formatado = montar_resumo(config_lab["nome_resumo"], resultados, urina)
        debug_info = montar_debug(blocos, resultados, urina)

    st.success(f"Extração concluída. Laboratório identificado: {config_lab['nome_resumo']}")
    st.markdown(
        f"""
        <div class="section-card">
            <div class="result-header">
                <p class="result-title">Resultado pronto para o prontuário</p>
                <span class="result-chip">Laboratório: {config_lab['nome_resumo']}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_area("Selecione, copie e cole:", resumo_formatado, height=420)
    st.markdown('<div class="footer-note">Copie o texto abaixo e cole diretamente no prontuário da unidade.</div></div>', unsafe_allow_html=True)

    text_to_copy = (
        resumo_formatado
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("$", "\\$")
    )
    html_code = f'''
    <button onclick="navigator.clipboard.writeText(`{text_to_copy}`)"
            style="padding:10px 16px;border:none;border-radius:8px;background:#0f766e;color:white;cursor:pointer;font-family:Arial,sans-serif;">
        📋 Copiar para o prontuário
    </button>
    '''
    st.components.v1.html(html_code, height=55)

    if mostrar_debug:
        st.subheader("Painel de depuração")
        st.caption("Use esta área para ver quais exames foram detectados e quais campos ainda precisam de ajuste.")
        st.markdown("**Exames detectados no PDF**")
        st.dataframe(debug_info["exames_detectados"], use_container_width=True, hide_index=True)
        st.markdown("**Campos gerais**")
        st.dataframe(debug_info["itens_resultado"], use_container_width=True, hide_index=True)
        st.markdown("**Campos do EAS**")
        st.dataframe(debug_info["itens_urina"], use_container_width=True, hide_index=True)

    with st.expander("Texto bruto extraído do PDF", expanded=False):
        st.text(texto_completo[:30000])
