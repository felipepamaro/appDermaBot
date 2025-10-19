# motor_cnf.py
from typing import Dict, List, Set, Any
import json

# 1) Importe a base que você já usa
from baseConhecimento import BASE_CONHECIMENTO  # :contentReference[oaicite:1]{index=1}


# ---------- Config: mapeamento peso -> CNF ----------
# Ajuste livremente estes valores conforme sua calibração/validação:
WEIGHT_TO_CNF = {0: 0.0, 1: 0.4, 2: 0.7, 3: 0.9}

AXES = ["sintomas", "sinais", "local", "idade", "sexo", "historico", "alergia"]


def weight_to_cnf(w: int) -> float:
    return WEIGHT_TO_CNF.get(int(w), 0.0)


# ---------- (A) Gerar JSON a partir do BASE_CONHECIMENTO ----------
def gerar_json_regras(base: Dict[str, Dict[str, Dict[str, int]]]) -> Dict[str, Any]:
    rules_out = {
        "schema_version": 1,
        "weight_to_cnf": {str(k): float(v) for k, v in WEIGHT_TO_CNF.items()},
        "axes": AXES,
        "rules": []
    }

    for disease, axes_map in base.items():
        antecedents = []
        for axis in AXES:
            axis_terms = axes_map.get(axis if axis != "local" else "local", {})  # nome igual ao da base
            for term, w in axis_terms.items():
                if w and int(w) > 0:
                    antecedents.append({"axis": axis, "term": term, "w": int(w)})
        rules_out["rules"].append({"disease": disease, "antecedents": antecedents})

    return rules_out


# ---------- (B) Inferência: combinar CNFs (acumulação otimista) ----------
def combinar_otimista(cf_total: float, cf_e: float) -> float:
    """
    Combina evidências positivas (independentes) no estilo MYCIN (OR probabilístico):
    CF_new = CF_total + CF_e * (1 - CF_total)
    """
    if cf_e <= 0:
        return cf_total
    return cf_total + cf_e * (1.0 - cf_total)


def inferir_diagnosticos(
    fatos: Dict[str, Set[str]],
    regras_json: Dict[str, Any],
    detalhar: bool = True
) -> Dict[str, Any]:
    """
    fatos: {"sintomas":{"prurido","dor"}, "sinais":{"vesicula"}, ...}
    regras_json: dicionário no formato gerado por gerar_json_regras(...)
    return:
        {
          "scores": [("doenca", cf), ... ordenado],
          "detalhes": {
             "doenca": {
                "cf": 0.87,
                "matches": [
                    {"axis":"sintomas","term":"prurido","w":1,"cnf":0.4},
                    {"axis":"sinais","term":"vesicula","w":2,"cnf":0.7},
                    ...
                ]
             },
             ...
          }
        }
    """
    detalhes = {}
    for rule in regras_json["rules"]:
        disease = rule["disease"]
        cf_total = 0.0
        matches = []

        for ant in rule["antecedents"]:
            axis = ant["axis"]
            term = ant["term"]
            w = int(ant["w"])
            if axis in fatos and term in fatos[axis]:
                cnf = weight_to_cnf(w)
                cf_total = combinar_otimista(cf_total, cnf)
                if detalhar:
                    matches.append({"axis": axis, "term": term, "w": w, "cnf": cnf})

        detalhes[disease] = {"cf": round(cf_total, 4), "matches": matches}

    # Ranking
    scores = sorted(((d, info["cf"]) for d, info in detalhes.items()),
                    key=lambda x: x[1], reverse=True)

    return {"scores": scores, "detalhes": detalhes}


# ---------- (C) Exemplo de uso ----------
if __name__ == "__main__":
    # 1) Gerar JSON e (opcional) salvar
    regras = gerar_json_regras(BASE_CONHECIMENTO)
    with open("regras_cnf.json", "w", encoding="utf-8") as f:
        json.dump(regras, f, ensure_ascii=False, indent=2)

    # 2) Fatos simulados vindos do chat (já normalizados pelo seu pipeline)
    fatos_paciente = {
        "sintomas": {"prurido"},
        "sinais": {"vesicula"},
        "local": {"labios"},
        "idade": {"adulto_jovem"},
        "sexo": {"feminino"},
        "historico": {"estresse"},
        "alergia": {"nao"}
    }

    resultado = inferir_diagnosticos(fatos_paciente, regras)
    print("Ranking:")
    for doenca, cf in resultado["scores"][:5]:
        print(f" - {doenca}: CF={cf:.3f}")

    # Para inspecionar explicações:
    # import pprint; pprint.pprint(resultado["detalhes"]["herpes_simples"])
