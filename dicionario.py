SINTOMAS_POR_NUMERO = {
    "1": "prurido",
    "2": "ardor",
    "3": "dor",
    "4": "formigamento",
    "5": "sensibilidade",
    "6": "dormencia",
    "7": "assintomatico"
}

SINTOMAS_SINONIMOS = {
    "prurido": {"prurido", "coceira", "coçando", "coçar", "purido", "plurido", "coça", "prurid"},
    "ardor": {"ardor", "queimaçao", "queimacao", "queimação", "queima", "ardencia", "arde", "ardido", "ardendo", "queimando"},
    "dor": {"dor", "doi", "dói", "doido", "doendo"},
    "formigamento": {"formigamento", "formiga", "parestesia", "parestezia"},
    "sensibilidade": {"perda de sensibilidade", "perda sensibilidade", "falta de sensibilidade"},
    "dormencia": {"dormencia", "dormência"},
    "assintomatico": {"assintomatico", "assintomático", "sem sintomas", "sem sintoma", "nao tem sintoma"}
}

SINAIS_POR_NUMERO = {
    "1": "eritema",
    "2": "edema",
    "3": "vesicula",
    "4": "bolhas",
    "5": "fissura",
    "6": "ressecamento",
    "7": "descamacao",
    "8": "placas_eritematosas",
    "9": "bordas_circinadas",
    "10": "escamas",
    "11": "ulcera",
    "12": "macula",
    "13": "dermatite",
    "14": "placa_liquenificada",
    "15": "sulcos",
    "16": "hiperpigmentacao",
    "17": "bordas_definidas",
    "18": "placa_mae",
    "19": "erupcoes_tronco",
    "20": "erupcao_eritemato_descamativa",
    "21": "lesoes_alvo",
    "22": "nodulo"
}

SINAIS_SINONIMOS = {
    "eritema": {"eritema", "lesoes eritematosas", "lesões eritematosas","lesão eritematosa", "lesão eritematosa",
                "vermelhidao", "vermelho", "avermelhado", "avermelhada", "lesao avermelhada", "lesoes avermelhadas"},
    "edema": {"edema", "edemas"},
    "vesicula": {"vesicula", "vesícula", "vesículas", "vesiculas", "vezicula", "veziculas", "vasicula", "vasiculas"},
    "bolhas": {"bolhas", "bolha", "bola", "bolas", "bolhos"},
    "fissura": {"fissura", "fissuras", "fiçura", "fiçuras", "rachadura", "rachaduras", "rachado", "rachada", "fenda"},
    "ressecamento": {"ressecamento", "seco", "ressecada", "ressecado", "seca", "rececado", "rececada"},
    "descamacao": {"descamacao", "descamação", "descamar", "descamativa", "descamado", "descamada", "descamando"},
    "placas_eritematosas": {"placas eritematosas", "placa eritematosa"},
    "bordas_circinadas": {"bordas circinadas", "borda circinada", "borda redonda", "borda arredondada"},
    "escamas": {"escamas", "escama", "escamas finas", "escama fina", "escamosa"},
    "ulcera": {"ulcera", "úlcera", "úlceras", "úlcura indolor", "úlceras indolores", "ulcera indolor",
               "ulceras", "ulceras indolores", "cancro", "cancro duro"},
    "macula": {"macula", "mácula", "máculas", "maculas", "máculas hipocrômicas ou eritematosas" ,"maculas hipocromicas ou eritematosas",
               "máculas hipocrômicas", "maculas hipocromicas", "máculas eritematosas", "maculas eritematosas"},
    "dermatite": {"dermatite", "dermatite ocre", "dermatite marrom"},
    "placa_liquenificada": {"placa liquenificada", "placas liquenificadas"},
    "sulcos": {"sulcos", "sulco", "acentuacao dos sulcos", "sulcos acentuados", "sulco acentuado"},
    "hiperpigmentacao": {"hiperpigmentaçao", "hiperpigmentação", "hiperpigmentacao", "hiperpigmentos"},
    "bordas_definidas": {"bordas definidas", "borda definida", "bordas bem definidas", "borda bem definida"},
    "placa_mae": {"placa-mae", "placa-mãe", "placa mãe", "placa mae", "placas-mae", "placas-mãe",
                  "placas mae", "placas mãe", "palcas mae"},
    "erupcoes_tronco": {"erupçoes tronco", "erupções tronco", "erupções secundárias em tronco", "erupçoes secundarias em tronco",
                        "erupçao em tronco", "erupção em tronco", "erupçoes em tronco", "erupções em tronco"},
    "erupcao_eritemato_descamativa": {"erupçao eritemato-descamativa", "erupção eritemato-descamativa", "erupcao eritemato-descamativa",
                                      "erupção descamativa", "erupçao descamativa", "erupcao descamativa"},
    "lesoes_alvo": {"lesões em alvo", "lesoes em alvo", "lesoes eritematosas em alvo", "lesao em alvo", "lesão em alvo",
                    "lesao eritematosa em alvo"},
    "nodulo": {"nodulo", "nódulo", "nódulos", "nodulos", "nodulo avermelhado", "nodulos avermelhados", "nodulo firme",
               "nodulos avermelhados e firmes", "nodulo vermelho", "nodulos vermelhos"}
 }


