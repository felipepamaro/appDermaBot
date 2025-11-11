
from typing import Dict, Any, Set, Iterable
import unicodedata

def _normalizacao(texto: str) -> str:
    if texto is None:
        return ""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def _lematizacao(tok: str) -> str:
    t = tok
    if t.endswith("oes"): t = t[:-3] + "ao"
    elif t.endswith("aes"): t = t[:-3] + "ao"
    elif t.endswith("res"): t = t[:-2]
    elif t.endswith("is") and len(t) > 3: t = t[:-1]
    elif t.endswith("es") and len(t) > 3: t = t[:-2]
    elif t.endswith("s") and len(t) > 3: t = t[:-1]
    if t.endswith("ando") or t.endswith("endo") or t.endswith("indo"): t = t[:-4]
    return t

def _tok(texto: str) -> Set[str]:
    t = _normalizacao(texto)
    for ch in ",.;:!?()/\\[]{}\"'|+-_@#$%^&*<>=~":
        t = t.replace(ch, " ")
    return { _lematizacao(w) for w in t.split() if w }


def _distancia_levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    dp = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        prev, dp[0] = dp[0], i
        for j, cb in enumerate(b, 1):
            cur = prev if ca == cb else prev + 1
            cur = min(cur, dp[j] + 1, dp[j-1] + 1)
            prev, dp[j] = dp[j], cur
    return dp[-1]

def _correspondencia(tokens: Set[str], candidatos: Iterable[str], max_lev: int = 1) -> bool:
    for cand in candidatos:
        c = _lematizacao(_normalizacao(cand))
        if c in tokens: 
            return True
        thr = max_lev + (1 if len(c) >= 7 else 0)
        if any(_distancia_levenshtein(tok, c) <= thr for tok in tokens):
            return True
    return False

