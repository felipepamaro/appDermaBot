from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from regras import (
    interpretar_sintomas, interpretar_sinais, interpretar_locais,
    interpretar_idade, interpretar_sexo, interpretar_historico, interpretar_alergia,
    formatar_resposta, _prettify
)
from baseConhecimento import BASE_CONHECIMENTO
from motorCNF import gerar_json_regras, inferir_diagnosticos

app = Flask(__name__)

# Gera o JSON de regras (uma única vez no boot do app)
REGRAS_JSON = gerar_json_regras(BASE_CONHECIMENTO)

# Armazenar o progresso de cada usuário
user_sessions = {}

# Próxima pergunta de acordo com a etapa
def proxima_pergunta(etapa):
    perguntas = {
    "inicio": "Olá, seja bem vindo(a) ao DermaBot! Gostaria de prosseguir para o pré-diagnóstico de alguma doença dermatológica?\n"
    "1-Sim\n2-Sair",
    "sintomas": "Vamos iniciar. Quais os *sintomas* do paciente?\n"
    "1- Prurido/coceira\n2- Ardor/queimação\n3- Dor\n4- Formigamento/parestesia\n5- Perda de sensibilidade\n6-Dormência\n7- Assintomático",
    "sinais": "Quais os *sinais clínicos* observados?\n1- Lesões eritematosas\n2- Edema\n3- Vesículas\n4- Bolhas\n5- Fissura\n6- Ressecamento\n"
    "7- Descamação\n8- Placas eritematosas\n9- Bordas circinadas\n10- Escamas finas\n11- Úlcera indolor (cancro duro)\n"
    "12- Máculas hipocrômicas ou eritematosas\n13- Dermatite ocre\n14- Placa liquenificada\n 15- Acentuação dos sulcos\n16- Hiperpigmentação\n"
    "17- Bordas bem definidas\n18- Placa-mãe oval\n19- Erupções secundárias em tronco\n20- Erupção eritemato-descamativa\n"
    "21- Lesões eritematosas em alvo\n22- Nódulos avermelhados e firmes",
    "localizacao": "Em qual *local* do corpo essas alterações apareceram?\n1- Disseminado\n2- Região palmo plantar\n3- Couro cabeludo\n"
    "4- Unhas\n5- Tronco\n6- Dobras (virilha)\n7- Lábios\n8- Genitais\n9-Face\n10- Áreas flexoras (cotovelos e joelhos)\n"
    "11- Membros inferiores e/ou superiores\n12- Nuca\n13- Região sacra",
    "idade": "Qual é a *idade* do(a) paciente?\n1- Bebê\n2- Criança\n3- Adolescente\n4- Adulto jovem\n5- Adulto\n"
    "6- Idoso",
    "sexo": "Qual é o *sexo* do(a) paciente?\n1- Masculino\n2- Feminino",
    "historico": "Há algum *histórico relevante*?\n1- Diabetes\n2- Imunossupressão\n3- Estresse\n4- Asma\n"
    "5- Rinite\n6- Dermatite\n7- Ansiedade\n8- Doenças autoimunes\n9- Fatores genéticos\n10- Contato sexual desprotegido\n"
    "11- Atopia\n12- Contato com casos familiares\n13- Exposição solar\n14- Ambiente úmido\n15- Sapatos fechados\n"
    "16- Contato direto com agentes irritantes\n17- Varizes\n18- Obesidade\n19- Artristes deformantes\n20- Eczema\n"
    "21- Picadas de inseto\n22- Oleosidade\n23- Infecção viral prévia\n24- Psoríase\n25- Reação medicamentosa\n26- Nenhum específico",
    "alergia": "O paciente tem alguma *alergia medicamentosa* conhecida?\n"
    "1- Sim (anticonvulsivantes)\n2- Sim (sulfas)\n3- Sim (antibióticos)\n4- Não\n5- Não sei",
    "final": "Obrigado pelas informações!\n\nAgora irei analisar os dados e gerar um *pré-diagnóstico* com base nos sintomas relatados."
    }
    return perguntas.get(etapa, "Fim do questionário.")

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "OK"}, 200

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "OK", "message": "Esta é uma api do app DermaBot, para uso exclusivo do integrador"}, 200



