import re
import unicodedata
from collections import defaultdict
from baseConhecimento import BASE_CONHECIMENTO
from dicionario import (
    SINTOMAS_POR_NUMERO, SINTOMAS_SINONIMOS,
    SINAIS_POR_NUMERO, SINAIS_SINONIMOS,
    LOCAIS_POR_NUMERO, LOCAIS_SINONIMOS,
    IDADE_POR_NUMERO, IDADE_SINONIMOS,
    SEXO_POR_NUMERO, SEXO_SINONIMOS,
    HISTORICO_POR_NUMERO, HISTORICO_SINONIMOS,
    ALERGIA_POR_NUMEROS, ALERGIA_SINONIMOS
)

def normalizar(resposta: str) -> str:
    if not resposta:
        return ""
    resposta = resposta.lower().strip()
    resposta = unicodedata.normalize("NFD", resposta)
    resposta = "".join(ch for ch in resposta if unicodedata.category(ch) != "Mn")  # remove acentos
    return resposta


def compilar_bordas(conjunto_termos: set) -> re.Pattern:
    termos_norm = { normalizar(t) for t in conjunto_termos if t }
    termos_ordenados = sorted((re.escape(t) for t in termos_norm), key=len, reverse=True)
    alternancia = "|".join(termos_ordenados) if termos_ordenados else r"(?!x)x"
    return re.compile(rf"(?<!\w)(?:{alternancia})(?!\w)")


def extrair_por_sinonimos(texto: str, padroes_por_chave: dict) -> set:
    """Retorna o conjunto de chaves no texto."""
    texto_normalizado = normalizar(texto)
    return {chave for chave, padrao in padroes_por_chave.items() if padrao.search(texto_normalizado)}

def _prettify(txt) -> str:
    return str(txt).replace("_", " ").strip()

def formatar_resposta(valor):
    if isinstance(valor, list):
        return ", ".join(_prettify(v) for v in valor)
    elif valor is None:
        return "Não informado"
    else:
        return _prettify(valor)

# ---------- PADRÕES COMPILADOS ----------
PADROES_SINTOMAS = {ch: compilar_bordas(sins) for ch, sins in SINTOMAS_SINONIMOS.items()}
PADROES_SINAIS   = {ch: compilar_bordas(sins) for ch, sins in SINAIS_SINONIMOS.items()}
PADROES_LOCAIS   = {ch: compilar_bordas(sins) for ch, sins in LOCAIS_SINONIMOS.items()}
PADROES_IDADE    = {ch: compilar_bordas(sins) for ch, sins in IDADE_SINONIMOS.items()}
PADROES_SEXO     = {ch: compilar_bordas(sins) for ch, sins in SEXO_SINONIMOS.items()}
PADROES_HIST     = {ch: compilar_bordas(sins) for ch, sins in HISTORICO_SINONIMOS.items()}
PADROES_ALERGIA  = {ch: compilar_bordas(sins) for ch, sins in ALERGIA_SINONIMOS.items()}


def interpretar_sintomas(resposta_usuario: str) -> set:

    # Retorna um conjunto com as chaves dos sintomas. Nunca retorna números
    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    sintomas_detectados = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = SINTOMAS_POR_NUMERO.get(numero)
        if chave:
            sintomas_detectados.add(chave)

    # Busca sinônimos no texto livre
    sintomas_detectados |= extrair_por_sinonimos(resposta_usuario, PADROES_SINTOMAS)

    return sintomas_detectados

def interpretar_sinais(resposta_usuario: str) -> set:

    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    sinais_detectados = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = SINAIS_POR_NUMERO.get(numero)
        if chave:
            sinais_detectados.add(chave)

    # Busca sinônimos no texto livre
    sinais_detectados |= extrair_por_sinonimos(resposta_usuario, PADROES_SINAIS)

    return sinais_detectados