LOCAIS_POR_NUMERO = {
    "1": "disseminado",
    "2": "palmo_plantar",
    "3": "couro",
    "4": "unha",
    "5": "tronco",
    "6": "dobras",
    "7": "labios",
    "8": "genitais",
    "9": "face",
    "10": "flexoras",
    "11": "membros",
    "12": "nuca",
    "13": "sacra"
}

LOCAIS_SINONIMOS = {
    "disseminado": {"disseminado", "corpo todo", "todo lugar", "espalhado"},
    "palmo_plantar": {"regiao palmo plantar", "regiao palmo-plantar", "palmo-plantar", "palmo plantar"},
    "couro": {"couro cabeludo", "cabeça", "cabeca"},
    "unha": {"unha", "unhas"},
    "tronco": {"tronco", "troncos", "abdomen", "costas"},
    "dobras": {"dobras", "dobra", "virilha", "virilia", "dobras (virilha)", "dobra (virilha)", "virilhas", "virilias"},
    "labios": {"labios", "labio", "boca", "beiços", "beiço", "beico", "beicos"},
    "genitais": {"genitais", "genitalia", "penis", "vagina"},
    "face": {"face", "rosto", "testa", "bochecha", "bochechas", "cara", "nariz"},
    "flexoras": {"flexoras", "areas flexoras", "cotovelo", "cotovelos", "joelho", "joelhos", "cotovelos e joelhos",
                 "areas flexoras (cotovelos e joelhos)"},
    "membros": {"membros", "membros inferiores", "membros superiores", "membro", "membros inferiores e/ou superiores",
                "memebros inferiores e superiores", "membros superiores e inferiores"},
    "nuca": {"nuca", "nunca"},
    "sacra": {"sacra", "regiao sacra", "bacia"}
}

IDADE_POR_NUMERO = {
    "1": "bebe",
    "2": "crianca",
    "3": "adolescente",
    "4": "adulto_jovem",
    "5": "adulto",
    "6": "idoso"
}
    
IDADE_SINONIMOS = {
    "bebe": {"bebe", "nenem", "bebezinho", "recem nascido", "recem-nascido", "nene", "bb", "1 ano", "2 anos"},
    "crianca": {"criança", "crianca", "crianças", "criancas", "3 anos", "4 anos", "5 anos", "6 anos", "7 anos", "8 anos", "9 anos",
                "10 anos", "11 anos", "12 anos"},
    "adolescente": {"adolescente", "adolecente", "adoslecente", "13 anos", "14 anos", "15 anos", "16 anos", "17 anos"},
    "adulto_jovem": {"adulto jovem", "jovem", "juventude"},
    "adulto": {"adulto", "adultos"},
    "idoso": {"idoso", "idosa", "idosos", "idosas", "velho", "velha", "anciao", "ancia"}
} 

SEXO_POR_NUMERO = {
    "1": "masculino",
    "2": "feminino"
}

SEXO_SINONIMOS = {
    "masculino": {"masculino", "homem", "h", "macho"},
    "feminino": {"feminino", "mulher", "m", "f", "femea"},
}


HISTORICO_POR_NUMERO = {
    "1": "diabetes",
    "2": "imunossupressao",
    "3": "estresse",
    "4": "asma",
    "5": "rinite",
    "6": "dermatite",
    "7": "ansiedade",
    "8": "doencas_autoimunes",
    "9": "fatores_geneticos",
    "10": "contato_sexual_desprotegido",
    "11": "atopia",
    "12": "contato_casos_familiares",
    "13": "exposicao_solar",
    "14": "ambiente_umido",
    "15": "sapatos_fechados",
    "16": "contato_agentes_irritantes",
    "17": "varizes",
    "18": "obesidade",
    "19": "artrites_deformantes",
    "20": "eczema",
    "21": "picadas_inseto",
    "22": "oleosidade",
    "23": "infeccao_viral_previa",
    "24": "psoriase",
    "25": "reacao_medicamentosa",
    "26": "nenhum_especifico"
}