@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip().lower()
    user_number = request.form.get("From", "desconhecido")

    # Recupera ou cria nova sessão
    session = user_sessions.get(user_number, {"etapa": "inicio", "respostas": {}, "mostrou_inicio": False})
    etapa = session.get("etapa", "inicio")

    resposta = MessagingResponse()
    mensagem = resposta.message()

    # ----
    # LISTAS de comandos
    iniciar = {"1", "1-", "1.", "sim", "s", "continuar", "quero", "bora", "iniciar", "start"}
    encerrar   = {"2", "2-", "2.", "sair", "encerrar", "finalizar", "não", "n", "nao", "fim"}
    reiniciar   = {"iniciar", "start", "sim", "s", "recomeçar", "reiniciar", "de novo", "recomecar"}  # para recomeçar após encerrar
    # ----

    # Mostra mensagem de boas-vindas na primeira interação
    if etapa == "inicio" and not session.get("mostrou_inicio", False):
        mensagem.body("Olá, seja bem vindo(a) ao DermaBot! Gostaria de prosseguir para o pré-diagnóstico de alguma doença dermatológica?\n1-Sim\n2-Sair")
        session["mostrou_inicio"] = True
        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")

    # Controle de fluxo
    if etapa == "inicio":
        if incoming_msg in iniciar:
            session["etapa"] = "sintomas"
            mensagem.body(proxima_pergunta("sintomas"))
        elif incoming_msg in encerrar:
            session["etapa"] = "encerrado"
            mensagem.body(
                "Obrigado por utilizar o DermaBot! A conversa foi encerrada.\n\n"
                "Para recomeçar a qualquer momento, digite: *Iniciar*"
            )
        else:
            mensagem.body("Desculpe, não entendi sua resposta.\n\n" + proxima_pergunta("inicio"))

    elif etapa == "encerrado":
        if incoming_msg in reiniciar:
            session["etapa"] = "sintomas"
            mensagem.body(proxima_pergunta("sintomas"))
        else:
            mensagem.body("A aplicação está *encerrada* no momento. Para recomeçar, digite: *Iniciar*")

    elif etapa == "sintomas":
        try:
            sintomas_relatados = interpretar_sintomas(incoming_msg or "")
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        if not sintomas_relatados:
            mensagem.body("Não reconheci os sintomas. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("sintomas"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        session["respostas"]["sintomas"] = sorted(list(sintomas_relatados))
        session["etapa"] = "sinais"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["sintomas"])
        mensagem.body(f"Anotado ✅ Sintomas: {confirmacao}\n\n{proxima_pergunta('sinais')}")

        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")

    elif etapa == "sinais":
        try:
            sinais_relatados = interpretar_sinais(incoming_msg)
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        if not sinais_relatados:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("sinais"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        session["respostas"]["sinais_clinicos"] = sorted(list(sinais_relatados))
        session["etapa"] = "localizacao"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["sinais_clinicos"])
        mensagem.body(f"Anotado ✅ Sinais: {confirmacao}\n\n{proxima_pergunta('localizacao')}")

        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")

    elif etapa == "localizacao":
        try:
            locais_relatados = interpretar_locais(incoming_msg)
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        if not locais_relatados:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("localizacao"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        session["respostas"]["localizacao_tipica"] = sorted(list(locais_relatados))
        session["etapa"] = "idade"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["localizacao_tipica"])
        mensagem.body(f"Anotado ✅ Localização: {confirmacao}\n\n{proxima_pergunta('idade')}")

        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")

    elif etapa == "idade":
        try:
            idade_relatada = interpretar_idade(incoming_msg)
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        if not idade_relatada:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("idade"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        session["respostas"]["idade"] = sorted(list(idade_relatada))
        session["etapa"] = "sexo"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["idade"])
        mensagem.body(f"Anotado ✅ Idade: {confirmacao}\n\n{proxima_pergunta('sexo')}")

        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")
    
    elif etapa == "sexo":
        try:
            sexo_relatado = interpretar_sexo(incoming_msg)
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        if not sexo_relatado:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("sexo"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        session["respostas"]["sexo"] = sorted(list(sexo_relatado))
        session["etapa"] = "historico"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["sexo"])
        mensagem.body(f"Anotado ✅ Sexo: {confirmacao}\n\n{proxima_pergunta('historico')}")

        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")

    elif etapa == "historico":
        try:
            historico_relatado = interpretar_historico(incoming_msg)
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        if not historico_relatado:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("historico"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        session["respostas"]["historico_relevante"] = sorted(list(historico_relatado))
        session["etapa"] = "alergia"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["historico_relevante"])
        mensagem.body(f"Anotado ✅ Histórico relevante: {confirmacao}\n\n{proxima_pergunta('alergia')}")

        user_sessions[user_number] = session
        return Response(str(resposta), mimetype="application/xml")

    elif etapa == "alergia":
        try:
            alergia_relatada = interpretar_alergia(incoming_msg)
        except Exception:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.")
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")
        
        if not alergia_relatada:
            mensagem.body("Desculpe, mas não entendi. Responda com as opções disponíveis por favor.\n\n" + proxima_pergunta("alergia"))
            user_sessions[user_number] = session
            return Response(str(resposta), mimetype="application/xml")

        session["respostas"]["alergia_medicamentosa"] = sorted(list(alergia_relatada))
        session["etapa"] = "final"
        
        confirmacao = ", ".join(_prettify(s) for s in session["respostas"]["alergia_medicamentosa"])
        mensagem.body(f"Anotado ✅ Alergia medicamentosa: {confirmacao}\n\n{proxima_pergunta('final')}")

        respostas = session["respostas"]
        resumo = (
            f"*Resumo do caso clínico:*\n"
            f"- Sintomas: {formatar_resposta(respostas.get('sintomas'))}\n"
            f"- Sinais clínicos: {formatar_resposta(respostas.get('sinais_clinicos'))}\n"
            f"- Localização típica: {formatar_resposta(respostas.get('localizacao_tipica'))}\n"
            f"- Idade: {formatar_resposta(respostas.get('idade'))}\n"
            f"- Sexo: {formatar_resposta(respostas.get('sexo'))}\n"
            f"- Histórico relevante: {formatar_resposta(respostas.get('historico_relevante'))}\n"
            f"- Alergia medicamentosa: {formatar_resposta(respostas.get('alergia_medicamentosa'))}\n\n"
            "Esses dados podem indicar algumas condições dermatológicas. "
        )
        mensagem.body(resumo)

        # --- CNF: monta fatos nos nomes esperados pelo motor ---
        facts = {
            "sintomas": set(session["respostas"].get("sintomas", [])),
            "sinais": set(session["respostas"].get("sinais_clinicos", [])),          # map: sinais_clinicos -> sinais
            "local": set(session["respostas"].get("localizacao_tipica", [])),         # map: localizacao_tipica -> local
            "idade": set(session["respostas"].get("idade", [])),
            "sexo": set(session["respostas"].get("sexo", [])),
            "historico": set(session["respostas"].get("historico_relevante", [])),    # map: historico_relevante -> historico
            "alergia": set(session["respostas"].get("alergia_medicamentosa", [])),    # map: alergia_medicamentosa -> alergia
        }
        
        resultado = inferir_diagnosticos(facts, REGRAS_JSON, detalhar=True)
        
        # Top-3 por CF
        top = resultado["scores"][:3]
        if not top or (len(top) > 0 and top[0][1] <= 0.0):
            mensagem.body("\n\nAinda não há evidência suficiente para sugerir uma condição específica.")
        
        else:
            linhas = []
            for doenca, cf in top:
                nome = doenca.replace("_", " ").title()
                linhas.append(f"• {nome}: {cf*100:.1f}%")
            mensagem.body("\n\n📋 Sugestões (CNF):\n" + "\n".join(linhas) +
                          "\n\n⚠️ Isto é triagem automatizada e **não substitui** avaliação clínica.")
    else:
        session["etapa"] = "inicio"
        mensagem.body(proxima_pergunta("inicio"))

    # Atualiza sessão
    user_sessions[user_number] = session
    return Response(str(resposta), mimetype="application/xml")


if __name__ == "__main__":
    app.run(port=5000)