# -------------------------
# Vocabulários
# -------------------------
SINONIMOS = {
    # PLACA
    "placa": {"placa","placas","placoide","placoides", "palca","palcas"},
    "circinada": {"circinada", "circinadas", "anel", "anelar", "circular", "redonda", "arredondada"},
    "liquenificada": {"liquenificada","liquenificadas","espessa","espessas","espessadas"},
    "eritemato": {"eritemato", "eritematosa", "eritematoso"},
    "descamativa": {"descamativa","descamativas","descamacao","descamar","escama","escamosa","escamosas","escamoso","escamosos","escamosa"},
    "bem_definida": {"bem","definida","delimitada","delimitadas","bemdelimitada","bem-delimitada", "bem definida", "definidas"},
    "placa_mae": {"placa-mae","placa_mae","herald","oval", "mae"},
    "erupcao": {"erupção", "erupçao", "erupcao", "erupcão", "erupções","erupcoes","erpçoes","erupcões","secundária","secundaria","secundárias","secundarias","em tronco"},

    # LESÃO
    "lesao": {"lesao", "lesão", "lesões", "lesoes","eritemato-descamativa", "eritemato","descamativa"},
    "caracteristica_lesao_seca": {"seca","secas","esfoliativa","esfoliativas","ressecada","ressecadas","ressecado","ressecados"},
    "caracteristica_lesao_alvo": {"alvo","vesículas","vesiculas","vesícula","vesicula","bolha","bolhas"},
    "local_lesao_disseminada": {"disseminada","disseminadas","disseminado","disseminados","generalizada","generalizadas","generalizado","generalizados","corpo","lugar","espalhada","todo","lugares","todos"},

    # VESÍCULA
    "vesicula": {"vesicula","vesículas","vesicular","bolha","bolhas","ampola","pústula","pustula","vesico","flictena","vesícula"},
    "vesicula_disseminada": {"disseminada","disseminadas","disseminado","disseminados","generalizada","generalizadas","generalizado","generalizados","corpo","lugar","espalhada","todo","lugares","todos"},
    "sintomas_sistemicos": {"febre","febril","mal-estar","indisposicao","cansaco","fadiga","astenia",
                            "cabeça","cefaleia","cefaleia","apetite","anorexia",
                            "malestar","mauestar"},
    "ardor": {"ardor","queima","queimacao","queimação","dolorido","dor","ardente"},
    "crianca": {"crianca","criança","pediatrico","pediátrico","menino","menina"},
    "adulto": {"adulto","adulta","maior de idade"},
    "exantema_disseminado": {"manchas","manchas avermelhadas","exantema","corpo todo","pelo corpo","generalizado","difuso"},
    "genitais": {"genital","genitais","pênis","penis","vulva","vagina","escroto","perianal","pubiana"},
    "boca": {"boca","labio","lábio","lábios","labios","oral","cavidade oral","intraoral"},
    "catapora_ou_imunossup": {
        "catapora","varicela","já teve varicela","teve catapora","imunossuprimido","imunossupressa",
        "imunossupressao","quimioterapia","quimioterápico","corticoide","corticosteroide","hiv","transplante"
    },
    
    # sintomas
    "prurido": {"prurido","coceira","comichao","pruriginoso","pruriginosa", "coça", "coca", "coçando", "cocando"},
    "sintoma_dermatite_contato": {"ardor","ador","queimação","queimaçao","queimacão","queima","arde","ardência","ardido","ardia"},
    
    # histórico placas
    "umidade": {"umido","umida","umidade","suor","suorento","suado"},
    "oclusao": {"sapato","tenis","bota","fechado","apertada","apertado","meia","roupa"},
    "diabetes": {"diabete","diabetes","glicemia","glicemico","glicêmico"},
    "viral": {"virose","resfriado","grip","infec","vias"},
    "estresse": {"estresse","stress","ansiedade","ansioso","ansiosa"},
    "atopia": {"atopia","atopico","atopica","atópico","atópica"},
    "dermatite": {"dermatite","eczema"},
    "picada": {"picada","picadas","inseto","mosquito","pulga"},

    # histórico dermatite
    "historico_dermatite_seborreica": {"estresse","stress","stres","hiv","aids","familiar","família","familia","genético","genetico","genética","genetica"},
    "historico_dermatite_contato": {"produto","produtos","irritante","irritantes","agente","agentes","perfume","perfumes","detergente","detergentes","cosméticos","cosmético","cosmetico","cosméticos","maquiagem"},
    "historico_dermatite_atopica": {"atopia","asma","rinite","bronquite"},


    # tipo pele dermatite
    "pele_oleosa": {"oleosa","oleoso","sebosa","seboso","oleosas","oleosos","sebo"},
    "pele_seca": {"seca","ressecada","seco","ressecado","ressecadas","ressecados"},
    
    # locais
    "pes": {"pe","pes","pé","pés","planta","plantar","calcanhar","dedo","dedos"},
    "virilha_dobras": {"virilha","ingle","inguinal","axila","axilas","inframamaria","submamaria","dobras","pregas", "dobra"},
    "tronco": {"tronco","dorso","costas","peito","torax","tórax","abdomen","barriga","flanco"},
    "areas_liquen": {"nuca","sacra", "genitais","genital", "membro", "membros", "bacia"},
    "areas_psoriase": {"couro","cabeludo","cabeça","cabeca","orelha","orelhas","cotovelo","cotovelos","joelho","joelhos","lombar","unha","unhas"},
    "local_dermatite_seborreica": {"couro","cabeludo","cabeça","cabeca"},
    "local_dermatite_contato": {"próximas","proximas","próxima","proxima","perto","mesma área","mesma area","mesmo local","mesmo lugar","próximo","proximo"}
}

# ---------------------------------------------
# Mapeamentos de múltipla escolha (ramificação)
# ---------------------------------------------
OPCOES: Dict[str, Dict[str, Set[str]]] = {
    "tipo_lesao_inicial": {
        "A": SINONIMOS["placa"],
        "B": SINONIMOS["lesao"],
        "C": SINONIMOS["vesicula"]
    }
}


NEGACAO = {"nao","nem","sem","ausencia","negativo","negativa","nunca","nenhum","nenhuma","nada","naoooo","n"}
AFIRMACAO = {"sim","s","claro","ok","yes","y","positivo","positiva","bora","vamos","quero","iniciar","começar","comecar"}

def _tem_negacao(texto: str) -> bool:
    return any(t in NEGACAO for t in _tok(texto))
def _tem_afirmacao(texto: str) -> bool:
    return any(t in AFIRMACAO for t in _tok(texto))

def _binarizacao(texto: str) -> str:
    texto = _normalizacao(texto)
    if texto in {"1","sim","s","y","yes"}:
        return "1"
    if texto in {"2","nao","não","n","no"}:
        return "2"
    return texto