def interpretar_locais(resposta_usuario: str) -> set:

    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    locais_detectados = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = LOCAIS_POR_NUMERO.get(numero)
        if chave:
            locais_detectados.add(chave)

    # Busca sinônimos no texto livre
    locais_detectados |= extrair_por_sinonimos(resposta_usuario, PADROES_LOCAIS)

    return locais_detectados


def interpretar_idade(resposta_usuario: str) -> set:

    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    idade_detectada = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = IDADE_POR_NUMERO.get(numero)
        if chave:
            idade_detectada.add(chave)

    # Busca sinônimos no texto livre
    idade_detectada |= extrair_por_sinonimos(resposta_usuario, PADROES_IDADE)

    return idade_detectada

def interpretar_sexo(resposta_usuario: str) -> set:

    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    sexo_detectado = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = SEXO_POR_NUMERO.get(numero)
        if chave:
            sexo_detectado.add(chave)

    # Busca sinônimos no texto livre
    sexo_detectado |= extrair_por_sinonimos(resposta_usuario, PADROES_SEXO)

    return sexo_detectado

def interpretar_historico(resposta_usuario: str) -> set:

    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    historico_detectado = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = HISTORICO_POR_NUMERO.get(numero)
        if chave:
            historico_detectado.add(chave)

    # Busca sinônimos no texto livre
    historico_detectado |= extrair_por_sinonimos(resposta_usuario, PADROES_HIST)

    return historico_detectado

def interpretar_alergia(resposta_usuario: str) -> set:

    if not resposta_usuario or not resposta_usuario.strip():
        return set()

    alergia_detectada = set()

    busca_numeros_resposta = re.findall(r"\b\d{1,3}\b", resposta_usuario)
    
    for numero in busca_numeros_resposta:
        chave = ALERGIA_POR_NUMEROS.get(numero)
        if chave:
            alergia_detectada.add(chave)

    # Busca sinônimos no texto livre
    alergia_detectada |= extrair_por_sinonimos(resposta_usuario, PADROES_ALERGIA)

    return alergia_detectada

def tem_termo(resposta, conjunto_termos: set) -> bool:
    # Aceita list/tuple/set/str/None como resposta; normaliza e busca termos com bordas
    if resposta is None:
        return False
    # Formata: ["ardor","vermelhidao"] -> "ardor vermelhidao"
    if isinstance(resposta, (list, tuple, set)):
        resposta = " ".join(map(str, resposta))
    resposta = str(resposta)
    if not resposta.strip():
        return False
    texto_normalizado = normalizar(resposta)
    for termo in conjunto_termos:
        padrao_com_bordas = rf"(?<!\w){re.escape(termo)}(?!\w)"
        if re.search(padrao_com_bordas, texto_normalizado):
            return True
    return False

def evidencia_sintomas(resposta: str, chave_vocab: str) -> bool:
    termos = SINTOMAS_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def evidencia_sinais(resposta: str, chave_vocab: str) -> bool:
    termos = SINAIS_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def evidencia_locais(resposta: str, chave_vocab: str) -> bool:
    termos = LOCAIS_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def evidencia_idade(resposta: str, chave_vocab: str) -> bool:
    termos = IDADE_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def evidencia_sexo(resposta: str, chave_vocab: str) -> bool:
    termos = SEXO_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def evidencia_historico(resposta: str, chave_vocab: str) -> bool:
    termos = HISTORICO_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def evidencia_alergia(resposta: str, chave_vocab: str) -> bool:
    termos = ALERGIA_SINONIMOS.get(chave_vocab, {chave_vocab})
    return tem_termo(resposta, termos)

def _coagir_para_texto(resposta_txt) -> str:
    #Aceita list/tuple/set/str/None e devolve string normalizada para busca
    if resposta_txt is None:
        return ""
    if isinstance(resposta_txt, (list, tuple, set)):
        # Junta termos com espaço: ["ardor","vermelhidao"] -> "ardor vermelhidao"
        return " ".join(map(str, resposta_txt))
    return str(resposta_txt)

