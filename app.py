import re
import unicodedata
from collections import OrderedDict

import pdfplumber
import streamlit as st


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


IGNORE_VALUES = {
    "",
    "NAO ENCONTRADO",
    "NÃO ENCONTRADO",
    "NÃO INFORMADO",
    "NAO INFORMADO",
    "NONE",
}


EXCLUDED_LINE_STARTS = [
    "WWW.", "MATRIZ ", "TATUI", "BOITUVA", "CAPELA DO ALTO", "IPERO", "PORTO FELIZ",
    "PAGINA ", "#ASSINATURA#", "PACIENTE :", "DATA NASC:", "CONVENIO :", "MÉDICO(A):",
    "MEDICO(A):", "O VALOR PREDITIVO", "CONFERIDO:", "LIBERADO POR:",
    "EXAME REALIZADO NO LABORATORIO", "EXAME REALIZADO NO LABORATÓRIO",
]


st.title("📋 ResumoLab")
st.write("Faça o upload do PDF do laboratório para extrair os resultados e gerar um texto pronto para o prontuário.")


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
                valor = re.sub(r"\b(Negativo|Normal|Ausentes?|Limpido|Límpido|Amarelo citrina)\b.*$", lambda x: x.group(1), valor, flags=re.IGNORECASE) if len(valor.split()) > 3 else valor
                return limpar_valor(valor)
    return None


def extrair_hemograma_detalhado(bloco: str) -> dict:
    retorno = {}

    def extrair_duplo(nome_base, chaves):
        for nome in chaves:
            padroes = [
                rf"{nome}\s*[\. :]+([\d,]+)\s*%\s*([\d\.]+)",
                rf"{nome}\s*[\. :]+([\d,]+)\s*%\s*([\d\.,]+)",
            ]
            for padrao in padroes:
                m = re.search(padrao, bloco, re.IGNORECASE)
                if m:
                    retorno[f"{nome_base}_perc"] = limpar_valor(m.group(1))
                    retorno[f"{nome_base}_abs"] = limpar_valor(m.group(2))
                    return

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
        linhas = len(blocos[titulo].splitlines())
        exames_detectados.append({"exame": titulo, "detectado": True, "linhas_bloco": linhas})

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


uploaded_file = st.file_uploader("Escolha o arquivo PDF do exame", type=["pdf"])
mostrar_debug = st.checkbox("Mostrar painel de depuração", value=True)
mostrar_blocos = st.checkbox("Mostrar blocos brutos dos exames", value=False)

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
    st.subheader("Resultado pronto para o prontuário")
    st.text_area("Selecione, copie e cole:", resumo_formatado, height=420)

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

    if mostrar_blocos:
        st.subheader("Blocos brutos detectados")
        for titulo, bloco in blocos.items():
            with st.expander(titulo, expanded=False):
                st.code(bloco)

    with st.expander("Texto bruto extraído do PDF", expanded=False):
        st.text(texto_completo[:30000])