HISTORICO_SINONIMOS = {
    "diabetes": {"diabetes", "diabete", "diabético", "diabetico"},
    "imunossupressao": {"imunossupressão", "imunossupresso", "baixa imunidade", "imunidade baixa", "imunodepressão"},
    "estresse": {"estresse", "stress", "estressado", "estresse emocional", "tensão", "estressada", "tenso"},
    "asma": {"asma", "asmático", "asmatico", "falta de ar", "crise asmática"},
    "rinite": {"rinite", "rinite alérgica", "alergia nasal", "nariz entupido"},
    "dermatite": {"dermatite", "inflamação na pele", "dermatite de contato", "dermatite atópica", "eczema"},
    "ansiedade": {"ansiedade", "ansioso", "ansiosa", "nervosismo", "preocupação", "nervosa", "nervoso"},
    "doencas_autoimunes": {"doenças autoimunes", "doença autoimune", "autoimune", "lúpus", "lupus", "artrite reumatoide", "doença do sistema imunológico"},
    "fatores_geneticos": {"fatores genéticos", "genética", "hereditário", "hereditariedade", "histórico familiar"},
    "contato_sexual_desprotegido": {"contato sexual desprotegido", "relação sexual sem proteção", "sexo sem camisinha", "sexo sem proteção"},
    "atopia": {"atopia", "atópico", "atopico", "alergia crônica", "predisposição alérgica"},
    "contato_casos_familiares": {"contato com casos familiares", "família com a mesma doença", "caso na família", "parente com o mesmo problema"},
    "exposicao_solar": {"exposição solar", "sol", "muito sol", "ficar no sol", "sol em excesso"},
    "ambiente_umido": {"ambiente úmido", "lugar úmido", "umidade", "muita umidade", "local abafado"},
    "sapatos_fechados": {"sapatos fechados", "usar sapato fechado", "calçado fechado", "sapato o tempo todo"},
    "contato_agentes_irritantes": {"contato direto com agentes irritantes", "produtos químicos", "detergente", "sabão em pó", "água sanitária", "substâncias irritantes"},
    "varizes": {"varizes", "veias dilatadas", "problemas de circulação", "má circulação"},
    "obesidade": {"obesidade", "sobrepeso", "acima do peso", "gordo", "excesso de peso"},
    "artrites_deformantes": {"artrites deformantes", "artrite deformante", "artrite grave", "artrose", "artrite"},
    "eczema": {"eczema", "coceira com vermelhidão", "pele irritada", "descamação"},
    "picadas_inseto": {"picadas de inseto", "picada de mosquito", "mordida de inseto", "picada", "inseto"},
    "oleosidade": {"oleosidade", "pele oleosa", "sebo", "pele brilhante"},
    "infeccao_viral_previa": {"infecção viral prévia", "infecção anterior", "vírus recente", "resfriado recente", "gripe recente"},
    "psoriase": {"psoríase", "psoriase", "placas avermelhadas", "descamação grossa", "doença autoimune da pele"},
    "reacao_medicamentosa": {"reação medicamentosa", "alergia a remédio", "alergia medicamentosa", "efeito colateral de remédio"},
    "nenhum_especifico": {"nenhum específico", "nenhum", "nada", "sem causa", "não sei", "não", "nenhuma", "nenhum fator"}
}
    
ALERGIA_POR_NUMEROS = {
    "1": "anticonvulsivantes",
    "2": "sulfas",
    "3": "antibioticos",
    "4": "nao",
    "5": "nao_sei"
}

ALERGIA_SINONIMOS = {
    "anticonvulsivantes": {"anticonvulsivantes", "anticonvulsivante"},
    "sulfas": {"sulfas", "sulfa", "sulfatos", "sulfato"},
    "antibioticos": {"antibioticos", "antibióticos", "antibiotico", "antibiótico"},
    "nao": {"nao", "nao tem", "não", "n"},
    "nao_sei": {"nao sei", "sei la", "desconhecido"}
}