# -------------------------
# Classificação multiopção
# -------------------------
def _classificar_opcao(caracteristica: str, tokens: Set[str]) -> str:
    mapa = OPCOES.get(caracteristica)
    if not mapa:
        return ""
    pontuacao = {}
    for chave, pistas in mapa.items():
        hits = 0
        for p in pistas:
            pnorm = _lematizacao(_normalizacao(p))
            if pnorm in tokens:
                hits += 2
            elif any(_distancia_levenshtein(t, pnorm) <= (2 if len(pnorm) >= 7 else 1) for t in tokens):
                hits += 1
        pontuacao[chave] = hits
    chave, melhor = max(pontuacao.items(), key=lambda kv: kv[1])
    return chave if melhor > 0 else ""

# -------------------------
# Mapeamento de respostas (binário + pistas)
# -------------------------
def _mesmo_topico(pergunta: str, resposta: str) -> bool:
    tq, tr = _tok(pergunta), _tok(resposta)
    stop = {"a","o","os","as","um","uma","de","do","da","dos","das","no","na","nos","nas","em","para","por","com","sem","e","ou","que","se","sao","sera","ha","tem","houve"}
    core = {t for t in tq if t not in stop and len(t) > 2}
    return len(core.intersection(tr)) >= 1 if core else False

def _mapear_resposta(caracteristica: str, pergunta_txt: str, entrada_txt: str) -> str:
    tokens = _tok(entrada_txt)

    # Multiopção (apenas o nó inicial)
    if caracteristica in OPCOES:
        chave = _classificar_opcao(caracteristica, tokens)
        if chave:
            return chave

    # Nós binários
    pistas = []
    if caracteristica == "caracteristica_micose":
        pistas = list(SINONIMOS["circinada"])
    elif caracteristica == "local_micose":
        pistas = list(SINONIMOS["pes"] | SINONIMOS["virilha_dobras"] | SINONIMOS["tronco"])
    elif caracteristica == "tem_prurido_micose":
        pistas = list(SINONIMOS["prurido"])
    elif caracteristica == "historico_umidade_micose":
        pistas = list(SINONIMOS["umidade"] | SINONIMOS["oclusao"])
    elif caracteristica == "historico_diabetes_micose":
        pistas = list(SINONIMOS["diabetes"])
    elif caracteristica == "caracteristica_liquen":
        pistas = list(SINONIMOS["liquenificada"])
    elif caracteristica == "local_liquen":
        pistas = list(SINONIMOS["areas_liquen"])
    elif caracteristica == "tem_prurido_liquen":
        pistas = list(SINONIMOS["prurido"])
    elif caracteristica == "historico_liquen":
        pistas = list(SINONIMOS["estresse"] | SINONIMOS["atopia"] | SINONIMOS["dermatite"] | SINONIMOS["picada"])
    elif caracteristica == "caracteristica_psoriase":
        pistas = list(SINONIMOS["eritemato"] | SINONIMOS["descamativa"] | SINONIMOS["bem_definida"])
    elif caracteristica == "local_psoriase":
        pistas = list(SINONIMOS["areas_psoriase"])
    elif caracteristica == "tem_prurido_psoriase":
        pistas = list(SINONIMOS["prurido"])
    elif caracteristica == "historico_psoriase":
        pistas = list(SINONIMOS["estresse"])
    elif caracteristica == "caracteristica_pitiriase_rosea":
        pistas = list(SINONIMOS["eritemato"] | SINONIMOS["descamativa"] | SINONIMOS["erupcao"] | SINONIMOS["placa_mae"])
    elif caracteristica == "infeccao_viral_pitiriase":
        pistas = list(SINONIMOS["viral"])
    elif caracteristica == "local_pitiriase":
        pistas = list(SINONIMOS["tronco"])
    elif caracteristica == "tem_prurido_pitiriase":
        pistas = list(SINONIMOS["prurido"])
    elif caracteristica == "local_lesao_disseminada":
        pistas = list(SINONIMOS["local_lesao_disseminada"])
    elif caracteristica == "caracteristica_lesao_seca":
        pistas = list(SINONIMOS["caracteristica_lesao_seca"])
    elif caracteristica == "caracteristica_lesao_alvo":
        pistas = list(SINONIMOS["caracteristica_lesao_alvo"])
    elif caracteristica == "tipo_pele_dermatite_oleosa":
        pistas = list(SINONIMOS["pele_oleosa"])
    elif caracteristica == "tipo_pele_dermatite_seca":
        pistas = list(SINONIMOS["pele_seca"])
    elif caracteristica == "historico_dermatite_seborreica":
        pistas = list(SINONIMOS["historico_dermatite_seborreica"])
    elif caracteristica == "local_dermatite_seborreica":
        pistas = list(SINONIMOS["local_dermatite_seborreica"])
    elif caracteristica == "historico_dermatite_contato":
        pistas = list(SINONIMOS["historico_dermatite_contato"])
    elif caracteristica == "local_dermatite_contato":
        pistas = list(SINONIMOS["local_dermatite_contato"])
    elif caracteristica == "historico_dermatite_atopica":
        pistas = list(SINONIMOS["historico_dermatite_atopica"])
    elif caracteristica == "sintoma_dermatite_contato":
        pistas = list(SINONIMOS["sintoma_dermatite_contato"])
    elif caracteristica == "lesoes_vesiculares_disseminadas":
        pistas = list(SINONIMOS["vesicula_disseminada"])
    elif caracteristica == "sintomas_sistemicos_varicela":
        pistas = list(SINONIMOS["sintomas_sistemicos"])
    elif caracteristica == "prurido_local":
        pistas = list(SINONIMOS["prurido"] | SINONIMOS.get("ardor", set()))
    elif caracteristica == "eh_crianca":
        pistas = list(SINONIMOS["crianca"])
    elif caracteristica == "eh_adulto":
        pistas = list(SINONIMOS["adulto"])
    elif caracteristica == "manchas_avermelhadas_disseminadas":
        pistas = list(SINONIMOS["exantema_disseminado"])
    elif caracteristica == "local_genitais":
        pistas = list(SINONIMOS["genitais"])
    elif caracteristica == "local_boca":
        pistas = list(SINONIMOS["boca"])
    elif caracteristica == "historico_catapora_ou_imunossup":
        pistas = list(SINONIMOS["catapora_ou_imunossup"])

    # Decisão: negação → "2"; presença de pistas → "1"
    if _tem_negacao(entrada_txt):
        return "2"
    if _correspondencia(tokens, pistas):
        return "1"

    if _tem_afirmacao(entrada_txt):
        return "1"
    # if _mesmo_topico(pergunta_txt, entrada_txt):
        #return "1"
    return _normalizacao(entrada_txt)