def pontuar_eixo(resposta_txt: str, eixo: str, pesos_eixo: dict) -> int:
    score = 0
    r = normalizar(_coagir_para_texto(resposta_txt))
    for chave_vocab, peso in pesos_eixo.items():
        if (
            evidencia_sintomas(r, chave_vocab) or
            evidencia_sinais(r, chave_vocab) or
            evidencia_locais(r, chave_vocab) or
            evidencia_idade(r, chave_vocab) or
            evidencia_sexo(r, chave_vocab) or
            evidencia_historico(r, chave_vocab) or
            evidencia_alergia(r, chave_vocab)
        ):
            score += peso
    return score

def classificar(respostas: dict):
    r = {k: (v or "") for k, v in (respostas or {}).items()}

    scores = defaultdict(int)
    matches = {doenca: [] for doenca in BASE_CONHECIMENTO.keys()}

    for doenca, eixos in BASE_CONHECIMENTO.items():
        pontos_sintomas  = pontuar_eixo(r.get("sintomas"),           "sintomas", eixos.get("sintomas", {}))
        pontos_sinais    = pontuar_eixo(r.get("sinais_clinicos"),    "sinais",   eixos.get("sinais", {}))
        pontos_locais    = pontuar_eixo(r.get("localizacao_tipica"), "local",    eixos.get("local", {}))
        pontos_idade     = pontuar_eixo(r.get("idade"),              "idade",    eixos.get("idade", {}))
        pontos_sexo      = pontuar_eixo(r.get("sexo"),               "sexo",     eixos.get("sexo", {}))
        pontos_historico = pontuar_eixo(r.get("historico_relevante"),"historico",eixos.get("historico", {}))
        pontos_alergia   = pontuar_eixo(r.get("alergia_medicamentosa"),"alergia",eixos.get("alergia", {}))

        scores[doenca] += (pontos_sintomas + pontos_sinais + pontos_locais +
                           pontos_idade + pontos_sexo + pontos_historico + pontos_alergia)

        # exemplos de matches detalhados (mantidos)
        for chave_vocab, peso in eixos.get("sintomas", {}).items():
            if evidencia_sintomas(r.get("sintomas"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"sintomas:{chave_vocab}(+{peso})")
        
        for chave_vocab, peso in eixos.get("sinais", {}).items():
            if evidencia_sinais(r.get("sinais_clinicos"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"sinais:{chave_vocab}(+{peso})")

        for chave_vocab, peso in eixos.get("local", {}).items():
            if evidencia_locais(r.get("localizacao_tipica"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"local:{chave_vocab}(+{peso})")
        
        for chave_vocab, peso in eixos.get("idade", {}).items():
            if evidencia_idade(r.get("idade"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"idade:{chave_vocab}(+{peso})")

        for chave_vocab, peso in eixos.get("sexo", {}).items():
            if evidencia_sexo(r.get("sexo"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"sexo:{chave_vocab}(+{peso})")

        for chave_vocab, peso in eixos.get("historico", {}).items():
            if evidencia_historico(r.get("historico_relevante"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"historico:{chave_vocab}(+{peso})")

        for chave_vocab, peso in eixos.get("alergia", {}).items():
            if evidencia_alergia(r.get("alergia_medicamentosa"), chave_vocab):
                scores[doenca] += peso
                matches[doenca].append(f"alergia:{chave_vocab}(+{peso})")

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    if not ranked:
        return {"diagnostico": None, "scores": {}, "matches": {}}

    top_doenca, top_score = ranked[0]
    total = sum(max(s, 0) for _, s in ranked)
    conf = round((top_score / total), 2) if total > 0 else 0.0

    return {
        "diagnostico": top_doenca if top_score >= 3 else None,
        "confianca": conf,
        "scores": dict(ranked),
        "matches": matches
    }