# -------------------------
# API
# -------------------------
def registrar_resposta(sessao: Dict[str, Any], valor_digitado: str):
    if not sessao.get("pergunta_atual"):
        return
    caract = sessao["pergunta_atual"]
    pergunta = sessao.get("texto_pergunta_atual","")

    v = _binarizacao(valor_digitado)
    if v not in {"1","2"} or caract in OPCOES:
        v = _mapear_resposta(caract, pergunta, valor_digitado)
    if v not in {"1","2"} and caract not in OPCOES:
        v = _mapear_resposta(caract, pergunta, valor_digitado)

    respostas = sessao.setdefault("respostas", {})
    respostas[caract] = v
    sessao["pergunta_atual"] = None
    sessao["texto_pergunta_atual"] = None

def proxima_etapa(no: Dict[str, Any], respostas: Dict[str, str]) -> Dict[str, Any]:
    if "folha" in no:
        return {"folha": no["folha"]}
    caract = no["caracteristica"]
    if caract not in respostas:
        return {"perguntar": {"caracteristica": caract, "texto": no["pergunta"]}}
    valor = respostas.get(caract)
    prox = no.get("ramos", {}).get(valor)
    if not prox:
        mensagem_erro = "Desculpe, mas não entendi sua resposta. Poderia reformular?"
        texto_refazer = f"{mensagem_erro}\n\n{no['pergunta']}"
        return {"perguntar": {"caracteristica": caract, "texto": texto_refazer}}
    return proxima_etapa(prox, respostas)


def reiniciar_sessao() -> Dict[str, Any]:
    return {"etapa": "arvore", "respostas": {}, "pergunta_atual": None, "texto_pergunta_atual": None}
